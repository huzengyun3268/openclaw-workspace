# -*- coding: utf-8 -*-
import urllib.request
import sys

# 沪深主要指数
indices = [
    ('sh000001', '上证指数'),
    ('sh000300', '沪深300'),
    ('sz399001', '深证成指'),
    ('sz399006', '创业板指'),
    ('sh000016', '上证50'),
    ('sh000688', '科创50'),
]

codes_str = ','.join([x[0] for x in indices])
url = 'https://qt.gtimg.cn/q=' + codes_str
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'})
r = urllib.request.urlopen(req, timeout=10)
raw = r.read().decode('gbk')

for line in raw.strip().split('\n'):
    if not line.strip():
        continue
    parts = line.split('~')
    if len(parts) > 32:
        code_full = parts[0].replace('v_', '')
        for idx_code, idx_name in indices:
            if idx_code.replace('sh', '').replace('sz', '') in code_full:
                price = parts[3]
                chg = parts[32]
                try:
                    p = float(price)
                    c = float(chg)
                    arrow = '▲' if c > 0 else '▼'
                    sys.stdout.buffer.write((f'{idx_name}: {p:.2f} {arrow}{c:+.2f}%\n').encode('utf-8'))
                except:
                    pass
                break
