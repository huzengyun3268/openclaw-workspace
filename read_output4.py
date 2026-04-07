# -*- coding: utf-8 -*-
import sys
import os

os.chdir(r'C:\Users\Administrator\.openclaw\workspace')

# Check raw bytes of each file
for fname in ['short_trade_out.txt', 'short2.txt']:
    if not os.path.exists(fname):
        print(f"{fname}: NOT FOUND\n")
        continue
    with open(fname, 'rb') as f:
        raw = f.read()
    print(f"=== {fname} (first 200 bytes) ===")
    print("Hex:", raw[:100].hex())
    print("Repr:", repr(raw[:200]))
    print()
