# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import json

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

codes = ','.join([s[1] for s in stocks])
url = f'http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f5,f6,f12,f14&secids=1.{codes}'

try:
    resp = requests.get(url, timeout=15)
    data = resp.json()
    items = data.get('data', {}).get('diff', [])
    code_map = {s[1]: s[0] for s in stocks}
    print('=== 个股实时行情 13:45 ===')
    for item in items:
        code = item.get('f12', '')
        name = code_map.get(code, code)
        price = item.get('f2', 0)
        pct = item.get('f3', 0)
        high = item.get('f4', '-')
        low = item.get('f5', '-')
        vol = item.get('f6', '-')
        if price not in (None, '-', 0):
            emoji = 'RED' if pct < -3 else ('YEL' if pct < 0 else 'GRN')
            print(f'{emoji} {name}({code}): {price}  {pct:+.2f}%  最高:{high} 最低:{low}')
        else:
            print(f'ERR {name}({code}): no data')
except Exception as e:
    print(f'ERROR: {e}')
