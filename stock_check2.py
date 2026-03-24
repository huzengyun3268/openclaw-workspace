# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
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
    '600114': ('东睦股份(老婆)', 32.428, 9200),
    '301638': ('南网数字(老婆)', 32.635, 1700),
}

all_codes = list(stocks.keys()) + list(stocks2.keys())
now = datetime.now().strftime('%H:%M:%S')
print(f'[{now}] Fetching data...')

try:
    df = ak.stock_zh_a_spot_em()
    print('\n=== MY ACCOUNT ===')
    total_pl = 0
    for code, (name, cost, qty) in stocks.items():
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            change = float(row['涨跌幅'].values[0])
            market_val = price * qty
            cost_val = cost * qty
            pl = market_val - cost_val
            pl_pct = (price - cost) / cost * 100
            total_pl += pl
            print(f'{code} {name}: price={price:.3f} change={change:+.2f}% qty={qty} cost={cost:.3f} pl={pl:+.2f} pl_pct={pl_pct:+.1f}%')
        else:
            print(f'{code} {name}: NO_DATA')

    print(f'Account total PL: {total_pl:+.2f}')

    print('\n=== WIFE ACCOUNT ===')
    for code, (name, cost, qty) in stocks2.items():
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            change = float(row['涨跌幅'].values[0])
            market_val = price * qty
            cost_val = cost * qty
            pl = market_val - cost_val
            pl_pct = (price - cost) / cost * 100
            print(f'{code} {name}: price={price:.3f} change={change:+.2f}% qty={qty} cost={cost:.3f} pl={pl:+.2f} pl_pct={pl_pct:+.1f}%')
        else:
            print(f'{code} {name}: NO_DATA')
except Exception as e:
    print(f'Error: {e}')
