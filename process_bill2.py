# -*- coding: utf-8 -*-
import pandas as pd

# Read Excel - skip first few rows as header
df = pd.read_excel('5.xlsx', sheet_name=0, header=None)

# Find actual data rows
items = []
for i in range(len(df)):
    row = df.iloc[i]
    # Check first column for item number (1, 2, 3...)
    col0 = str(row[0]).strip() if pd.notna(row[0]) else ''
    if col0.isdigit():
        try:
            # Get all columns
            code = str(row[1]) if pd.notna(row[1]) else ''
            name = str(row[2]) if pd.notna(row[2]) else ''
            unit = str(row[4]) if pd.notna(row[4]) else ''
            
            # Try to get numeric values
            try:
                qty = float(row[5]) if pd.notna(row[5]) else 0
            except:
                qty = 0
                
            try:
                price = float(row[6]) if pd.notna(row[6]) else 0
            except:
                price = 0
                
            try:
                total = float(row[7]) if pd.notna(row[7]) else 0
            except:
                total = 0
            
            if name:  # Only add if has name
                items.append({
                    '序号': int(col0),
                    '项目编码': code,
                    '项目名称': name[:50],  # Limit length
                    '单位': unit,
                    '工程量': qty,
                    '综合单价': price,
                    '合价': total
                })
        except Exception as e:
            pass

df_items = pd.DataFrame(items)

print("=" * 70)
print("台州府城集散中心 - 土建工程清单")
print("=" * 70)
print(f"总清单项目数: {len(df_items)}")

# Calculate totals
total_qty = df_items['工程量'].sum()
total_price = (df_items['工程量'] * df_items['综合单价']).sum()
total_amount = df_items['合价'].sum()

print(f"\n工程量总计: {total_qty:,.2f}")
print(f"计算总价: {total_price:,.2f} 元")
print(f"清单合价: {total_amount:,.2f} 元")

# Extract categories
def get_category(name):
    if '柱' in name:
        return '柱'
    elif '梁' in name:
        return '梁'
    elif '板' in name:
        return '板'
    elif '墙' in name:
        return '墙'
    elif '基础' in name:
        return '基础'
    elif '砌' in name:
        return '砌体'
    elif '钢筋' in name:
        return '钢筋'
    elif '混凝土' in name:
        return '混凝土'
    else:
        return '其他'

df_items['类别'] = df_items['项目名称'].apply(get_category)

# Category summary
print("\n" + "=" * 70)
print("按类别工程量汇总")
print("=" * 70)
cat_sum = df_items.groupby('类别').agg({
    '工程量': 'sum',
    '合价': 'sum',
    '序号': 'count'
}).rename(columns={'序号': '项数'})
cat_sum = cat_sum.sort_values('合价', ascending=False)
print(cat_sum.to_string())

# Top items
print("\n" + "=" * 70)
print("前20项清单")
print("=" * 70)
top = df_items.nlargest(20, '合价')[['序号', '项目名称', '单位', '工程量', '综合单价', '合价']]
for _, r in top.iterrows():
    print(f"{r['序号']:3d}. {r['项目名称'][:20]:20s} {r['单位']:6s} {r['工程量']:12,.2f} {r['综合单价']:10,.2f} {r['合价']:15,.2f}")

# Save
df_items.to_excel('清单汇总.xlsx', index=False)
print("\n✓ 已保存: 清单汇总.xlsx")
