# -*- coding: utf-8 -*-
import requests
import json

stocks = [
    ('浙江龙盛', '600352', '1'),    # Shanghai
    ('航发动力', '600893', '1'),    # Shanghai
    ('同花顺', '300033', '0'),       # Shenzhen
    ('西部矿业', '601168', '1'),    # Shanghai
    ('普适导航', '831330', '0'),    # Beijing
    ('亨通光电', '600487', '1'),    # Shanghai
    ('中复神鹰', '688295', '1'),    # Shanghai (科创板)
    ('亿能电力', '920046', '0'),    # Beijing 新三板
    ('圣博润', '430046', '0'),      # Beijing 新三板
    ('东睦股份', '600114', '1'),    # Shanghai
    ('南网数字', '301638', '0'),    # Shenzhen
    ('特变电工', '600089', '1'),    # Shanghai
]

# Build secids: market.code
secids = ','.join([f'{m}.{c}' for _, c, m in stocks])
url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids={secids}&ut=bd1d9ddb04089700cf9c27f6f7426281&cb=jQuery&_=1'

try:
    resp = requests.get(url, timeout=15)
    text = resp.text
    json_str = text[text.index('(') + 1 : text.rindex(')')]
    data = json.loads(json_str)
    if data.get('data') and data['data'].get('diff'):
        for item in data['data']['diff']:
            code = item.get('f12', '')
            name = item.get('f14', '')
            price = item.get('f2', '')
            chg = item.get('f3', '')
            close = item.get('f4', '')
            if price not in ('-', '', None):
                print(f'{name}|{code}|{float(price):.3f}|{float(chg):+.2f}|{float(close):.3f}')
            else:
                print(f'{name}|{code}|N/A|N/A|N/A')
    else:
        print('NO DATA from API')
        print(text[:300])
except Exception as e:
    print(f'ERROR: {e}')
