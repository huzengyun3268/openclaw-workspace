import requests

# Try eastmoney for bj and sz stocks
codes_bj = ['bj831330', 'bj920046']
codes_sz = ['sz430046', 'sz300033']

# Use eastmoney quote API
for code in ['bj831330', 'sz430046']:
    url = f'https://push2.eastmoney.com/api/qt/stock/get?secid=0.{code[2:]}' if code.startswith('bj') else f'https://push2.eastmoney.com/api/qt/stock/get?secid=1.{code[2:]}'
    try:
        r = requests.get(url, timeout=5, headers={'Referer': 'https://quote.eastmoney.com/'})
        data = r.json()
        if 'data' in data and data['data']:
            name = data['data'].get('name', code)
            price = data['data'].get('c', 'N/A')
            chg = data['data'].get('pct', 'N/A')
            print(f"{code} {name}: {price} ({chg}%)")
        else:
            print(f"{code}: no data - {r.text[:100]}")
    except Exception as e:
        print(f"{code}: error - {e}")
