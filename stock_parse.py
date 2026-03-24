# -*- coding: utf-8 -*-
import requests
from datetime import datetime

stocks = {
    '600352': ('浙江龙盛', 15.91, 106700),
    '600089': ('特变电工', 24.765, 52300),
    '301667': ('纳百川', 82.715, 3000),
    '920046': ('亿能电力', 35.936, 12731),
    '300033': ('同花顺', 511.22, 600),
    '831330': ('普适导航', 20.415, 6370),
    '300189': ('神农种业', 17.099, 5000),
    '430046': ('圣博润', 0.478, 10334),
}

stocks2 = {
    '600114': ('东睦股份', 32.428, 9200),
    '301638': ('南网数字', 32.635, 1700),
}

tc_codes = {
    '600352': 'sh600352', '600089': 'sh600089', '301667': 'sz301667',
    '920046': 'bj920046', '300033': 'sz300033', '831330': 'bj831330',
    '300189': 'sz300189', '430046': 'bj430046', '600114': 'sh600114',
    '301638': 'sz301638',
}

all_stocks = {}
all_stocks.update(stocks)
all_stocks.update(stocks2)

codes_str = ','.join(tc_codes[c] for c in all_stocks.keys())
url = f'https://qt.gtimg.cn/q={codes_str}'
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'}

now = datetime.now().strftime('%H:%M:%S')
print(f'[{now}] Stock Prices')

resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = 'gbk'

total_pl = 0
print('\n=== MY ACCOUNT ===')
for code, (name, cost, qty) in stocks.items():
    tc = tc_codes[code]
    key = f'v_{tc}'
    for line in resp.text.split(';'):
        if key in line:
            parts = line.split('~')
            if len(parts) > 32:
                price = float(parts[3])
                prev = float(parts[4])
                change = (price - prev) / prev * 100
                market_val = price * qty
                cost_val = cost * qty
                pl = market_val - cost_val
                pl_pct = (price - cost) / cost * 100
                total_pl += pl
                if change >= 0:
                    arrow = '+'
                else:
                    arrow = ''
                print(f'{code} {name}: {price:.3f} ({arrow}{change:.2f}%) Cost={cost:.3f} Qty={qty} PL={pl:+.2f}({pl_pct:+.1f}%)')
            break

print(f'\nAccount Total PL: {total_pl:+.2f}')

print('\n=== WIFE ACCOUNT ===')
wife_pl = 0
for code, (name, cost, qty) in stocks2.items():
    tc = tc_codes[code]
    key = f'v_{tc}'
    for line in resp.text.split(';'):
        if key in line:
            parts = line.split('~')
            if len(parts) > 32:
                price = float(parts[3])
                prev = float(parts[4])
                change = (price - prev) / prev * 100
                market_val = price * qty
                cost_val = cost * qty
                pl = market_val - cost_val
                pl_pct = (price - cost) / cost * 100
                wife_pl += pl
                if change >= 0:
                    arrow = '+'
                else:
                    arrow = ''
                print(f'{code} {name}: {price:.3f} ({arrow}{change:.2f}%) Cost={cost:.3f} Qty={qty} PL={pl:+.2f}({pl_pct:+.1f}%)')
            break

print(f'\nWife Account Total PL: {wife_pl:+.2f}')
print(f'\nCOMBINED TOTAL: {total_pl + wife_pl:+.2f}')
