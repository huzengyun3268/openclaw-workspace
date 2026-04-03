# -*- coding: utf-8 -*-
import urllib.request
import json

stocks = [
    ('浙江龙盛', 'sh600352'),
    ('航发动力', 'sh600893'),
    ('同花顺', 'sz300033'),
    ('西部矿业', 'sh601168'),
    ('普适导航', 'bj831330'),
    ('亨通光电', 'sh600487'),
    ('中复神鹰', 'sh688295'),
    ('圣博润', 'sz430046'),
    ('东睦股份', 'sh600114'),
    ('特变电工', 'sh600089'),
]

print('=== 持仓监控 2026-03-31 收盘 ===')
for name, code in stocks:
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('gbk', errors='replace')
        fields = data.split('~')
        if len(fields) > 32:
            price = fields[3]
            yest = fields[4]
            open_p = fields[5]
            vol = fields[6]
            amount = fields[7]
            # 计算涨跌
            if price and yest and float(yest) > 0:
                chg = float(price) - float(yest)
                chg_pct = (chg / float(yest)) * 100
                print(f'{name}({code}): 现价={price} 涨跌={chg:.2f}({chg_pct:.2f}%) 昨收={yest} 今开={open_p}')
            else:
                print(f'{name}({code}): {fields}')
        else:
            print(f'{name}({code}): Parse error - {fields[:5]}')
    except Exception as e:
        print(f'{name}({code}): Error - {e}')
