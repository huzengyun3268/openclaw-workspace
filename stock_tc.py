# -*- coding: utf-8 -*-
import requests
from datetime import datetime
import time

# Try Tencent finance API
stocks = {
    '600352': ('浙江龙盛', 15.91, 106700),
    '600089': ('特变电工', 24.765, 52300),
    '301667': ('纳百川', 82.715, 3000),
    '920046': ('亿能电力', 35.936, 12731),
    '300033': ('同花顺', 511.22, 600),
    '831330': ('普适导航', 20.415, 6370),
    '300189': ('神农种业', 17.099, 5000),
    '430046': ('圣博润', 0.478, 10334),
    '600114': ('东睦股份', 32.428, 9200),
    '301638': ('南网数字', 32.635, 1700),
}

# Map to Tencent codes
tc_codes = {
    '600352': 'sh600352', '600089': 'sh600089', '301667': 'sz301667',
    '920046': 'bj920046', '300033': 'sz300033', '831330': 'bj831330',
    '300189': 'sz300189', '430046': 'bj430046', '600114': 'sh600114',
    '301638': 'sz301638',
}

now = datetime.now().strftime('%H:%M:%S')
print(f'[{now}] Trying Tencent API...')

codes_str = ','.join(tc_codes.values())
url = f'https://qt.gtimg.cn/q={codes_str}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.qq.com',
}

try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = 'gbk'
    print(f'Status: {resp.status_code}')
    print(resp.text[:2000])
except Exception as e:
    print(f'Error: {e}')

print('\n--- Trying 163 API ---')
try:
    codes163 = ';'.join([c for c in tc_codes.keys()])
    url163 = f'http://api.money.126.net/data/feed/{codes_str}'
    resp = requests.get(url163, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    print(f'Status: {resp.status_code}')
    print(resp.text[:2000])
except Exception as e:
    print(f'Error: {e}')
