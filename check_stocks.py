# -*- coding: utf-8 -*-
import urllib.request
import sys

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

codes = ','.join([s[0] for s in stocks])
url = f'https://qt.gtimg.cn/q={codes}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')

for line in data.strip().split('\n'):
    if '=' not in line:
        continue
    parts = line.split('~')
    if len(parts) < 33:
        continue
    code = parts[0].split('_')[-1]
    name = parts[1]
    price = parts[3]
    change = parts[31]
    pct = parts[32]
    # Find the name from our list
    for c, n in stocks:
        if c == code:
            name = n
            break
    print(f'{name}|{code}|{price}|{change}|{pct}')
