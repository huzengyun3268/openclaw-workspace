# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
from datetime import datetime

now = datetime.now().strftime('%Y-%m-%d %H:%M')

# 主账户持仓
main_stocks = [
    ('浙江龙盛', '600352', 'sh', 16.52, 86700, 12.0),
    ('航发动力', '600893', 'sh', 49.184, 9000, 42.0),
    ('同花顺', '300033', 'sz', 423.488, 1200, 280),
    ('西部矿业', '601168', 'sh', 26.169, 11000, 22.0),
    ('普适导航', '831330', 'bj', 20.361, 7370, 18.0),
    ('亨通光电', '600487', 'sh', 45.47, 4000, 38.0),
    ('中复神鹰', '688295', 'sh', 56.85, 3000, None),
    ('圣博润', '430046', 'sz', 0.478, 10334, None),
]

# 老婆账户
wife_stocks = [
    ('东睦股份', '600114', 'sh', 31.681, 4900, 25.0),
]

# 两融账户
margin_stocks = [
    ('特变电工', '600089', 'sh', 24.765, 52300, 25.0),
]

print(f'=== 持仓监控报告 {now} ===')
print()

# 获取实时行情
try:
    df = ak.stock_zh_a_spot_em()
    codes = [s[1] for s in main_stocks + wife_stocks + margin_stocks]
    spot = df[df['代码'].isin(codes)][['代码','名称','最新价','涨跌幅','涨跌额','成交量','成交额']]
    spot_dict = {}
    for _, row in spot.iterrows():
        spot_dict[row['代码']] = {
            'price': row['最新价'],
            'change_pct': row['涨跌幅'],
            'change_amt': row['涨跌额'],
        }
except Exception as e:
    print(f'获取行情失败: {e}')
    spot_dict = {}

print('【主账户 3293】')
total_pl = 0
for name, code, mkt, cost, qty, stop in main_stocks:
    info = spot_dict.get(code, {})
    price = info.get('price', 0)
    chg = info.get('change_pct', 0)
    if price > 0:
        pl = (price - cost) * qty
        pl_pct = (price / cost - 1) * 100
        total_pl += pl
        stop_alert = ' [触及止损!]' if stop and price <= stop else (' [涨停]' if chg >= 9.9 else '')
        print(f'  {name}({mkt}{code}): {price:.2f}  {chg:+.2f}%  浮盈:{pl/10000:+.1f}万({pl_pct:+.1f}%){stop_alert}')
    else:
        print(f'  {name}({mkt}{code}): 行情获取失败')

print(f'  主账户浮动盈亏: {total_pl/10000:+.1f}万')
print()

print('【老婆账户】')
for name, code, mkt, cost, qty, stop in wife_stocks:
    info = spot_dict.get(code, {})
    price = info.get('price', 0)
    chg = info.get('change_pct', 0)
    if price > 0:
        pl = (price - cost) * qty
        pl_pct = (price / cost - 1) * 100
        stop_alert = ' [触及止损!]' if stop and price <= stop else (' [跌破成本!]' if price < cost * 0.95 else '')
        print(f'  {name}({mkt}{code}): {price:.2f}  {chg:+.2f}%  浮盈:{pl/10000:+.1f}万({pl_pct:+.1f}%){stop_alert}')
print()

print('【两融账户 2306】')
for name, code, mkt, cost, qty, stop in margin_stocks:
    info = spot_dict.get(code, {})
    price = info.get('price', 0)
    chg = info.get('change_pct', 0)
    if price > 0:
        pl = (price - cost) * qty
        pl_pct = (price / cost - 1) * 100
        stop_alert = ' [触及止损!]' if stop and price <= stop else ''
        print(f'  {name}({mkt}{code}): {price:.2f}  {chg:+.2f}%  浮盈:{pl/10000:+.1f}万({pl_pct:+.1f}%){stop_alert}')
print()

print('=== 操作提醒 ===')
# 中复神鹰 T+1 提醒
info = spot_dict.get('688295', {})
chg = info.get('change_pct', 0)
if info.get('price', 0) > 0:
    print(f'中复神鹰: 今日涨幅{chg:+.2f}%，明天(T+1)可卖出')

# 亨通光电涨停
info = spot_dict.get('600487', {})
if info.get('price', 0) > 0 and info.get('change_pct', 0) >= 9.9:
    print('亨通光电: 涨停中，次日可卖出')

# 东睦股份风险提醒
info = spot_dict.get('600114', {})
if info.get('price', 0) > 0:
    price = info['price']
    cost = 31.681
    stop = 25.0
    if price <= stop:
        print(f'东睦股份: ⚠️ 已触及止损价{stop}，建议止损!')
    elif price < cost * 0.85:
        print(f'东睦股份: ⚠️ 距成本跌幅已超15%，关注风险!')
