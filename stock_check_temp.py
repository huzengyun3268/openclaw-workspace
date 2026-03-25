# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import akshare as ak

stocks = [
    ('600352', '浙江龙盛'),
    ('300033', '同花顺'),
    ('000988', '华工科技'),
    ('688295', '中复神鹰'),
    ('600487', '亨通光电'),
    ('300499', '高澜股份'),
    ('601168', '西部矿业'),
    ('600893', '航发动力'),
]

df = ak.stock_zh_a_spot_em()
for code, name in stocks:
    try:
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            chg = float(row['涨跌幅'].values[0])
            print(f"{name}({code}): {price} ({chg:+.2f}%)")
        else:
            print(f"{name}({code}): 无数据")
    except Exception as e:
        print(f"{name}({code}): 错误 - {e}")
