# -*- coding: utf-8 -*-
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.sina.com.cn'
}

# Try Sina API for BJ stocks
codes = ['bj831330', 'bj430046']
url = f'https://hq.sinajs.cn/list={",".join(codes)}'
try:
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = 'gbk'
    print(f'Sina: {resp.text}')
except Exception as e:
    print(f'Sina error: {e}')

# Try eastmoney snapshot
print('\n--- Eastmoney snapshot ---')
try:
    url2 = 'https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f107,f50&secid=0.831330&cb=jQuery'
    resp2 = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com'}, timeout=10)
    print(f'Status: {resp2.status_code}')
    print(resp2.text[:500])
except Exception as e:
    print(f'Eastmoney error: {e}')
