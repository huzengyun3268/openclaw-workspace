# -*- coding: utf-8 -*-
import pandas as pd

# Read Excel file with proper encoding
try:
    # Read without header first to see raw data
    df = pd.read_excel('5.xlsx', sheet_name=0, header=None)
    print(f"Shape: {df.shape}")
    
    # Print first few rows
    print("\n=== First 10 rows ===")
    for i in range(min(10, len(df))):
        print(f"\nRow {i}:")
        for j in range(min(11, len(df.columns))):
            val = df.iloc[i, j]
            if pd.notna(val):
                print(f"  Col {j}: {str(val)[:80]}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
