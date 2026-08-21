#!/usr/bin/env python3
"""Il Consigliere — report TESTUALE nel terminale, dati reali, formato "oro".

Stampa esattamente lo stile che piace a Sal: verdetto, i thread/chat più pesanti
con dati veri (data | token | modello/effort | titolo), la spiegazione semplice,
poi le soluzioni pratiche. Nessun HTML, nessun template, nessun modello AI:
legge i dati locali (Codex `~/.codex/state_5.sqlite` + Claude `~/.claude/projects`)
e li stampa. Gira con un comando.

    ~/leaderai/.venv/bin/python tools/il-consigliere/consigliere.py
    ~/leaderai/.venv/bin/python tools/il-consigliere/consigliere.py --days 14 --top 6
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sqlite3
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODEX_DB = Path("~/.codex/state_5.sqlite").expanduser()
CLAUDE_REPORT_CANDIDATES = [
    HERE.parent / "claude-usage" / "report.py",      # LeaderAI interno
    HERE / "collector" / "claude_usage.py",          # kit cliente
]


def claude_report_path() -> Path | None:
    for path in CLAUDE_REPORT_CANDIDATES:
        if path.exists():
            return path
    return None


def m(tok: int | float) -> str:
    """Token -> '57,1M' (virgola italiana)."""
    return f"{tok / 1_000_000:.1f}".replace(".", ",") + "M"


def gg_mm(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime("%d/%m")


def codex_section(days: int, top: int) -> list[str]:
    if not CODEX_DB.exists():
        return ["(Codex: nessun dato locale su questo Mac.)"]
    con = sqlite3.connect(f"file:{CODEX_DB}?mode=ro", uri=True)
    try:
        total = con.execute(
            "select coalesce(sum(tokens_used),0) from threads "
            "where tokens_used>0 and updated_at>=strftime('%s','now',?)",
            (f"-{days} days",),
        ).fetchone()[0]
        bucket = con.execute(
            "select coalesce(model,'?'), coalesce(reasoning_effort,'?'), sum(tokens_used) "
            "from threads where tokens_used>0 and updated_at>=strftime('%s','now',?) "
            "group by model,reasoning_effort order by sum(tokens_used) desc limit 1",
            (f"-{days} days",),
        ).fetchone()
        heavy = con.execute(
            "select updated_at, tokens_used, coalesce(model,'?'), coalesce(reasoning_effort,'?'), "
            "replace(substr(title,1,60),char(10),' ') from threads "
            "where tokens_used>0 and updated_at>=strftime('%s','now',?) "
            "order by tokens_used desc limit ?",
            (f"-{days} days", top),
        ).fetchall()
    finally:
        con.close()

    out = []
    if bucket:
        out.append(
            f"Dai dati locali su questo Mac, negli ultimi {days} giorni il grosso consumo Codex "
            f"viene da thread con {bucket[0]} e reasoning {bucket[1]}: circa {m(bucket[2])} token locali."
        )
    out.append("I thread Codex più pesanti:")
    for up, tok, mod, eff, title in heavy:
        out.append(f"  {gg_mm(up)} | {m(tok)} | {mod} {eff} | {title}")
    out.append(f"Totale Codex {days}gg: {m(total)} token.")
    return out


def claude_section(top: int) -> list[str]:
    report = claude_report_path()
    if not report:
        return []
    spec = importlib.util.spec_from_file_location("claude_usage_report", report)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    per_session, _, _ = mod.scan(mod.DEFAULT_PROJECTS_DIR, "leaderai")
    if not per_session:
        return ["(Claude: nessun dato locale.)"]
    grand = sum(s["total"] for s in per_session.values())
    grand_cr = sum(s["cache_r"] for s in per_session.values())
    heavy = sorted(per_session.values(), key=lambda s: s["total"], reverse=True)[:top]
    out = [
        f"Su Claude Code: {m(grand)} token processati, di cui {mod.pct(grand_cr, grand)} "
        f"è contesto già trascinato (cache), non testo nuovo. Le chat più pesanti:"
    ]
    for s in heavy:
        out.append(f"  {s['last'] or '?'} | {m(s['total'])} | {(s['model'] or '?').replace('claude-','')} cache {mod.pct(s['cache_r'], s['total'])} | {mod.session_title(s['path'])}")
    return out


def _short_title(t: str, n: int = 42) -> str:
    t = " ".join((t or "").split())
    return (t[:n] + "…") if len(t) > n else t


def verdict(days: int) -> str:
    """La riga di apertura: una conclusione VERA calcolata dai dati di oggi,
    non una frase fissa. Sceglie il segnale più forte tra Codex e Claude."""
    cands: list[tuple[float, str]] = []

    # Codex
    if CODEX_DB.exists():
        con = sqlite3.connect(f"file:{CODEX_DB}?mode=ro", uri=True)
        try:
            tot = con.execute(
                "select coalesce(sum(tokens_used),0) from threads "
                "where tokens_used>0 and updated_at>=strftime('%s','now',?)",
                (f"-{days} days",)).fetchone()[0] or 0
            if tot:
                th = con.execute(
                    "select tokens_used, replace(substr(title,1,60),char(10),' ') from threads "
                    "where tokens_used>0 and updated_at>=strftime('%s','now',?) "
                    "order by tokens_used desc limit 1", (f"-{days} days",)).fetchone()
                if th:
                    sh = th[0] / tot
                    cands.append((sh, f"Una sola chat Codex — \"{_short_title(th[1])}\" — vale il {round(sh*100)}% del consumo: il problema non è quante ne apri, è tenerle aperte troppo a lungo."))
                bk = con.execute(
                    "select coalesce(model,'?'), coalesce(reasoning_effort,'?'), sum(tokens_used) from threads "
                    "where tokens_used>0 and updated_at>=strftime('%s','now',?) "
                    "group by model,reasoning_effort order by sum(tokens_used) desc limit 1",
                    (f"-{days} days",)).fetchone()
                if bk:
                    sh = bk[2] / tot
                    cands.append((sh * 0.85, f"Il grosso del consumo Codex è {bk[0]} {bk[1]} ({round(sh*100)}%): non è il numero di messaggi, è il reasoning alto."))
        finally:
            con.close()

    # Claude
    report = claude_report_path()
    if report:
        spec = importlib.util.spec_from_file_location("claude_usage_report", report)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ps, _, _ = mod.scan(mod.DEFAULT_PROJECTS_DIR, "leaderai")
        grand = sum(s["total"] for s in ps.values())
        if grand:
            cr = sum(s["cache_r"] for s in ps.values()) / grand
            cands.append((cr, f"Su Claude il {round(cr*100)}% del consumo è contesto riletto a ogni turno, non testo nuovo: paghi le chat lunghe, non le risposte."))
            top = max(ps.values(), key=lambda s: s["total"])
            sh = top["total"] / grand
            cands.append((sh, f"Una sola chat Claude — \"{_short_title(mod.session_title(top['path']))}\" — vale il {round(sh*100)}% del totale: tenerla aperta è costato più di tutto il resto."))

    if not cands:
        return "Nessun dato locale sufficiente per un verdetto questa settimana."
    return max(cands, key=lambda c: c[0])[1]


SOLUZIONI = [
    "Usa il modello pesante / xhigh solo quando serve (architettura, debug duro, decisioni). Per il resto: leggero, risposta breve.",
    "Chat nuova per ogni task grosso. Un thread vecchio porta dietro tutto il contesto e pesa tantissimo.",
    "Prima chiedi la diagnosi, poi autorizzi l'azione: \"dimmi quali file leggeresti, non leggere ancora tutto\".",
    "Limita il perimetro: non \"controlla il workspace\", ma \"controlla solo commerciale/<cliente>, STATUS + proposta\".",
    "Modelli leggeri per task semplici (riassunti, comandi, piccole modifiche).",
    "Niente report lunghi se non servono: \"dammi solo causa, prova, prossima azione\".",
    "Chiudi i task in micro-step: prima trova, poi analizza solo il pezzo scelto. Non \"analizza tutto\".",
]


SOLUZIONI_CLIENTE = [
    "Una conversazione = un obiettivo. Se cambi lavoro, apri una nuova conversazione.",
    "Prima di chiedere all'AI di fare, dille esattamente cosa deve guardare e cosa deve ignorare.",
    "Quando passi da analizzare a scrivere, cambia chat: analizzare e scrivere sono due lavori diversi.",
    "Se una richiesta contiene tante cose insieme, spezzala in due passaggi: prima capire, poi fare.",
    "Quando una richiesta si ripete spesso, trasformala in una procedura pronta da riusare.",
]


def learning_level() -> tuple[str, str, str]:
    """Prima versione semplice: un livello deciso dal pattern dominante.
    In futuro andra' confrontato con i report precedenti per evitare ripetizioni."""
    if not CODEX_DB.exists():
        return (
            "Livello 1 — Spegni sprechi evidenti",
            "Non ho abbastanza dati Codex per dire cosa hai gia' migliorato.",
            "Usa una conversazione per un solo obiettivo.",
        )

    con = sqlite3.connect(f"file:{CODEX_DB}?mode=ro", uri=True)
    try:
        rows = con.execute(
            "select tokens_used, coalesce(reasoning_effort,''), coalesce(title,'') from threads "
            "where tokens_used>0 and updated_at>=strftime('%s','now','-14 days') "
            "order by tokens_used desc limit 10"
        ).fetchall()
    finally:
        con.close()

    if not rows:
        return (
            "Livello 1 — Spegni sprechi evidenti",
            "Nessun thread pesante recente da confrontare.",
            "Tieni il perimetro stretto prima di far partire l'agente.",
        )

    xhigh = sum(tok for tok, effort, _ in rows if effort == "xhigh")
    total = sum(tok for tok, _, _ in rows)
    top_share = rows[0][0] / total if total else 0

    if top_share > 0.25:
        return (
            "Livello 3 — Cambi fase bene",
            "Hai gia' capito che il problema non e' il numero di messaggi.",
            "Quando passi da analizzare a scrivere o modificare, apri una chat nuova.",
        )
    if total and xhigh / total > 0.55:
        return (
            "Livello 2 — Prompt piu' stretti",
            "Il perimetro e' il prossimo punto: non basta usare meno, devi chiedere meglio.",
            "Per ogni richiesta indica file, obiettivo e formato della risposta.",
        )
    return (
        "Livello 4 — Procedure riusabili",
        "Gli sprechi evidenti stanno calando: ora guarda cosa si ripete.",
        "Se chiedi la stessa cosa due volte, falla diventare procedura o template.",
    )


def translate_for_client(line: str) -> str:
    """Trasforma alcuni termini tecnici in linguaggio cliente."""
    if re.match(r"^\s+\d{2}/\d{2} \|", line):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            return f"  {parts[0]} | peso {parts[1]} | {parts[3]}"
    if re.match(r"^\s+\d{4}-\d{2}-\d{2} \|", line):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 4:
            return f"  {parts[0]} | peso {parts[1]} | {parts[3]}"
    phrase_repl = {
        "Dai dati locali su questo Mac, negli ultimi": "Dai dati locali su questo computer, negli ultimi",
        "il grosso consumo Codex viene da thread con": "il lavoro piu' pesante per Codex viene da conversazioni con",
        "viene da conversazioni con gpt-5.5 e reasoning xhigh": "viene da conversazioni in modalita' pesante",
        "viene da conversazioni con gpt-5.5 in modalita' pesante": "viene da conversazioni in modalita' pesante",
        "e reasoning xhigh": "in modalita' pesante",
        "I thread Codex più pesanti:": "Le conversazioni Codex piu' pesanti:",
        "Totale Codex": "Totale lavoro Codex",
        "Su Claude Code:": "Su Claude:",
        "dati locali per capire chi pesa": "dati locali per capire quali conversazioni pesano",
        "token locali": "unita' locali di lavoro AI",
        "token processati": "unita' di lavoro AI processate",
        "cache": "contesto riletto",
        "thread vecchio": "conversazione vecchia",
        "thread": "conversazione",
    }
    for src, dst in phrase_repl.items():
        line = line.replace(src, dst)
    repl = {
        "token": "unita' di lavoro AI",
        "reasoning": "modalita' di ragionamento",
        "xhigh": "modalita' pesante",
        "contesto trascinato": "cose vecchie che l'AI deve rileggere",
    }
    for src, dst in repl.items():
        line = line.replace(src, dst)
    return line


def main() -> int:
    ap = argparse.ArgumentParser(description="Il Consigliere — report testuale dati reali")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--audience", choices=["sal", "cliente"], default="sal")
    args = ap.parse_args()

    line = "─" * 70
    print(line)
    print("IL CONSIGLIERE — Efficacia & Efficienza")
    print(verdict(args.days))
    print(line)
    print()
    for r in codex_section(args.days, args.top):
        print(translate_for_client(r) if args.audience == "cliente" else r)
    print()
    cl = claude_section(args.top)
    if cl:
        for r in cl:
            print(translate_for_client(r) if args.audience == "cliente" else r)
        print()
    if args.audience == "cliente":
        print("Quindi: non stai usando l'AI \"troppe volte\". Stai mettendo troppi lavori diversi")
        print("nelle stesse conversazioni. L'AI deve rileggere troppe cose e risponde peggio o piu' lentamente.")
    else:
        print("Quindi: non usi gli agenti \"troppe volte\", li usi su lavori più grossi —")
        print("più contesto, più file, reasoning più alto. È questo che brucia.")
    print()
    livello, migliorato, mossa = learning_level()
    if args.audience == "cliente":
        livello = livello.replace("Prompt piu' stretti", "Richieste piu' chiare")
        migliorato = "Hai gia' capito che non conta solo quanto usi l'AI: conta come organizzi il lavoro."
        mossa = "Per ogni richiesta indica obiettivo, materiale da guardare e risultato che vuoi."
    print("Livello da sbloccare:")
    print(f"  {livello}")
    print(f"  Cosa hai gia' migliorato: {migliorato}")
    print(f"  Mossa della settimana: {mossa}")
    print()
    print("Soluzioni pratiche, in ordine di impatto:")
    soluzioni = SOLUZIONI_CLIENTE if args.audience == "cliente" else SOLUZIONI
    for i, s in enumerate(soluzioni, 1):
        print(f"  {i}. {s}")
    print()
    print("Nota: dati locali per capire chi pesa. Il conto vero resta nel pannello ufficiale.")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
