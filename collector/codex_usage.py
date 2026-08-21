#!/usr/bin/env python3
"""Report locale sui consumi Codex.

Legge i database locali di Codex:
- ~/.codex/state_5.sqlite: token per thread
- ~/.codex/logs_2.sqlite: eventi/byte per fascia oraria

Non chiama API esterne e non modifica dati.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from typing import Iterable, Sequence


DEFAULT_STATE_DB = Path("~/.codex/state_5.sqlite").expanduser()
DEFAULT_LOGS_DB = Path("~/.codex/logs_2.sqlite").expanduser()


def connect_readonly(path: Path) -> sqlite3.Connection:
    uri = f"file:{path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def fetch_all(db: Path, query: str, params: Sequence[object] = ()) -> list[tuple]:
    with connect_readonly(db) as conn:
        return conn.execute(query, params).fetchall()


def fmt_tokens(value: int | float | None) -> str:
    if value is None:
        return "0"
    value = int(value)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def fmt_mb(value: int | float | None) -> str:
    if value is None:
        return "0.00"
    return f"{float(value):.2f}"


def print_table(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> None:
    materialized = [tuple("" if c is None else str(c) for c in row) for row in rows]
    widths = [len(h) for h in headers]
    for row in materialized:
        widths = [max(widths[i], len(row[i])) for i in range(len(headers))]

    line = "  ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    print(line)
    print("  ".join("-" * widths[i] for i in range(len(headers))))
    for row in materialized:
        print("  ".join(row[i].ljust(widths[i]) for i in range(len(headers))))


def require_db(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"Database {label} non trovato: {path}")


def daily_report(state_db: Path, days: int) -> None:
    rows = fetch_all(
        state_db,
        """
        select
          date(updated_at, 'unixepoch', 'localtime') as giorno,
          count(*) as thread,
          sum(tokens_used) as tokens
        from threads
        where tokens_used > 0
          and updated_at >= strftime('%s', 'now', ?)
        group by giorno
        order by giorno desc
        """,
        (f"-{days} days",),
    )
    print(f"\nConsumi per giorno - ultimi {days} giorni")
    print_table(
        ("giorno", "thread", "token"),
        ((day, threads, fmt_tokens(tokens)) for day, threads, tokens in rows),
    )


def hourly_today_report(state_db: Path, logs_db: Path) -> None:
    token_rows = fetch_all(
        state_db,
        """
        select
          strftime('%Y-%m-%d %H:00', updated_at, 'unixepoch', 'localtime') as ora,
          count(*) as thread,
          sum(tokens_used) as tokens
        from threads
        where tokens_used > 0
          and updated_at >= strftime('%s', 'now', 'start of day')
        group by ora
        order by ora
        """,
    )
    log_rows = fetch_all(
        logs_db,
        """
        select
          strftime('%Y-%m-%d %H:00', ts, 'unixepoch', 'localtime') as ora,
          count(*) as eventi,
          round(sum(estimated_bytes) / 1024.0 / 1024.0, 2) as mb
        from logs
        where ts >= strftime('%s', 'now', 'start of day')
        group by ora
        order by ora
        """,
    )
    by_hour: dict[str, dict[str, object]] = {}
    for hour, threads, tokens in token_rows:
        by_hour.setdefault(hour, {})["thread"] = threads
        by_hour.setdefault(hour, {})["tokens"] = tokens
    for hour, events, mb in log_rows:
        by_hour.setdefault(hour, {})["events"] = events
        by_hour.setdefault(hour, {})["mb"] = mb

    print("\nOggi per ora")
    print_table(
        ("ora", "thread aggiornati", "token thread", "eventi log", "MB log"),
        (
            (
                hour,
                by_hour[hour].get("thread", 0),
                fmt_tokens(by_hour[hour].get("tokens", 0)),
                by_hour[hour].get("events", 0),
                fmt_mb(by_hour[hour].get("mb", 0)),
            )
            for hour in sorted(by_hour)
        ),
    )


def model_report(state_db: Path, days: int) -> None:
    rows = fetch_all(
        state_db,
        """
        select
          coalesce(model, '?') as model,
          coalesce(reasoning_effort, '?') as effort,
          count(*) as thread,
          sum(tokens_used) as tokens
        from threads
        where tokens_used > 0
          and updated_at >= strftime('%s', 'now', ?)
        group by model, effort
        order by tokens desc
        """,
        (f"-{days} days",),
    )
    print(f"\nModello / reasoning - ultimi {days} giorni")
    print_table(
        ("model", "effort", "thread", "token"),
        ((model, effort, threads, fmt_tokens(tokens)) for model, effort, threads, tokens in rows),
    )


def top_threads_report(state_db: Path, days: int, limit: int) -> None:
    rows = fetch_all(
        state_db,
        """
        select
          datetime(updated_at, 'unixepoch', 'localtime') as updated,
          tokens_used,
          coalesce(model, '?') as model,
          coalesce(reasoning_effort, '?') as effort,
          replace(substr(title, 1, 90), char(10), ' ') as title
        from threads
        where tokens_used > 0
          and updated_at >= strftime('%s', 'now', ?)
        order by tokens_used desc
        limit ?
        """,
        (f"-{days} days", limit),
    )
    print(f"\nTop thread pesanti - ultimi {days} giorni")
    print_table(
        ("updated", "token", "model", "effort", "title"),
        ((updated, fmt_tokens(tokens), model, effort, title) for updated, tokens, model, effort, title in rows),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Report locale consumi Codex")
    parser.add_argument("--days", type=int, default=14, help="giorni da includere nei report principali")
    parser.add_argument("--top", type=int, default=15, help="numero di thread pesanti da mostrare")
    parser.add_argument("--state-db", type=Path, default=DEFAULT_STATE_DB, help="path state_5.sqlite")
    parser.add_argument("--logs-db", type=Path, default=DEFAULT_LOGS_DB, help="path logs_2.sqlite")
    args = parser.parse_args()

    require_db(args.state_db, "state")
    require_db(args.logs_db, "logs")

    print("Report locale consumi Codex")
    print(f"state: {args.state_db}")
    print(f"logs:  {args.logs_db}")
    print("\nNota: questi sono dati locali per diagnosi. Il contatore ufficiale resta Codex/OpenAI Usage.")
    print("Nota: i token per ora sono attribuiti all'ora di aggiornamento del thread, non al singolo turno.")

    daily_report(args.state_db, args.days)
    hourly_today_report(args.state_db, args.logs_db)
    model_report(args.state_db, args.days)
    top_threads_report(args.state_db, args.days, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
