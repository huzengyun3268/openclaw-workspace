# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode('gbk', errors='replace')
    except Exception as e:
        return f"Error: {e}"

# 指数
indices_url = 'https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sh000300'
resp = get(indices_url)
print("=== 主要指数 ===")
for line in resp.strip().split('\n'):
    if 'pv2' in line or '_' in line:
        parts = line.split('~')
        if len(parts) > 10:
            name = parts[1]
            price = parts[3]
            prev = parts[4]
            change = float(price) - float(prev)
            pct = (change / float(prev) * 100) if float(prev) else 0
            vol = parts[6]
            amount = parts[7]
            print(f"{name}: {price} {change:+.2f} ({pct:+.2f}%) 成交量{vol} 成交额{amount}")

# 个股
stocks = [
    ('sh600352', '浙江龙盛'),
    ('sz300033', '同花顺'),
    ('sh600487', '亨通光电'),
    ('sh600893', '航发动力'),
    ('sh601168', '西部矿业'),
    ('sh518880', '黄金ETF'),
    ('sz430046', '圣博润'),
    ('sh600114', '东睦股份'),
    ('sh600089', '特变电工'),
]

print("\n=== 持仓个股 ===")
codes = ','.join([s[0] for s in stocks])
resp2 = get(f'https://qt.gtimg.cn/q={codes}')
for line in resp2.strip().split('\n'):
    parts = line.split('~')
    if len(parts) > 10:
        code = parts[0].replace('v_', '')
        name = parts[1]
        price = parts[3]
        prev = parts[4]
        change = float(price) - float(prev)
        pct = (change / float(prev) * 100) if float(prev) else 0
        vol = parts[6]
        amount = parts[7]
        print(f"{name}({code}): {price} {change:+.2f} ({pct:+.2f}%) 额{amount}万")
