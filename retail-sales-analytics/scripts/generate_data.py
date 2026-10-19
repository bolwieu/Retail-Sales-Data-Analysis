"""Generate deterministic synthetic retail transaction data."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(42)
N = 3000
categories = {'Electronics': [('Headphones', 85, 48), ('Keyboard', 65, 32), ('Monitor', 230, 150)], 'Home': [('Lamp', 45, 20), ('Chair', 140, 83), ('Storage Box', 28, 12)], 'Clothing': [('Jacket', 95, 49), ('T-Shirt', 26, 10), ('Jeans', 62, 29)], 'Beauty': [('Skincare Set', 55, 23), ('Perfume', 78, 36), ('Lip Balm', 12, 4)]}
records = []
for i in range(N):
    category = RNG.choice(list(categories), p=[.32, .25, .28, .15])
    product, price, cost = categories[category][RNG.integers(3)]
    quantity = int(RNG.choice([1, 2, 3, 4], p=[.55, .28, .12, .05]))
    discount = float(RNG.choice([0, .05, .1, .2], p=[.55, .2, .2, .05]))
    date = pd.Timestamp('2025-01-01') + pd.Timedelta(days=int(RNG.integers(365)))
    records.append({'order_id': f'ORD-{i+1:05d}', 'order_date': date.date().isoformat(), 'customer_id': f'C{int(RNG.integers(1, 601)):04d}', 'region': RNG.choice(['North', 'South', 'East', 'West']), 'category': category, 'product': product, 'quantity': quantity, 'unit_price': price, 'unit_cost': cost, 'discount_pct': discount, 'payment_method': RNG.choice(['Card', 'Digital Wallet', 'Cash'], p=[.6, .3, .1])})
ROOT.joinpath('data').mkdir(exist_ok=True)
pd.DataFrame(records).to_csv(ROOT / 'data' / 'retail_sales.csv', index=False)
print(f'Generated {N} synthetic transactions')
