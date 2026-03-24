# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
from datetime import datetime
import time

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

codes = list(stocks.keys()) + list(stocks2.keys())
now = datetime.now().strftime('%H:%M:%S')
print(f'[{now}] Retrying stock data...')

for attempt in range(3):
    try:
        df = ak.stock_zh_a_spot_em()
        print(f'Got {len(df)} records')
        results = []
        for code, (name, cost, qty) in list(stocks.items()) + list(stocks2.items()):
            row = df[df['代码'] == code]
            if not row.empty:
                price = float(row['最新价'].values[0])
                change = float(row['涨跌幅'].values[0])
                market_val = price * qty
                cost_val = cost * qty
                pl = market_val - cost_val
                pl_pct = (price - cost) / cost * 100
                results.append((code, name, price, change, qty, cost, pl, pl_pct))
                print(f'{code} {name}: {price:.3f} ({change:+.2f}%) PL={pl:+.2f} ({pl_pct:+.1f}%)')
            else:
                print(f'{code} {name}: N/A')
        break
    except Exception as e:
        print(f'Attempt {attempt+1} failed: {e}')
        time.sleep(3)
