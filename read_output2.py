# -*- coding: utf-8 -*-
import sys
import os

os.chdir(r'C:\Users\Administrator\.openclaw\workspace')

def read_utf16_le(path):
    with open(path, 'rb') as f:
        raw = f.read()
    # Already checked: UTF-16-LE with BOM
    text = raw.decode('utf-16-le')
    # Remove BOM character
    text = text.lstrip('\ufeff')
    return text

content1 = read_utf16_le('morning_report_out.txt')
content2 = read_utf16_le('short_trade_out.txt')

# Write to a UTF-8 file for reading
with open('report_decoded.txt', 'w', encoding='utf-8') as f:
    f.write("=== MORNING REPORT ===\n")
    f.write(content1)
    f.write("\n=== SHORT TRADE ===\n")
    f.write(content2)

print("Done, written to report_decoded.txt")
print("Lengths:", len(content1), len(content2))
