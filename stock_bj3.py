# -*- coding: utf-8 -*-
import requests
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Referer': 'https://finance.qq.com'}

# Try different BJ codes for Tencent
# 普适导航 831330 - try different prefixes
for prefix in ['bj', 'bj8', 'BJ']:
    url = f'https://qt.gtimg.cn/q={prefix}831330'
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.encoding = 'gbk'
        print(f'{prefix}831330: {resp.text[:200]}')
    except Exception as e:
        print(f'{prefix}831330: Error - {e}')

# Also try akshare with different functions
print('\n--- Trying akshare stock_bj_a_spot ---')
try:
    import akshare as ak
    df = ak.stock_bj_a_spot_em()
    for code in ['831330', '430046']:
        row = df[df['代码'] == code]
        if not row.empty:
            p = row['最新价'].values[0]
            c = row['涨跌幅'].values[0]
            print(f'{code}: price={p} change={c}%')
        else:
            print(f'{code}: not found')
except Exception as e:
    print(f'akshare error: {e}')
