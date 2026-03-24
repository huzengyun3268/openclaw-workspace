# -*- coding: utf-8 -*-
import requests
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'}
url = 'https://qt.gtimg.cn/q=bj831330,bj430046'
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = 'gbk'
print(resp.text)
