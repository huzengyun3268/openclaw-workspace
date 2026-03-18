# -*- coding: utf-8 -*-
import pandas as pd

# Read Excel
df = pd.read_excel('5.xlsx', sheet_name=0, header=None)

# Print some raw data to understand structure
print("=== 检查原始数据 ===")
for i in range(10):
    print(f"\nRow {i}:")
    for j in range(11):
        val = df.iloc[i, j]
        if pd.notna(val):
            print(f"  Col{j}: {str(val)[:50]}")
