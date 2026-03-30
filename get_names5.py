# -*- coding: utf-8 -*-
import urllib.request, json

codes = [
    ('sz002471', '+35', '3.15%'),
    ('sh688011', '+35', '3.48%'),
    ('sz002491', '+25', '3.83%'),
    ('sh603387', '+10', '3.13%'),
    ('sz002431', '+10', '3.58%'),
    ('sh600186', '+10', '3.50%'),
    ('sz002246', '+10', '4.47%'),
    ('sh688802', '+10', '4.83%'),
    ('sh688667', '+10', '3.36%'),
    ('sz002181', '+5',  '4.42%'),
]

for code, score, change in codes:
    url = f"https://qt.gtimg.cn/q={code}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            raw = r.read()
            # GBK decode
            text = raw.decode('gbk', errors='replace')
            parts = text.split('~')
            name = parts[1] if len(parts) > 1 else 'N/A'
            price = parts[3] if len(parts) > 3 else 'N/A'
            print(f"{code} [{name}] price={price} change={change} score={score}")
    except Exception as e:
        print(f"{code} ERROR: {e}")
