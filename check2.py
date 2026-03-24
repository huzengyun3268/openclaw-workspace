# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import akshare as ak
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)

stocks = [
    ('浙江龙盛', '600352'),
    ('特变电工', '600089'),
    ('同花顺', '300033'),
    ('中复神鹰', '688295'),
    ('高澜股份', '300499'),
    ('亿能电力', '920046'),
    ('普适导航', '831330'),
    ('圣博润', '430046'),
    ('东睦股份', '600114'),
    ('南网数字', '301638'),
    ('华工科技', '000988'),
    ('亨通光电', '600487'),
    ('西部矿业', '601168'),
    ('航发动力', '600893'),
    ('神农种业', '300189'),
]

print('=== 个股实时行情 13:45 ===')
for name, code in stocks:
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            pct = float(row['涨跌幅'].values[0])
            vol = row['成交额'].values[0]
            high = row['最高'].values[0]
            low = row['最低'].values[0]
            emoji = 'RED' if pct < -3 else ('YEL' if pct < 0 else 'GRN')
            print(f'{emoji} {name}({code}): {price:.3f}  {pct:+.2f}%  最高:{high} 最低:{low}  额:{vol}')
        else:
            print(f'ERR {name}({code}): no data')
    except Exception as e:
        print(f'ERR {name}({code}): ERROR {e}')
