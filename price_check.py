# -*- coding: utf-8 -*-
import json
import akshare as ak
import time

stocks = [
    ('600352', '浙江龙盛'),
    ('300033', '同花顺'),
    ('000988', '华工科技'),
    ('688295', '中复神鹰'),
    ('600487', '亨通光电'),
    ('300499', '高澜股份'),
    ('601168', '西部矿业'),
    ('600893', '航发动力'),
    ('600089', '特变电工'),
]

result = []
for code, name in stocks:
    try:
        df = ak.stock_zh_a_hist(symbol=code, period='daily', start_date='20260325', end_date='20260326', adjust='')
        if df is not None and not df.empty:
            latest = df.iloc[-1]
            price = float(latest.get('收盘', latest.get('close', 0)))
            pct = float(latest.get('涨跌幅', latest.get('pct', 0)))
            result.append({'code': code, 'name': name, 'price': price, 'pct': pct})
        else:
            result.append({'code': code, 'name': name, 'price': None, 'pct': None, 'error': 'no_data'})
    except Exception as e:
        result.append({'code': code, 'name': name, 'price': None, 'pct': None, 'error': str(e)})
    time.sleep(1)

with open(r'C:\Users\Administrator\.openclaw\workspace\price_data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print('Done')
