# -*- coding: utf-8 -*-
import requests

# 新三板/北交所股票
codes_bj = [
    ('831330', '普适导航', 'bj'),
    ('430046', '圣博润', 'bj'),
    ('920046', '亿能电力', 'bj'),
]

results = []
for code, name, mkt in codes_bj:
    try:
        symbol = f'{mkt}{code}'
        url = f'http://hq.sinajs.cn/list={symbol}'
        headers = {'Referer': 'http://finance.sina.com.cn', 'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=8)
        text = resp.content.decode('gbk', errors='replace')
        parts = text.split('"')
        if len(parts) > 1:
            data = parts[1].split(',')
            if len(data) > 6:
                open_p = float(data[1])
                close_p = float(data[2])
                current = float(data[3])
                high = float(data[4])
                low = float(data[5])
                change = current - close_p
                pct = (change / close_p) * 100 if close_p else 0
                results.append((code, name, current, change, pct, high, low))
            else:
                results.append((code, name, 0, 0, 0, 0, 0))
        else:
            results.append((code, name, 0, 0, 0, 0, 0))
    except Exception as e:
        results.append((code, name, 0, 0, 0, 0, 0))

for code, name, price, change, pct, high, low in results:
    if price > 0:
        print(f"{code} {name}: {price} ({pct:+.2f}%) H:{high} L:{low}")
    else:
        print(f"{code} {name}: N/A")
