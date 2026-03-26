### code for the Figures : code written by ABDULKHALIK ALSOUFI

import pandas as pd
import matplotlib.pyplot as plt

df_gpcrs= pd.read_csv(r'c:\Users\abdul\OneDrive\Desktop\vscode\GPCRdb_structures (1) (1).csv', skiprows=1)
df_gpcrs.columns = df_gpcrs.columns.str.strip()
for col in df_gpcrs.select_dtypes(include='object').columns:
    df_gpcrs[col] = df_gpcrs[col].str.strip()
df_gpcrs.dropna(how='all', inplace=True)

counts2 = df_gpcrs['State'].value_counts()
total2 = len(df_gpcrs)

print(f"Total GPCR structures in template set: {total2}")
print(f"\nState distribution:")
for state, i in counts2.items():
    print(f"  {state}: {i} ({i/total2*100:.1f}%)")


active = counts2.get('Active', 0)
intermediate = counts2.get('Intermediate', 0)
inactive = counts2.get('Inactive', 0)

print(f"\n{'='*50}")
print(f"Active-state:       {active}  ({active/total2*100:.1f}%)")
print(f"Inactive-state:     {inactive}  ({inactive/total2*100:.1f}%)")
if intermediate > 0:
    print(f"Intermediate:       {intermediate}  ({intermediate/total2*100:.1f}%)")
print(f"Total:              {total2}")
print(f"{'='*50}")


labels = list(counts2.index)
values = list(counts2.values)
percentages = [v / total2 * 100 for v in values]
color_map = {'Active': '#2ecc71', 'Inactive': '#e74c3c', 'Intermediate': '#f39c12'}
colors = [color_map.get(l, '#95a5a6') for l in labels]

fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='black', linewidth=0.8)

for bar, val, pct in zip(bars, values, percentages):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'{val} ({pct:.1f}%)', ha='center', va='bottom', fontsize=13, fontweight='bold')

ax.set_ylabel('Number of Structures', fontsize=12)
ax.set_title('GPCRdb Template Set — Structure States', fontsize=14, fontweight='bold')
ax.set_ylim(0, max(values) * 1.15)
plt.tight_layout()
plt.show()