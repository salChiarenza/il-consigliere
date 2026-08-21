#!/usr/bin/env python3
"""Dossier per il tutor di efficienza (passo dati, a costo zero di modello).

Mette insieme il materiale grezzo su cui il tutor (un giro Sonnet) scrivera' i
consigli:
1. il report consumi di Claude Code  (tools/claude-usage/report.py)
2. il report consumi di Codex         (tools/codex-usage/report.py)
3. un CAMPIONE LIMITATO delle sessioni Claude piu' pesanti
   (primi e ultimi messaggi, troncati) — MAI il transcript intero, altrimenti
   leggere una chat-mostro costerebbe come rifarla.

Output: un markdown su stdout (o --write su file). Non chiama modelli ne' API.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
VENV_PY = REPO / ".venv" / "bin" / "python"


def _find(repo_rel: str, *sibling_names: str) -> Path:
    """Trova uno script sia nel repo leaderai sia nel kit standalone (file accanto).

    In leaderai vive in `tools/<area>/report.py`; nel kit consegnato al cliente
    vive accanto a questo file (es. `claude_usage.py`). Cosi' lo stesso dossier
    gira in entrambi i contesti senza modifiche.
    """
    candidate = REPO / repo_rel
    if candidate.exists():
        return candidate
    for name in sibling_names:
        sib = HERE / name
        if sib.exists():
            return sib
    return candidate


CLAUDE_REPORT = _find("tools/claude-usage/report.py", "claude_usage.py")
CODEX_REPORT = _find("tools/codex-usage/report.py", "codex_usage.py")


def run_report(script: Path, extra: list[str]) -> str:
    """Esegue un report.py e cattura il testo. Non blocca se uno fallisce."""
    if not script.exists():
        return f"(report non trovato: {script})"
    py = str(VENV_PY) if VENV_PY.exists() else sys.executable
    try:
        out = subprocess.run(
            [py, str(script), *extra],
            capture_output=True, text=True, timeout=120,
        )
        return out.stdout.strip() or out.stderr.strip() or "(nessun output)"
    except Exception as exc:  # diagnosi: il dossier non deve morire per un report
        return f"(errore esecuzione {script.name}: {exc})"


def load_claude_scan():
    """Importa scan()/session_title() da tools/claude-usage/report.py."""
    spec = importlib.util.spec_from_file_location("claude_usage_report", CLAUDE_REPORT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def short(text: str, limit: int = 280) -> str:
    text = " ".join((text or "").split())
    return text[:limit] + ("…" if len(text) > limit else "")


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            t = block.get("type")
            if t == "text":
                parts.append(block.get("text", ""))
            elif t == "tool_use":
                parts.append(f"[tool: {block.get('name', '?')}]")
            elif t == "tool_result":
                parts.append("[tool_result]")
        return " ".join(p for p in parts if p)
    return ""


def sample_session(path: Path, head: int = 18, tail: int = 6) -> str:
    """Estratto limitato: primi `head` e ultimi `tail` messaggi reali, troncati."""
    msgs: list[str] = []
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                typ = row.get("type")
                if typ not in ("user", "assistant"):
                    continue
                text = extract_text(row.get("message", {}).get("content"))
                if not text:
                    continue
                text = text.strip()
                if text.startswith("<") or text.startswith("Caveat:"):
                    continue  # blocchi iniettati da sistema/hook
                who = "Sal" if typ == "user" else "Claude"
                msgs.append(f"  [{who}] {short(text)}")
    except OSError as exc:
        return f"  (impossibile leggere: {exc})"

    if len(msgs) <= head + tail:
        body = msgs
    else:
        body = msgs[:head] + [f"  … ({len(msgs) - head - tail} messaggi in mezzo) …"] + msgs[-tail:]
    return "\n".join(body) if body else "  (nessun messaggio leggibile)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Dossier dati per il tutor di efficienza")
    parser.add_argument("--project", default="leaderai", help="filtro progetto Claude (sottostringa). Vuoto = tutti.")
    parser.add_argument("--top-sample", type=int, default=3, help="quante sessioni pesanti campionare")
    parser.add_argument("--write", type=Path, default=None, help="scrivi il dossier su questo file invece che a video")
    args = parser.parse_args()

    iso = datetime.now().isocalendar()
    week = f"{iso[0]}-W{iso[1]:02d}"
    today = datetime.now().strftime("%d/%m/%Y")

    claude_txt = run_report(CLAUDE_REPORT, ["--project", args.project, "--top", "12"])
    codex_txt = run_report(CODEX_REPORT, ["--days", "7", "--top", "10"])

    # campione delle sessioni Claude piu' pesanti
    samples_md = ""
    try:
        mod = load_claude_scan()
        per_session, _, _ = mod.scan(mod.DEFAULT_PROJECTS_DIR, args.project or None)
        heavy = sorted(per_session.values(), key=lambda s: s["total"], reverse=True)[: args.top_sample]
        blocks = []
        for s in heavy:
            title = mod.session_title(s["path"])
            blocks.append(
                f"### {mod.fmt_tokens(s['total'])} token · cache_r {mod.pct(s['cache_r'], s['total'])} · "
                f"{(s['model'] or '?').replace('claude-', '')} · ultimo {s['last'] or '?'}\n"
                f"**Titolo:** {title}\n\n```\n{sample_session(s['path'])}\n```"
            )
        samples_md = "\n\n".join(blocks) if blocks else "(nessuna sessione campionabile)"
    except Exception as exc:
        samples_md = f"(errore campionamento: {exc})"

    dossier = f"""# Dossier efficienza — {week} (generato {today})

> Materiale grezzo per il tutor. NON è il consiglio: è ciò che il tutor legge per scriverlo.
> Regola di lettura: il costo sta nell'input/contesto trascinato (cache_read), non nell'output.
> Riferimento: memory/feedback_economia_contesto.md

## 1. Consumi Claude Code

```
{claude_txt}
```

## 2. Consumi Codex (ultimi 7 giorni)

```
{codex_txt}
```

## 3. Campione delle sessioni Claude più pesanti (estratto limitato)

{samples_md}
"""

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(dossier, encoding="utf-8")
        print(f"Dossier scritto in {args.write}")
    else:
        print(dossier)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
