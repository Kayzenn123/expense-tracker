# expense-tracker

Tiny CLI expense tracker. Pure Python, sqlite3 only — no dependencies.

## Usage

```bash
# add an expense (today)
python expense.py add 25000 "kopi" --cat food

# add with custom category and date
python expense.py add 150000 "bensin" --cat transport --date 2026-10-09

# list this month
python expense.py list --month 2026-10

# summary by category with bar chart
python expense.py summary
python expense.py summary --month 2026-09
```

## Output

```
Summary 2026-10 — total Rp175.000

transport    Rp     150.000    1x  85.7% #################
food         Rp      25.000    1x  14.3% ##
```

Data lives in `~/.expense.db` (override with `--db path`).
