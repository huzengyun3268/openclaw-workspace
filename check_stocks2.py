# -*- coding: utf-8 -*-
import urllib.request
import json

stocks = [
    ('sh600352', '浙江龙盛', 16.948, 12.0),
    ('sz300033', '同花顺', 423.488, 280),
    ('sh600487', '亨通光电', 43.210, 38.0),
    ('sh600893', '航发动力', 49.184, 42.0),
    ('sh601168', '西部矿业', 26.169, 22.0),
    ('sh518880', '黄金ETF', 9.868, None),
    ('sz430046', '圣博润', 0.478, None),
    ('sh600114', '东睦股份', 31.176, 25.0),
    ('sh600089', '特变电工', 24.765, 25.0),
]

codes = ','.join([s[0] for s in stocks])
url = f'https://qt.gtimg.cn/q={codes}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')

results = []
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
    
    for c, name, cost, stop in stocks:
        if c == code:
            pnl = (price - cost) * (76700 if c == 'sh600352' else 
                     1200 if c == 'sz300033' else
                     3000 if c == 'sh600487' else
                     9000 if c == 'sh600893' else
                     11000 if c == 'sh601168' else
                     24000 if c == 'sh518880' else
                     10334 if c == 'sz430046' else
                     11100 if c == 'sh600114' else
                     52300)
            results.append({
                'name': name,
                'code': code,
                'price': price,
                'change': change,
                'pct': pct,
                'cost': cost,
                'stop': stop,
                'pnl_wan': round(pnl / 10000, 2)
            })
            break

print(json.dumps(results, ensure_ascii=False, indent=2))
