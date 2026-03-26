# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import akshare as ak
import pandas as pd
from datetime import datetime

codes = {
    '600352': '浙江龙盛',
    '300033': '同花顺',
    '831330': '普适导航',
    '000988': '华工科技',
    '688295': '中复神鹰',
    '600487': '亨通光电',
    '300499': '高澜股份',
    '601168': '西部矿业',
    '600893': '航发动力',
    '920046': '亿能电力',
    '430046': '圣博润',
    '600114': '东睦股份',
    '301638': '南网数字',
    '600089': '特变电工',
}

today = datetime.now().strftime('%Y%m%d')

results = []
for code, name in codes.items():
    try:
        if code.startswith('6'):
            sym = f"sh{code}"
        elif code.startswith('4') or code.startswith('8') or code.startswith('9'):
            sym = f"bj{code}"
        else:
            sym = f"sz{code}"
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            chg = row['涨跌幅'].values[0]
            amount = float(row['成交额'].values[0]) / 1e8
            results.append({'代码': code, '名称': name, '最新价': price, '涨跌幅': chg, '成交额亿': round(amount, 2)})
        else:
            results.append({'代码': code, '名称': name, '最新价': 'N/A', '涨跌幅': 'N/A', '成交额亿': 'N/A'})
    except Exception as e:
        results.append({'代码': code, '名称': name, '最新价': f'ERR:{e}', '涨跌幅': 'N/A', '成交额亿': 'N/A'})

df_res = pd.DataFrame(results)
print(df_res.to_string(index=False))
