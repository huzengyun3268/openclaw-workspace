# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

stocks = {
    '600352': '浙江龙盛',
    '600893': '航发动力',
    '300033': '同花顺',
    '601168': '西部矿业',
    '831330': '普适导航',
    '600487': '亨通光电',
    '688295': '中复神鹰',
    '920046': '亿能电力',
    '430046': '圣博润',
}

print("=== 主账户持仓监控 13:30 ===")
try:
    df = ak.stock_zh_a_spot_em()
    for code, name in stocks.items():
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            chg = float(row['涨跌幅'].values[0])
            print(f"{name}({code}): {price}  {chg:+.2f}%")
        else:
            print(f"{name}({code}): 未找到")
except Exception as e:
    print(f"查询失败: {e}")
