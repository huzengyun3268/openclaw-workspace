# -*- coding: utf-8 -*-
import requests

tc_codes = ['sh600352','sh600089','sz301667','bj920046','sz300033','bj831330','sz300189','bj430046','sh600114','sz301638']
codes_str = ','.join(tc_codes)
url = f'https://qt.gtimg.cn/q={codes_str}'
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'}
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = 'gbk'
for line in resp.text.split(';'):
    for tc in tc_codes:
        if f'v_{tc}' in line:
            parts = line.split('~')
            if len(parts) > 32:
                print(f'{tc}: price={parts[3]} prev={parts[4]} time={parts[30]}')
            break
