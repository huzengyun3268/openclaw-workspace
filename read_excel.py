# -*- coding: utf-8 -*-
import pandas as pd

# Read Excel file
try:
    # Try to read all sheets
    excel_file = pd.ExcelFile('5.xlsx')
    print("=== Sheets ===")
    print(excel_file.sheet_names)
    
    # Read first sheet
    df = pd.read_excel('5.xlsx', sheet_name=0)
    print(f"\n=== First Sheet: {excel_file.sheet_names[0]} ===")
    print(f"Shape: {df.shape}")
    print("\n=== Columns ===")
    print(df.columns.tolist())
    print("\n=== First 20 rows ===")
    print(df.head(20).to_string())
    
except Exception as e:
    print(f"Error: {e}")
