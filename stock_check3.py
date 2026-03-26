# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import akshare as ak

# Use single data fetch
df = ak.stock_zh_a_spot_em()
cols = df.columns.tolist()
# Find code column
code_col = None
name_col = None
for c in cols:
    if c in ['代码', 'code']:
        code_col = c
    if c in ['名称', 'name', '股票名称']:
        name_col = c

print(f'列名: {cols[:10]}')

# Main account positions
main_stocks = [
    ('600352', '浙江龙盛', 106700, 15.952, 12.0),
    ('300033', '同花顺', 1200, 423.488, 280),
    ('831330', '普适导航', 7370, 20.361, 0),
    ('000988', '华工科技', 1000, 116.87, 0),
    ('688295', '中复神鹰', 1500, 37.843, 0),
    ('600487', '亨通光电', 2000, 42.391, 0),
    ('300499', '高澜股份', 1500, 41.625, 38.0),
    ('601168', '西部矿业', 2000, 24.863, 0),
    ('600893', '航发动力', 1000, 47.196, 0),
    ('920046', '亿能电力', 200, 329.555, 27),
    ('430046', '圣博润', 10334, 0.478, 0),
]

# Margin account
margin_stocks = [
    ('600089', '特变电工', 52300, 24.765, 25.0),
]

# Wife account
wife_stocks = [
    ('600114', '东睦股份', 4800, 26.5, 25.0),
    ('301638', '南网数字', 1700, 32.635, 28.0),
]

print()
print('=== 主账户持仓 ===')
total_pnl = 0
for code, name, vol, cost, stop in main_stocks:
    row = df[df[code_col] == code]
    if not row.empty:
        price = float(row['最新价'].values[0])
        chg = float(row['涨跌幅'].values[0])
        pnl = (price - cost) * vol
        total_pnl += pnl
        flag = ''
        if stop > 0 and price <= stop:
            flag = ' ⚠️止损位'
        elif price < cost * 0.9:
            flag = ' ⚠️亏>10%'
        print(f'{name}({code}): {price:.2f} {chg:+.2f}% 浮:{pnl:+.0f}元{flag}')
    else:
        print(f'{name}({code}): 数据未找到')

print()
print(f'主账户浮动盈亏合计: {total_pnl:+.0f}元')
print()
print('=== 两融账户持仓 ===')
for code, name, vol, cost, stop in margin_stocks:
    row = df[df[code_col] == code]
    if not row.empty:
        price = float(row['最新价'].values[0])
        chg = float(row['涨跌幅'].values[0])
        pnl = (price - cost) * vol
        flag = ''
        if price <= stop:
            flag = ' ⚠️止损位'
        print(f'{name}({code}): {price:.2f} {chg:+.2f}% 浮:{pnl:+.0f}元{flag}')
    else:
        print(f'{name}({code}): 数据未找到')

print()
print('=== 老婆账户持仓 ===')
for code, name, vol, cost, stop in wife_stocks:
    row = df[df[code_col] == code]
    if not row.empty:
        price = float(row['最新价'].values[0])
        chg = float(row['涨跌幅'].values[0])
        pnl = (price - cost) * vol
        flag = ''
        if price <= stop:
            flag = ' ⚠️止损位'
        print(f'{name}({code}): {price:.2f} {chg:+.2f}% 浮:{pnl:+.0f}元{flag}')
    else:
        print(f'{name}({code}): 数据未找到')
