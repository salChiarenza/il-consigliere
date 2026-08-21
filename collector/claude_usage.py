#!/usr/bin/env python3
"""Report locale sui consumi di Claude Code.

Legge le sessioni salvate da Claude Code (un file .jsonl per sessione) in
~/.claude/projects/<progetto>/ e aggrega i token consumati.

Ogni riga `assistant` del transcript porta un blocco `usage` con:
- input_tokens                -> contesto nuovo inviato in quel turno
- cache_creation_input_tokens -> contesto scritto in cache (caro come input)
- cache_read_input_tokens     -> contesto RILETTO dalla cache = "contesto trascinato"
- output_tokens               -> testo prodotto dall'agente

Il "contesto trascinato" (cache_read) e' di solito la voce piu' pesante: e' il
prezzo di chat lunghe e perimetri larghi. Vedi memory/feedback_economia_contesto.md.

Non chiama API esterne e non modifica dati: legge solo i transcript locali.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_PROJECTS_DIR = Path("~/.claude/projects").expanduser()


def fmt_tokens(value: int | float | None) -> str:
    if not value:
        return "0"
    value = int(value)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def pct(part: int, whole: int) -> str:
    if not whole:
        return "0%"
    return f"{round(100 * part / whole)}%"


def print_table(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> None:
    materialized = [tuple("" if c is None else str(c) for c in row) for row in rows]
    widths = [len(h) for h in headers]
    for row in materialized:
        widths = [max(widths[i], len(row[i])) for i in range(len(headers))]
    print("  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for row in materialized:
        print("  ".join(row[i].ljust(widths[i]) for i in range(len(headers))))


def local_date(ts: str) -> str | None:
    """ISO UTC ('...Z') -> data locale 'AAAA-MM-GG'."""
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%Y-%m-%d")
    except ValueError:
        return None


def usage_tokens(usage: dict) -> dict[str, int]:
    inp = int(usage.get("input_tokens") or 0)
    cache_w = int(usage.get("cache_creation_input_tokens") or 0)
    cache_r = int(usage.get("cache_read_input_tokens") or 0)
    out = int(usage.get("output_tokens") or 0)
    return {
        "input": inp,
        "cache_w": cache_w,
        "cache_r": cache_r,
        "output": out,
        "total": inp + cache_w + cache_r + out,
    }


def session_title(path: Path) -> str:
    """Primo messaggio umano della sessione, come titolo leggibile."""
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("type") != "user":
                    continue
                content = row.get("message", {}).get("content")
                text = None
                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text")
                            break
                if not text:
                    continue
                text = " ".join(text.split())
                # salta i blocchi iniettati dal sistema (reminder, hook)
                if text.startswith("<") or text.startswith("Caveat:"):
                    continue
                return text[:80]
    except OSError:
        pass
    return "(senza titolo)"


def scan(projects_dir: Path, project_filter: str | None):
    """Ritorna (per_session, per_day, per_model) aggregati."""
    per_session: dict[str, dict] = {}
    per_day: dict[str, dict[str, int]] = {}
    per_model: dict[str, dict[str, int]] = {}

    for jsonl in projects_dir.glob("*/*.jsonl"):
        if project_filter and project_filter not in str(jsonl.parent.name):
            continue
        sess = per_session.setdefault(
            str(jsonl),
            {"path": jsonl, "total": 0, "cache_r": 0, "output": 0,
             "last": "", "model": "?", "sidechain": 0},
        )
        try:
            fh = jsonl.open(encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("type") != "assistant":
                    continue
                msg = row.get("message", {})
                usage = msg.get("usage")
                if not usage:
                    continue
                tk = usage_tokens(usage)
                day = local_date(row.get("timestamp", ""))
                model = msg.get("model") or "?"

                sess["total"] += tk["total"]
                sess["cache_r"] += tk["cache_r"]
                sess["output"] += tk["output"]
                if row.get("isSidechain"):
                    sess["sidechain"] += tk["total"]
                if day and day > sess["last"]:
                    sess["last"] = day
                sess["model"] = model

                if day:
                    d = per_day.setdefault(day, {"total": 0, "cache_r": 0, "output": 0})
                    d["total"] += tk["total"]
                    d["cache_r"] += tk["cache_r"]
                    d["output"] += tk["output"]

                m = per_model.setdefault(model, {"total": 0, "sessions": set()})
                m["total"] += tk["total"]
                m["sessions"].add(str(jsonl))

    # togli le sessioni a zero token
    per_session = {k: v for k, v in per_session.items() if v["total"] > 0}
    return per_session, per_day, per_model


def main() -> int:
    parser = argparse.ArgumentParser(description="Report locale consumi Claude Code")
    parser.add_argument("--project", default="leaderai",
                        help="filtro sul nome cartella progetto (sottostringa). Vuoto = tutti.")
    parser.add_argument("--top", type=int, default=15, help="sessioni pesanti da mostrare")
    parser.add_argument("--projects-dir", type=Path, default=DEFAULT_PROJECTS_DIR)
    args = parser.parse_args()

    if not args.projects_dir.exists():
        raise SystemExit(f"Cartella sessioni non trovata: {args.projects_dir}")

    pfilter = args.project or None
    per_session, per_day, per_model = scan(args.projects_dir, pfilter)

    print("Report locale consumi Claude Code")
    print(f"sessioni: {args.projects_dir}")
    print(f"filtro progetto: {pfilter or '(tutti)'}")
    print("\nNota: dati locali dai transcript .jsonl, per diagnosi. Il contatore "
          "ufficiale resta il pannello Claude/Anthropic.")
    print("Nota: 'cache_r' = contesto riletto dalla cache = costo del contesto trascinato.")

    grand = sum(s["total"] for s in per_session.values())
    grand_cr = sum(s["cache_r"] for s in per_session.values())
    grand_out = sum(s["output"] for s in per_session.values())
    print(f"\nTOTALE: {fmt_tokens(grand)} token processati  |  "
          f"contesto trascinato (cache_r): {fmt_tokens(grand_cr)} ({pct(grand_cr, grand)})  |  "
          f"output: {fmt_tokens(grand_out)} ({pct(grand_out, grand)})  |  "
          f"sessioni: {len(per_session)}")

    print("\nConsumi per giorno")
    print_table(
        ("giorno", "token", "cache_r", "output"),
        ((day,
          fmt_tokens(per_day[day]["total"]),
          f'{fmt_tokens(per_day[day]["cache_r"])} ({pct(per_day[day]["cache_r"], per_day[day]["total"])})',
          fmt_tokens(per_day[day]["output"]))
         for day in sorted(per_day, reverse=True)),
    )

    print("\nPer modello")
    print_table(
        ("model", "sessioni", "token"),
        ((model, len(per_model[model]["sessions"]), fmt_tokens(per_model[model]["total"]))
         for model in sorted(per_model, key=lambda m: per_model[m]["total"], reverse=True)),
    )

    heavy = sorted(per_session.values(), key=lambda s: s["total"], reverse=True)[: args.top]
    print(f"\nTop {args.top} sessioni pesanti")
    print_table(
        ("ultimo", "token", "cache_r%", "model", "titolo"),
        ((s["last"] or "?",
          fmt_tokens(s["total"]),
          pct(s["cache_r"], s["total"]),
          (s["model"] or "?").replace("claude-", ""),
          session_title(s["path"]))
         for s in heavy),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
