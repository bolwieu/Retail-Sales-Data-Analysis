"""Load cleaned data into SQLite and execute the portfolio SQL queries."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'outputs' / 'cleaned_sales.csv'
if not source.exists():
    raise SystemExit('Run python scripts/analyze.py first.')
with sqlite3.connect(ROOT / 'outputs' / 'retail_sales.sqlite') as con:
    pd.read_csv(source).to_sql('sales', con, if_exists='replace', index=False)
    statements = (ROOT / 'sql' / 'business_questions.sql').read_text().split(';')
    for i, statement in enumerate(statements, 1):
        # Remove SQL comment lines before checking if the statement is executable.
        sql = '\n'.join(line for line in statement.splitlines() if not line.strip().startswith('--')).strip()
        if sql:
            result = pd.read_sql_query(sql, con)
            result.to_csv(ROOT / 'outputs' / f'sql_question_{i}.csv', index=False)
            print(f'Question {i}: {len(result)} rows')
print('SQL reports generated.')
