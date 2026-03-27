# -*- coding: utf-8 -*-
import akshare as ak

for code, name in [('831330', '普适导航'), ('430046', '圣博润')]:
    try:
        df = ak.stock_zh_new_spot()
        row = df[df['代码'] == code]
        if len(row) > 0:
            r = row.iloc[0]
            price = float(r.get('现价', 0))
            pct = float(r.get('涨跌幅', 0))
            print(f'{name}({code}): {price} | {pct}%')
        else:
            print(f'{name}({code}): NOT FOUND')
    except Exception as e:
        print(f'{name}({code}): ERROR {e}')
