# -*- coding: utf-8 -*-
import requests
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'}

# Try eastmoney for BJ stocks
# 831330 普适导航 -> bj831330
# 430046 圣博润 -> bj430046

# eastmoney real-time API
url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids=0.831330,0.430046&ut=b2884a393a59ad64002292a3e90d46a5'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com'}, timeout=10)
print(f'Eastmoney status: {resp.status_code}')
print(resp.text[:2000])

# Also try Tencent with different format
print('\n--- Tencent v2 ---')
url2 = 'https://qt.gtimg.cn/q=bj831330,bj430046'
resp2 = requests.get(url2, headers=headers, timeout=10)
resp2.encoding = 'gbk'
print(resp2.text)
