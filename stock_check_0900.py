# -*- coding: utf-8 -*-
import akshare as ak
import sys
sys.stdout.reconfigure(encoding='utf-8')

stocks = [
    ('浙江龙盛', 'sh600352'),
    ('航发动力', 'sh600893'),
    ('同花顺', 'sz300033'),
    ('西部矿业', 'sh601168'),
    ('普适导航', 'sh831330'),
    ('亨通光电', 'sh600487'),
    ('中复神鹰', 'sh688295'),
    ('圣博润', 'sh430046'),
    ('东睦股份', 'sh600114'),
]

print('=== 持仓监控 09:30 ===')
df = ak.stock_zh_a_spot_em()
for name, code in stocks:
    try:
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            change_pct = float(row['涨跌幅'].values[0])
            print(f'{name}({code}): {price} ({change_pct:+.2f}%)')
        else:
            print(f'{name}({code}): 未找到')
    except Exception as e:
        print(f'{name}({code}): 错误-{e}')
