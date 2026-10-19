"""Validate, analyze and visualize retail sales data."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)
df = pd.read_csv(ROOT / 'data' / 'retail_sales.csv', parse_dates=['order_date'])
required = ['order_id','order_date','customer_id','region','category','product','quantity','unit_price','unit_cost','discount_pct']
assert not df[required].isna().any().any(), 'Missing required values'
assert df.order_id.is_unique, 'Duplicate orders'
assert (df.quantity > 0).all() and (df.unit_price >= 0).all() and (df.unit_cost >= 0).all()
assert df.discount_pct.between(0, 1).all()
df['revenue'] = df.quantity * df.unit_price * (1 - df.discount_pct)
df['cost'] = df.quantity * df.unit_cost
df['profit'] = df.revenue - df.cost
df['month'] = df.order_date.dt.to_period('M').astype(str)
df.to_csv(OUT / 'cleaned_sales.csv', index=False)
monthly = df.groupby('month', as_index=False).agg(revenue=('revenue','sum'), profit=('profit','sum'), orders=('order_id','nunique'))
category = df.groupby('category', as_index=False).agg(revenue=('revenue','sum'), profit=('profit','sum'), orders=('order_id','nunique')).sort_values('revenue', ascending=False)
region = df.groupby('region', as_index=False).agg(revenue=('revenue','sum'), profit=('profit','sum')).sort_values('revenue', ascending=False)
customers = df.groupby('customer_id', as_index=False).agg(total_spend=('revenue','sum'), orders=('order_id','nunique'))
customers['segment'] = pd.cut(customers.total_spend, bins=[-1, 200, 500, float('inf')], labels=['Low', 'Medium', 'High'])
for name, frame in [('monthly_summary',monthly),('category_summary',category),('region_summary',region),('customer_summary',customers)]:
    frame.to_csv(OUT / f'{name}.csv', index=False)
sns.set_theme(style='whitegrid')
fig, ax = plt.subplots(figsize=(11, 5))
sns.lineplot(data=monthly, x='month', y='revenue', marker='o', ax=ax)
ax.set(title='Monthly Revenue — Synthetic Retail Data', xlabel='Month', ylabel='Revenue ($)')
plt.xticks(rotation=45)
fig.tight_layout(); fig.savefig(OUT / 'monthly_revenue.png', dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(category['category'], category['revenue'])
ax.set(title='Revenue by Product Category', xlabel='Category', ylabel='Revenue ($)')
fig.tight_layout(); fig.savefig(OUT / 'category_revenue.png', dpi=160); plt.close(fig)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(region['region'], region['profit'])
ax.set(title='Profit by Region', xlabel='Region', ylabel='Profit ($)')
fig.tight_layout(); fig.savefig(OUT / 'region_profit.png', dpi=160); plt.close(fig)
summary = f'''# Analysis Results (Synthetic Data)\n\n- Transactions: {len(df):,}\n- Unique customers: {df.customer_id.nunique():,}\n- Total revenue: ${df.revenue.sum():,.2f}\n- Total profit: ${df.profit.sum():,.2f}\n- Profit margin: {100*df.profit.sum()/df.revenue.sum():.2f}%\n- Average order value: ${df.revenue.sum()/df.order_id.nunique():,.2f}\n- Highest-revenue category: {category.iloc[0].category}\n- Highest-profit region: {region.sort_values('profit', ascending=False).iloc[0].region}\n\nThese findings are descriptive, not causal. The dataset is generated for demonstration, not real business decisions.\n'''
(OUT / 'findings.md').write_text(summary)
print(summary)
