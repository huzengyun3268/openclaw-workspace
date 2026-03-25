# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

codes = ['600352', '300033', '831330', '000988', '688295', '600487', '300499', '601168', '600893', '920046', '430046', '600114', '301638', '600089']
results = []
for code in codes:
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == code]
        if not row.empty:
            name = row['名称'].values[0]
            price = row['最新价'].values[0]
            chg = row['涨跌幅'].values[0]
            high = row['最高'].values[0]
            low = row['最低'].values[0]
            amount = row['成交额'].values[0]
            results.append(f'{code}|{name}|{price}|{chg}|{high}|{low}|{amount}')
        else:
            results.append(f'{code}|NOT_FOUND|N/A')
    except Exception as e:
        results.append(f'{code}|ERROR|{e}')

for r in results:
    print(r)
