# -*- coding: utf-8 -*-
import requests
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Use Tencent stock API
codes = ['sh600352', 'sz300033', 'sh600487', 'sh600893', 'sh601168', 'sh518880', 'sz430046', 'sh600089']

url = 'https://qt.gtimg.cn/q=' + ','.join(codes)

try:
    resp = requests.get(url, timeout=10)
    lines = resp.text.strip().split('\n')
    results = []
    for line in lines:
        parts = line.split('~')
        if len(parts) > 50:
            code = parts[0].replace('sz', '').replace('sh', '')
            name = parts[1]
            price = parts[3]
            change_pct = parts[32]
            high = parts[33]
            low = parts[34]
            vol = parts[36]
            amount = parts[37]
            results.append(f"{code}\t{name}\t{price}\t{change_pct}%\t{high}\t{low}\t{vol}\t{amount}")
    for r in results:
        print(r)
except Exception as e:
    print(f'Error: {e}')
