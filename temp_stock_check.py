# -*- coding: utf-8 -*-
import akshare as ak
import sys

stocks_main = [
    ('浙江龙盛', '600352'),
    ('航发动力', '600893'),
    ('同花顺', '300033'),
    ('西部矿业', '601168'),
    ('普适导航', '831330'),
    ('亨通光电', '600487'),
    ('中复神鹰', '688295'),
    ('圣博润', '430046'),
]

print('=== 主账户持仓 2026-03-31 收盘 ===')
for name, code in stocks_main:
    try:
        if code.startswith('6'):
            full_code = 'sh' + code
        elif code.startswith('8') or code.startswith('4'):
            full_code = 'bj' + code
        else:
            full_code = 'sz' + code
        df = ak.stock_individual_info_em(symbol=full_code)
        info = dict(zip(df['item'].tolist(), df['value'].tolist()))
        price = info.get('最新价', 'N/A')
        change_pct = info.get('涨跌幅', 'N/A')
        volume = info.get('成交量', 'N/A')
        amount = info.get('成交额', 'N/A')
        print(f'{name}({full_code}): 现价={price} 涨跌={change_pct} 量={volume} 额={amount}')
    except Exception as e:
        print(f'{name}({code}): Error - {e}')

print()
print('=== 老婆账户持仓 ===')
laopo = [('东睦股份', '600114')]
for name, code in laopo:
    try:
        full_code = 'sh' + code
        df = ak.stock_individual_info_em(symbol=full_code)
        info = dict(zip(df['item'].tolist(), df['value'].tolist()))
        price = info.get('最新价', 'N/A')
        change_pct = info.get('涨跌幅', 'N/A')
        print(f'{name}({full_code}): 现价={price} 涨跌={change_pct}')
    except Exception as e:
        print(f'{name}({code}): Error - {e}')

print()
print('=== 两融账户持仓 ===')
rong = [('特变电工', '600089')]
for name, code in rong:
    try:
        full_code = 'sh' + code
        df = ak.stock_individual_info_em(symbol=full_code)
        info = dict(zip(df['item'].tolist(), df['value'].tolist()))
        price = info.get('最新价', 'N/A')
        change_pct = info.get('涨跌幅', 'N/A')
        print(f'{name}({full_code}): 现价={price} 涨跌={change_pct}')
    except Exception as e:
        print(f'{name}({code}): Error - {e}')
