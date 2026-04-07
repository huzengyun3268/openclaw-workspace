# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from yang_select import yang_select

print("=" * 50)
print("Yang Yongxing Overnight Select v1.0")
print("Rule: Enter 14:45 Exit nextday 10:30")
print("=" * 50)

results = yang_select(max_stocks=3)

if results:
    print(f"\n[*] Recommended ({len(results)} stocks):")
    for r in results:
        print(f"  {r['name']}({r['code']})")
        print(f"    {r['volume_detail']} | {r['trend_detail']}")
else:
    print("\n[!] No passing stocks today")
