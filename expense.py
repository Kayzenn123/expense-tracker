#!/usr/bin/env python3
"""expense-tracker — tiny CLI expense tracker. Pure Python (sqlite3 stdlib).

Data lives in ~/.expense.db (override with --db).

Usage:
    python expense.py add 25000 "kopi" --cat food
    python expense.py add 150000 "bensin" --cat transport --date 2026-10-09
    python expense.py list --month 2026-10
    python expense.py summary                 # this month by category
    python expense.py summary --month 2026-09
"""

import argparse
import os
import sqlite3
import sys
from datetime import date

DEFAULT_DB = os.path.expanduser("~/.expense.db")


def connect(path):
    db = sqlite3.connect(path)
    db.execute("""CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        amount INTEGER NOT NULL,
        category TEXT NOT NULL DEFAULT 'other',
        note TEXT DEFAULT '')""")
    return db


def fmt(n):
    return f"{n:,}".replace(",", ".")


def cmd_add(args):
    db = connect(args.db)
    d = args.date or date.today().isoformat()
    db.execute("INSERT INTO expenses(date, amount, category, note) VALUES (?,?,?,?)",
               (d, args.amount, args.cat, args.note or ""))
    db.commit()
    print(f"+ Rp{fmt(args.amount)}  [{args.cat}] {args.note or ''}  ({d})")


def cmd_list(args):
    db = connect(args.db)
    month = args.month or date.today().isoformat()[:7]
    rows = db.execute(
        "SELECT date, amount, category, note FROM expenses "
        "WHERE substr(date,1,7)=? ORDER BY date, id", (month,)).fetchall()
    if not rows:
        print(f"no expenses in {month}")
        return
    total = 0
    for d, amt, cat, note in rows:
        total += amt
        print(f"{d}  Rp{fmt(amt):>12}  [{cat:<10}] {note}")
    print(f"{'-'*40}\nTOTAL Rp{fmt(total)}")


def cmd_summary(args):
    db = connect(args.db)
    month = args.month or date.today().isoformat()[:7]
    rows = db.execute(
        "SELECT category, SUM(amount), COUNT(*) FROM expenses "
        "WHERE substr(date,1,7)=? GROUP BY category ORDER BY 2 DESC",
        (month,)).fetchall()
    if not rows:
        print(f"no expenses in {month}")
        return
    total = sum(r[1] for r in rows)
    print(f"Summary {month} — total Rp{fmt(total)}\n")
    for cat, amt, n in rows:
        pct = 100 * amt / total if total else 0
        bar = "#" * int(pct / 5)
        print(f"{cat:<12} Rp{fmt(amt):>12}  {n:>3}x  {pct:4.1f}% {bar}")


def main():
    ap = argparse.ArgumentParser(description="expense-tracker — tiny CLI")
    ap.add_argument("--db", default=DEFAULT_DB)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add")
    p.add_argument("amount", type=int)
    p.add_argument("note", nargs="?", default="")
    p.add_argument("--cat", default="other")
    p.add_argument("--date")

    p = sub.add_parser("list")
    p.add_argument("--month")

    p = sub.add_parser("summary")
    p.add_argument("--month")

    args = ap.parse_args()
    {"add": cmd_add, "list": cmd_list, "summary": cmd_summary}[args.cmd](args)


if __name__ == "__main__":
    main()
