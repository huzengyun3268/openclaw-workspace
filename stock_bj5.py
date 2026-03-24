# -*- coding: utf-8 -*-
import requests

headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com'}

# 普适导航 831330
url1 = 'https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f107,f50&secid=0.831330'
resp1 = requests.get(url1, headers=headers, timeout=10)
print(f'普适导航: {resp1.text}')

# 圣博润 430046
url2 = 'https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f107,f50&secid=0.430046'
resp2 = requests.get(url2, headers=headers, timeout=10)
print(f'圣博润: {resp2.text}')
