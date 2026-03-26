# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import akshare as ak
import pandas as pd

print('=== 主账户持仓实时行情 ===')
stocks = [
    ('600352', '浙江龙盛', 106700, 15.952, 12.0),
    ('300033', '同花顺', 1200, 423.488, 280),
    ('000988', '华工科技', 1000, 116.87, 0),
    ('688295', '中复神鹰', 1500, 37.843, 0),
    ('600487', '亨通光电', 2000, 42.391, 0),
    ('300499', '高澜股份', 1500, 41.625, 38.0),
    ('601168', '西部矿业', 2000, 24.863, 0),
    ('600893', '航发动力', 1000, 47.196, 0),
]

try:
    df = ak.stock_zh_a_spot_em()
    cols = df.columns.tolist()
    code_col = None
    for c in ['代码', '代码', 'code', 'Code']:
        if c in cols:
            code_col = c
            break
    
    for code, name, vol, cost, stop in stocks:
        row = df[df[code_col] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            chg = float(row['涨跌幅'].values[0])
            pnl = (price - cost) * vol
            flag = ''
            if stop > 0 and price <= stop:
                flag = ' [止损位]'
            elif price < cost * 0.9:
                flag = ' [亏损>10%]'
            print(f'{name}({code}): {price:.2f} 涨跌:{chg:+.2f}% 浮盈亏:{pnl:+.0f}元{flag}')
        else:
            print(f'{name}({code}): 未找到')
except Exception as e:
    print(f'获取行情失败: {e}')

print()
print('=== 两融账户持仓 ===')
try:
    df = ak.stock_zh_a_spot_em()
    code = '600089'
    name = '特变电工'
    vol = 52300
    cost = 24.765
    code_col = '代码'
    for c in ['代码', 'code', 'Code']:
        if c in df.columns.tolist():
            code_col = c
            break
    row = df[df[code_col] == code]
    if not row.empty:
        price = float(row['最新价'].values[0])
        chg = float(row['涨跌幅'].values[0])
        pnl = (price - cost) * vol
        flag = ''
        if price <= 25.0:
            flag = ' [止损位]'
        print(f'{name}({code}): {price:.2f} 涨跌:{chg:+.2f}% 浮盈亏:{pnl:+.0f}元{flag}')
except Exception as e:
    print(f'获取特变电工行情失败: {e}')
