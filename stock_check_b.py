# -*- coding: utf-8 -*-
import akshare as ak

# 补查: 831330(新三板), 920046(北交所), 430046(新三板)
extra = [
    ('831330', '普适导航', 'bj'),
    ('920046', '亿能电力', 'bj'),
    ('430046', '圣博润', 'bj'),
]

for code, name, expected_market in extra:
    try:
        # 北交所用bj前缀
        df = ak.stock_zh_a_daily(symbol='bj' + code, adjust='qfq')
        if len(df) > 0:
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else latest
            price = float(latest.get('close', 0))
            prev_close = float(prev.get('close', 0))
            pct = (price - prev_close) / prev_close * 100 if prev_close > 0 else 0
            print(f'{name}({code}): {price} | {pct:.2f}%')
        else:
            print(f'{name}({code}): NO DATA from bj')
    except Exception as e:
        print(f'{name}({code}): ERROR {e}')
