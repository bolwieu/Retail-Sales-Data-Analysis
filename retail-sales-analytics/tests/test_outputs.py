"""Lightweight validation checks; run after the analysis pipeline."""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / 'outputs' / 'cleaned_sales.csv')
assert len(df) == 3000
assert df['order_id'].is_unique
assert not df.isna().any().any()
assert np.allclose(df['revenue'], df['quantity'] * df['unit_price'] * (1 - df['discount_pct']))
assert np.allclose(df['profit'], df['revenue'] - df['quantity'] * df['unit_cost'])
monthly = pd.read_csv(ROOT / 'outputs' / 'monthly_summary.csv')
assert np.isclose(monthly['revenue'].sum(), df['revenue'].sum())
print('All data quality and reconciliation checks passed.')
