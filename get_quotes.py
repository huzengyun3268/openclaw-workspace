# -*- coding: utf-8 -*-
import requests
import sys

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://finance.qq.com'
}

# All codes: sh=上交所, sz=深交所, bj=北交所
# 6开头=上交所, 0/3开头=深交所, 8/4开头=北交所(bj)
stock_map = {
    'sh600352': ('浙江龙盛', 86700, 16.52, 12.0),
    'sh600893': ('航发动力', 9000, 49.184, 42.0),
    'sz300033': ('同花顺', 1200, 423.488, 280),
    'sh601168': ('西部矿业', 11000, 26.169, 22.0),
    'bj831330': ('普适导航', 7370, 20.361, 18.0),
    'sh600487': ('亨通光电', 3000, 43.998, 38.0),
    'sh688295': ('中复神鹰', 1500, 37.843, 0),
    'bj920046': ('亿能电力', 200, 329.553, 27),
    'bj430046': ('圣博润', 10334, 0.478, 0),
    'sh600114': ('东睦股份', 4900, 26.0, 25.0),
    'sz301638': ('南网数字', 1700, 32.64, 28.0),
    'sh600089': ('特变电工', 52300, 24.765, 25.0),
}

codes_str = ','.join(stock_map.keys())
url = f'https://qt.gtimg.cn/q={codes_str}'
r = requests.get(url, headers=headers, timeout=15)
# response is in GBK encoding
raw = r.content.decode('gbk')

print("=== 主账户持仓 ===", flush=True)
total_pnl = 0.0

for line in raw.strip().split('\n'):
    parts = line.split('~')
    if len(parts) > 35:
        key = parts[0].split('_')[1] if '_' in parts[0] else parts[0]
        # Find matching key
        matched_key = None
        for k in stock_map:
            if k in parts[0]:
                matched_key = k
                break
        if not matched_key:
            continue
        
        name_local, qty, cost, stop = stock_map[matched_key]
        price = float(parts[3])
        pct = float(parts[32])
        pnl = (price - cost) * qty
        
        flag = ""
        if stop > 0 and price <= stop:
            flag = " [!!止损位!!]"
        elif pct <= -3:
            flag = " [WARNING: large drop]"
        elif matched_key in ['sh600352', 'sh600893', 'sz300033', 'sh601168', 'bj831330', 'sh600487', 'sh688295', 'bj920046', 'bj430046']:
            total_pnl += pnl
        
        print(f"{name_local}({matched_key[2:]}): {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop {stop}{flag}", flush=True)

print("\n=== Wife account ===", flush=True)
for key in ['sh600114', 'sz301638']:
    name_local, qty, cost, stop = stock_map[key]
    code = key[2:]

print("\n=== Margin account ===", flush=True)
for key in ['sh600089']:
    name_local, qty, cost, stop = stock_map[key]
    code = key[2:]

# Get individual price
for line in raw.strip().split('\n'):
    parts = line.split('~')
    if len(parts) > 35:
        code_raw = parts[2] if len(parts) > 2 else ''
        price = float(parts[3]) if len(parts) > 3 else 0
        pct = float(parts[32]) if len(parts) > 32 else 0
        
        if code_raw == '600352':
            qty, cost, stop = 86700, 16.52, 12.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"浙江龙盛: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 12.0{flag}", flush=True)
        elif code_raw == '600893':
            qty, cost, stop = 9000, 49.184, 42.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"航发动力: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 42.0{flag}", flush=True)
        elif code_raw == '300033':
            qty, cost, stop = 1200, 423.488, 280
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"同花顺: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 280{flag}", flush=True)
        elif code_raw == '601168':
            qty, cost, stop = 11000, 26.169, 22.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"西部矿业: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 22.0{flag}", flush=True)
        elif code_raw == '831330':
            qty, cost, stop = 7370, 20.361, 18.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"普适导航: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 18.0{flag}", flush=True)
        elif code_raw == '600487':
            qty, cost, stop = 3000, 43.998, 38.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"亨通光电: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 38.0{flag}", flush=True)
        elif code_raw == '688295':
            qty, cost, stop = 1500, 37.843, 0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"中复神鹰: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | No stop", flush=True)
        elif code_raw == '920046':
            qty, cost, stop = 200, 329.553, 27
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"亿能电力: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 27{flag}", flush=True)
        elif code_raw == '430046':
            qty, cost, stop = 10334, 0.478, 0
            pnl = (price - cost) * qty
            print(f"圣博润: {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | No stop", flush=True)
        elif code_raw == '600114':
            qty, cost, stop = 4900, 26.0, 25.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"东睦股份(W): {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 25.0{flag}", flush=True)
        elif code_raw == '301638':
            qty, cost, stop = 1700, 32.64, 28.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"南网数字(W): {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 28.0{flag}", flush=True)
        elif code_raw == '600089':
            qty, cost, stop = 52300, 24.765, 25.0
            pnl = (price - cost) * qty
            flag = " [!!STOP!!]" if price <= stop else ""
            print(f"特变电工(M): {price} ({pct:+.2f}%) | PnL {pnl/10000:+.1f}w | Stop 25.0{flag}", flush=True)
