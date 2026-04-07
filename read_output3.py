# -*- coding: utf-8 -*-
import sys
import os

os.chdir(r'C:\Users\Administrator\.openclaw\workspace')

files = ['morning_report_out.txt', 'short_trade_out.txt', 'short2.txt']

for fname in files:
    if not os.path.exists(fname):
        print(f"{fname}: NOT FOUND")
        continue
    with open(fname, 'rb') as f:
        raw = f.read()
    text = raw.decode('utf-16-le').lstrip('\ufeff')
    print(f"=== {fname} ===")
    print(text)
    print()
