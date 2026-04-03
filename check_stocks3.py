# -*- coding: utf-8 -*-
import urllib.request
import codecs
import sys

stocks = [
    ('sh600352', 76700, '浙江龙盛', 16.948, 12.0),
    ('sz300033', 1200, '同花顺', 423.488, 280),
    ('sh600487', 3000, '亨通光电', 43.210, 38.0),
    ('sh600893', 9000, '航发动力', 49.184, 42.0),
    ('sh601168', 11000, '西部矿业', 26.169, 22.0),
    ('sh518880', 24000, '黄金ETF', 9.868, None),
    ('sz430046', 10334, '圣博润', 0.478, None),
    ('sh600114', 11100, '东睦股份', 31.176, 25.0),
    ('sh600089', 52300, '特变电工', 24.765, 25.0),
]

codes = ','.join([s[0] for s in stocks])
url = f'https://qt.gtimg.cn/q={codes}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')

output = []
for line in data.strip().split('\n'):
    if '=' not in line:
        continue
    parts = line.split('~')
    if len(parts) < 33:
        continue
    code = parts[0].split('_')[-1]
    price = float(parts[3])
    change = float(parts[31])
    pct = float(parts[32])
    
    for c, qty, name, cost, stop in stocks:
        if c == code:
            pnl = (price - cost) * qty
            output.append(f"{name}|{code}|{price}|{change}|{pct}|{cost}|{stop}|{round(pnl/10000,2)}")
            break

# Write to file with UTF-8
with open(r'C:\Users\Administrator\.openclaw\workspace\stock_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
