# -*- coding: utf-8 -*-
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check 圣博润 (430046) - it might be a了新三板股票，需要特殊接口
# Try with bj prefix (北交所)
codes_try = ['bj430046', 'sz430046', '430046']
for code in codes_try:
    url = f'https://qt.gtimg.cn/q=v_{code}'
    try:
        resp = requests.get(url, timeout=5)
        print(f'{code}: {resp.text.strip()[:200]}')
    except Exception as e:
        print(f'{code} Error: {e}')
