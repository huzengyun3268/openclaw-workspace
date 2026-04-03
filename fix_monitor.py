# -*- coding: utf-8 -*-
with open(r'C:\Users\Administrator\.openclaw\workspace\skills\stock-monitor-pro\scripts\monitor_v2.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')
for i, line in enumerate(lines):
    if 'USER_AGENTS' in line or ('UA' in line and len(line) < 100):
        print(f'Line {i+1}: {repr(line[:100])}')
    # Find lines around the problem area (line 210-215)
    if 207 <= i <= 220:
        print(f'Line {i+1}: {repr(line[:120])}')
