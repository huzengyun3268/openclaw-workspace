# -*- coding: utf-8 -*-
import pandas as pd
import re

# Read Excel file
df = pd.read_excel('5.xlsx', sheet_name=0, header=None)

# Find data rows (skip headers and sub-totals)
data_rows = []
for i in range(len(df)):
    row = df.iloc[i]
    # Check if first column has a number (item number)
    val = str(row[0]).strip() if pd.notna(row[0]) else ''
    if val and val[0].isdigit() and '小计' not in val and '合计' not in val:
        try:
            item = {
                '序号': int(val),
                '项目编码': str(row[1]) if pd.notna(row[1]) else '',
                '项目名称': str(row[2]) if pd.notna(row[2]) else '',
                '项目特征': str(row[3]) if pd.notna(row[3]) else '',
                '单位': str(row[4]) if pd.notna(row[4]) else '',
                '工程量': float(row[5]) if pd.notna(row[5]) and str(row[5]).replace('.','').isdigit() else 0,
                '综合单价': float(row[6]) if pd.notna(row[6]) and str(row[6]).replace('.','').replace('-','').isdigit() else 0,
                '合价': float(row[7]) if pd.notna(row[7]) and str(row[7]).replace('.','').replace('-','').isdigit() else 0,
            }
            data_rows.append(item)
        except:
            pass

# Create DataFrame
items_df = pd.DataFrame(data_rows)

print("=" * 60)
print("台州府城集散中心 - 土建工程清单汇总")
print("=" * 60)

print(f"\n总清单项目数: {len(items_df)}")

# Calculate totals
total_amount = items_df['合价'].sum()
total_quantity = items_df['工程量'].sum()

print(f"\n工程量合计: {total_quantity:,.2f}")
print(f"清单合价合计: {total_amount:,.2f} 元")

# Group by project name (first few characters)
items_df['类别'] = items_df['项目名称'].str[:6]
category_summary = items_df.groupby('类别').agg({
    '工程量': 'sum',
    '合价': 'sum',
    '序号': 'count'
}).rename(columns={'序号': '项目数'})

print("\n" + "=" * 60)
print("按类别汇总")
print("=" * 60)
print(category_summary.sort_values('合价', ascending=False).head(20).to_string())

# Top 20 expensive items
print("\n" + "=" * 60)
print("前20大金额项目")
print("=" * 60)
top_items = items_df.nlargest(20, '合价')[['项目名称', '单位', '工程量', '综合单价', '合价']]
print(top_items.to_string(index=False))

# Save to file
items_df.to_excel('清单汇总.xlsx', index=False)
print("\n已保存: 清单汇总.xlsx")
