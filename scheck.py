# -*- coding: utf-8 -*-
import sys
import json
import urllib.request

stocks = [
    ('600352', '浙江龙盛'),
    ('300033', '同花顺'),
    ('000988', '华工科技'),
    ('688295', '中复神鹰'),
    ('600487', '亨通光电'),
    ('300499', '高澜股份'),
    ('601168', '西部矿业'),
    ('600893', '航发动力'),
]

results = []
for code, name in stocks:
    try:
        if code.startswith('6'):
            secid = f'1.{code}'
        else:
            secid = f'0.{code}'
        
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f57,f58,f169&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2'
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            d = data.get('data', {})
            if d:
                price = d.get('f43', 0) / 100
                chg = d.get('f169', 0) / 100
                results.append(f'{name}({code}): {price} ({chg:+.2f}%)')
            else:
                results.append(f'{name}({code}): no data')
    except Exception as e:
        results.append(f'{name}({code}): error')

with open(r'C:\Users\Administrator\.openclaw\workspace\stock_results.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
