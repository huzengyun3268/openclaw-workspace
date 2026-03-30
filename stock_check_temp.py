# -*- coding: utf-8 -*-
import urllib.request
import json

# Get additional stocks and check market
stocks = {
    '普适导航': 'sz831330',
    '圣博润': 'sz430046',
    '亨通光电': 'sh600487',
    '特变电工': 'sh600089',
    '中复神鹰': 'sh688295',
}

codes = ','.join(stocks.values())
url = 'http://qt.gtimg.cn/q=' + codes
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk', errors='replace')

results = {}
lines = data.strip().split('\n')
for name, code in stocks.items():
    for line in lines:
        if code in line:
            parts = line.split('~')
            if len(parts) >= 4:
                price = float(parts[3]) if parts[3] else 0
                # parts[4] is yesterday close
                yestclose = float(parts[4]) if parts[4] else price
                chg = (price - yestclose) / yestclose * 100 if yestclose else 0
                results[code] = {'name': name, 'price': price, 'yestclose': yestclose, 'chg': chg}
            break

with open('C:/Users/Administrator/.openclaw/workspace/stock_prices2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('done')
