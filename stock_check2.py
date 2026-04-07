# -*- coding: utf-8 -*-
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check 东睦股份 and 圣博润
codes = ['sz430046', 'sh600114']
url = 'https://qt.gtimg.cn/q=' + ','.join(codes)

try:
    resp = requests.get(url, timeout=10)
    print(resp.text.strip())
except Exception as e:
    print(f'Error: {e}')
