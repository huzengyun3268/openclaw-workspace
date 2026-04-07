# -*- coding: utf-8 -*-
import sys
import os

os.chdir(r'C:\Users\Administrator\.openclaw\workspace')
sys.stdout.reconfigure(encoding='utf-8')

for fname in ['short_trade_out.txt', 'short2.txt']:
    if not os.path.exists(fname):
        print(f"{fname}: NOT FOUND\n")
        continue
    with open(fname, 'rb') as f:
        raw = f.read()
    text = raw.decode('utf-16-le').lstrip('\ufeff')
    print(f"=== {fname} ===")
    print(text)
    print()
