# -*- coding: utf-8 -*-
import akshare as ak

# 补查 831330 普适导航 和 430046 圣博润 - 北交所/新三板
# 尝试直接用akshare接口
for code, name in [('831330', '普适导航'), ('430046', '圣博润')]:
    try:
        # 北交所
        df = ak.stock_bj_spot_em()
        row = df[df['代码'] == code]
        if len(row) > 0:
            r = row.iloc[0]
            price = float(r.get('最新价', 0))
            pct = float(r.get('涨跌幅', 0))
            print(f'{name}({code}) BJ: {price} | {pct}%')
            continue
    except Exception as e1:
        pass
    
    try:
        # 用集合竞价接口
        df = ak.stock_zh_a_spot_em(symbol='北证A股')
        row = df[df['代码'] == code]
        if len(row) > 0:
            r = row.iloc[0]
            price = float(r.get('最新价', 0))
            pct = float(r.get('涨跌幅', 0))
            print(f'{name}({code}) BZX: {price} | {pct}%')
            continue
    except Exception as e2:
        pass
    
    print(f'{name}({code}): FAILED')
