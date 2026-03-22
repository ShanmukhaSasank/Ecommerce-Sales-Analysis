"""
================================================
E-Commerce Sales Performance Analysis
================================================
Author  : Shanmukha Sasank Nandula
Dataset : ecommerce_sales.csv (50,000 rows)
Tools   : Python, Pandas, NumPy, Matplotlib, Seaborn
GitHub  : github.com/ShanmukhaSasank
================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "ecommerce_sales.csv"
OUT  = BASE / "python" / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# ── Plot Style ─────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0f1117',
    'axes.facecolor':   '#1a1d2e',
    'axes.edgecolor':   '#2d3155',
    'axes.labelcolor':  '#c8cce0',
    'xtick.color':      '#8b90b5',
    'ytick.color':      '#8b90b5',
    'text.color':       '#e0e3f5',
    'grid.color':       '#2d3155',
    'grid.linestyle':   '--',
    'grid.alpha':       0.5,
    'font.family':      'DejaVu Sans',
    'font.size':        11,
})
PALETTE = ['#3b82f6','#8b5cf6','#10b981','#f59e0b',
           '#ef4444','#ec4899','#06b6d4']

# ══════════════════════════════════════════════════════════════
# 1. LOAD & VALIDATE DATA
# ══════════════════════════════════════════════════════════════
print("=" * 60)
print("  E-COMMERCE SALES PERFORMANCE — EDA")
print("=" * 60)

df = pd.read_csv(DATA, parse_dates=['order_date'])

# Feature Engineering
df['year']       = df['order_date'].dt.year
df['month']      = df['order_date'].dt.month
df['month_name'] = df['order_date'].dt.strftime('%b')
df['quarter']    = 'Q' + df['order_date'].dt.quarter.astype(str)
df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
df['discount_band'] = pd.cut(
    df['discount_pct'],
    bins=[-0.01, 0, 0.10, 0.20, 0.30, 1],
    labels=['No Discount', '1-10%', '11-20%', '21-30%', '30%+']
)

print(f"\n✓ Rows loaded    : {len(df):,}")
print(f"✓ Columns        : {df.shape[1]}")
print(f"✓ Date range     : {df['order_date'].min().date()} → {df['order_date'].max().date()}")
print(f"✓ Unique customers: {df['customer_id'].nunique():,}")
print(f"✓ Unique products : {df['product_id'].nunique():,}")

# Data Quality
print("\n[DATA QUALITY]")
nulls = df.isnull().sum()
nulls = nulls[nulls > 0]
print(f"Nulls per column:\n{nulls}")
print(f"Duplicate orders : {df['order_id'].duplicated().sum()}")
print(f"Negative revenue : {(df['revenue'] < 0).sum()}")

# ══════════════════════════════════════════════════════════════
# 2. HEADLINE KPIs
# ══════════════════════════════════════════════════════════════
print("\n[HEADLINE KPIs]")
print("-" * 45)

total_rev    = df['revenue'].sum()
total_profit = df['profit'].sum()
total_orders = len(df)
aov          = df['revenue'].mean()
margin       = total_profit / total_rev * 100
return_rate  = df['is_returned'].mean() * 100
avg_rating   = df['rating'].dropna().mean()

print(f"Total Revenue    : ₹{total_rev:>18,.2f}")
print(f"Total Profit     : ₹{total_profit:>18,.2f}")
print(f"Profit Margin    :  {margin:>16.2f}%")
print(f"Total Orders     :  {total_orders:>16,}")
print(f"Avg Order Value  : ₹{aov:>18,.2f}")
print(f"Return Rate      :  {return_rate:>16.2f}%")
print(f"Avg Rating       :  {avg_rating:>16.2f} / 5.0")

# ══════════════════════════════════════════════════════════════
# 3. CATEGORY ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n[CATEGORY ANALYSIS]")
print("-" * 45)

cat = (df.groupby('category')
         .agg(revenue=('revenue','sum'),
              profit=('profit','sum'),
              orders=('order_id','count'),
              avg_order=('revenue','mean'))
         .assign(margin=lambda x: x['profit']/x['revenue']*100,
                 share=lambda x: x['revenue']/total_rev*100)
         .sort_values('revenue', ascending=False))

print(cat[['revenue','profit','orders','margin','share']].round(2).to_string())
print(f"\n★ Top 3 Categories: {', '.join(cat.head(3).index.tolist())}")
cat.reset_index().to_csv(OUT / 'summary_category.csv', index=False)

# ══════════════════════════════════════════════════════════════
# 4. SEASONAL TREND ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n[SEASONAL TREND]")
print("-" * 45)

monthly = (df.groupby(['year','month'])['revenue']
             .sum().reset_index()
             .sort_values(['year','month']))

monthly_avg  = df.groupby('month')['revenue'].sum() / df['year'].nunique()
peak_month   = monthly_avg.idxmax()
trough_month = monthly_avg.idxmin()
spike_pct    = (monthly_avg[peak_month] - monthly_avg[trough_month]) / monthly_avg[trough_month] * 100

print(f"Peak Month   : Month {peak_month}  (₹{monthly_avg[peak_month]:,.0f} avg)")
print(f"Trough Month : Month {trough_month}  (₹{monthly_avg[trough_month]:,.0f} avg)")
print(f"Seasonal Spike: {spike_pct:.1f}%")

monthly_total = df.groupby('year_month')['revenue'].sum().reset_index()
monthly_total.to_csv(OUT / 'summary_monthly.csv', index=False)

# ══════════════════════════════════════════════════════════════
# 5. REGIONAL ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n[REGIONAL ANALYSIS]")
print("-" * 45)

region = (df.groupby('region')
            .agg(revenue=('revenue','sum'),
                 profit=('profit','sum'),
                 orders=('order_id','count'),
                 avg_order=('revenue','mean'))
            .assign(margin=lambda x: x['profit']/x['revenue']*100)
            .sort_values('revenue', ascending=False))

print(region.round(2).to_string())
region.reset_index().to_csv(OUT / 'summary_region.csv', index=False)

# ══════════════════════════════════════════════════════════════
# 6. CHANNEL ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n[CHANNEL ANALYSIS]")
print("-" * 45)

channel = (df.groupby('channel')
             .agg(revenue=('revenue','sum'),
                  orders=('order_id','count'),
                  avg_order=('revenue','mean'))
             .sort_values('revenue', ascending=False))

print(channel.round(2).to_string())
channel.reset_index().to_csv(OUT / 'summary_channel.csv', index=False)

# ══════════════════════════════════════════════════════════════
# 7. CUSTOMER SEGMENT ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n[CUSTOMER SEGMENT ANALYSIS]")
print("-" * 45)

segment = (df.groupby('customer_segment')
             .agg(revenue=('revenue','sum'),
                  orders=('order_id','count'),
                  avg_order=('revenue','mean'),
                  return_rate=('is_returned','mean'))
             .assign(return_rate=lambda x: x['return_rate']*100)
             .sort_values('revenue', ascending=False))

print(segment.round(2).to_string())
segment.reset_index().to_csv(OUT / 'summary_segment.csv', index=False)

# ══════════════════════════════════════════════════════════════
# 8. DISCOUNT IMPACT ANALYSIS
# ══════════════════════════════════════════════════════════════
print("\n[DISCOUNT IMPACT]")
print("-" * 45)

discount = (df.groupby('discount_band', observed=True)
              .agg(orders=('order_id','count'),
                   revenue=('revenue','sum'),
                   profit=('profit','sum'))
              .assign(margin=lambda x: x['profit']/x['revenue']*100))

print(discount.round(2).to_string())
discount.reset_index().to_csv(OUT / 'summary_discount.csv', index=False)

# ══════════════════════════════════════════════════════════════
# 9. VISUALISATIONS
# ══════════════════════════════════════════════════════════════
print("\n[GENERATING CHARTS]")

def save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  ✓ {name}")

# Chart 1 — Revenue by Category
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(cat.index[::-1], cat['revenue'][::-1]/1e6,
               color=PALETTE[:len(cat)], height=0.6)
for bar, val in zip(bars, cat['revenue'][::-1]/1e6):
    ax.text(val+0.5, bar.get_y()+bar.get_height()/2,
            f'₹{val:.1f}M', va='center', fontsize=10)
ax.set_xlabel('Revenue (₹ Millions)')
ax.set_title('Revenue by Category', fontsize=14, fontweight='bold', pad=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f'₹{x:.0f}M'))
ax.grid(axis='x')
plt.tight_layout()
save(fig, 'fig1_revenue_by_category.png')

# Chart 2 — Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(14, 5))
x = range(len(monthly_total))
ax.fill_between(x, monthly_total['revenue']/1e6, alpha=0.2, color='#3b82f6')
ax.plot(x, monthly_total['revenue']/1e6, color='#3b82f6',
        linewidth=2.5, marker='o', markersize=4)
ax.set_xticks(list(x))
ax.set_xticklabels(monthly_total['year_month'], rotation=45, ha='right', fontsize=8)
ax.set_ylabel('Revenue (₹ Millions)')
ax.set_title('Monthly Revenue Trend (2023–2024)', fontsize=14, fontweight='bold', pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}M'))
ax.grid(axis='y')
plt.tight_layout()
save(fig, 'fig2_monthly_trend.png')

# Chart 3 — Regional Revenue Donut
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(region['revenue'], labels=region.index,
       autopct='%1.1f%%', colors=PALETTE, startangle=90,
       wedgeprops=dict(width=0.55, edgecolor='#0f1117', linewidth=2),
       pctdistance=0.78, textprops={'color':'#e0e3f5','fontsize':11})
ax.set_title('Revenue Share by Region', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
save(fig, 'fig3_region_donut.png')

# Chart 4 — Discount Band vs Margin
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#10b981' if m > 35 else '#f59e0b' for m in discount['margin']]
bars = ax.bar(discount.index.astype(str), discount['margin'],
              color=colors, width=0.5)
for bar, val in zip(bars, discount['margin']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
            f'{val:.1f}%', ha='center', fontsize=10)
ax.set_ylabel('Profit Margin (%)')
ax.set_title('Profit Margin by Discount Band', fontsize=14, fontweight='bold', pad=12)
ax.set_ylim(0, discount['margin'].max()*1.2)
ax.grid(axis='y')
plt.tight_layout()
save(fig, 'fig4_discount_margin.png')

# Chart 5 — Channel Revenue
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(channel.index, channel['revenue']/1e6,
              color=PALETTE[:len(channel)], width=0.5)
for bar, val in zip(bars, channel['revenue']/1e6):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
            f'₹{val:.1f}M', ha='center', fontsize=10)
ax.set_ylabel('Revenue (₹ Millions)')
ax.set_title('Revenue by Sales Channel', fontsize=14, fontweight='bold', pad=12)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'₹{v:.0f}M'))
ax.grid(axis='y')
plt.tight_layout()
save(fig, 'fig5_channel_revenue.png')

# Chart 6 — Customer Segment Revenue
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(segment.index, segment['revenue']/1e6,
              color=['#3b82f6','#10b981','#8b5cf6','#f59e0b'], width=0.5)
for bar, val in zip(bars, segment['revenue']/1e6):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
            f'₹{val:.1f}M', ha='center', fontsize=10)
ax.set_ylabel('Revenue (₹ Millions)')
ax.set_title('Revenue by Customer Segment', fontsize=14, fontweight='bold', pad=12)
ax.grid(axis='y')
plt.tight_layout()
save(fig, 'fig6_segment_revenue.png')

# Chart 7 — Category Margin Comparison
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(cat.index, cat['margin'],
              color='#8b5cf6', width=0.5)
for bar, val in zip(bars, cat['margin']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f'{val:.1f}%', ha='center', fontsize=10)
ax.set_ylabel('Profit Margin (%)')
ax.set_title('Profit Margin by Category', fontsize=14, fontweight='bold', pad=12)
ax.set_ylim(0, cat['margin'].max()*1.2)
ax.grid(axis='y')
plt.tight_layout()
save(fig, 'fig7_category_margin.png')

print("\n✓ All charts saved to python/outputs/")
print("\n" + "=" * 60)
print("  ANALYSIS COMPLETE")
print("=" * 60)
