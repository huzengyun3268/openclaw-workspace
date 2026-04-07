# -*- coding: utf-8 -*-
import codecs
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def read_with_encoding(path):
    with open(path, 'rb') as f:
        raw = f.read()
    # Remove BOM if present
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        raw = raw[2:]
    if raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    # Try decode
    for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030', 'latin-1']:
        try:
            return raw.decode(enc)
        except:
            continue
    return raw.decode('latin-1', errors='replace')

path1 = r'C:\Users\Administrator\.openclaw\workspace\morning_report_out.txt'
path2 = r'C:\Users\Administrator\.openclaw\workspace\short_trade_out.txt'

print("=== MORNING REPORT ===")
print(read_with_encoding(path1))
print("=== SHORT TRADE ===")
print(read_with_encoding(path2))
