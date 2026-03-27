# -*- coding: utf-8 -*-
import requests
import json

stocks_info = {
    '600352': ('浙江龙盛', 16.52, 12.0, 86700),
    '600893': ('航发动力', 49.184, 42.0, 9000),
    '300033': ('同花顺', 423.488, 280, 1200),
    '601168': ('西部矿业', 26.169, 22.0, 11000),
    '831330': ('普适导航', 20.361, 18.0, 7370),
    '600487': ('亨通光电', 43.998, 38.0, 3000),
    '688295': ('中复神鹰', 37.843, None, 1500),
    '920046': ('亿能电力', 329.553, 27, 200),
    '430046': ('圣博润', 0.478, None, 10334),
    '600089': ('特变电工', 24.765, 25.0, 52300),
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.eastmoney.com/',
    'Accept': 'application/json',
}

# Build secids for eastmoney: 1=sh, 0=sz
secids = []
for code in stocks_info:
    if code.startswith('6'):
        secids.append(f'1.{code}')
    else:
        secids.append(f'0.{code}')

secid_str = ','.join(secids)
url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids={secid_str}'

try:
    resp = requests.get(url, headers=headers, timeout=10)
    print('Status:', resp.status_code)
    print('Content:', resp.text[:500])
except Exception as e:
    print(f'Error: {e}')
