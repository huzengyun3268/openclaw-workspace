# -*- coding: utf-8 -*-
import pandas as pd

# Read Excel - skip header rows
df = pd.read_excel('5.xlsx', sheet_name=0, header=None)

# Find actual data rows - check col6 and col7 (price columns)
print("=== 检查价格列 ===")
for i in range(5, 20):
    row = df.iloc[i]
    col0 = str(row[0]).strip() if pd.notna(row[0]) else ''
    if col0.isdigit():
        col5 = row[5]  # 工程量
        col6 = row[6]  # 综合单价
        col7 = row[7]  # 合价
        print(f"Row {i}: 序号={col0}, 工程量={col5}, 单价={col6}, 合价={col7}")
