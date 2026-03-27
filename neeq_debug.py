import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

neeq_stocks = [('920046', '亿能电力'), ('430046', '圣博润')]
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.eastmoney.com/'}

for code, name in neeq_stocks:
    try:
        neeq_url = f'https://push2.eastmoney.com/api/qt/stock/get?fields=f43,f44,f45,f57,f58,f169,f170,f171,f47,f48&secid=0.{code}&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2'
        r = requests.get(neeq_url, headers=headers, timeout=10)
        d = r.json()
        if d.get('data'):
            f43 = d['data'].get('f43')  # current price
            f44 = d['data'].get('f44')  # yesterday close
            f169 = d['data'].get('f169')  # high
            f170 = d['data'].get('f170')  # change pct
            print(f'{code} {name}: f43={f43} f44={f44} f169={f169} f170={f170}')
            print(f'Raw data: {d["data"]}')
        else:
            print(f'{code} {name}: no data - {d}')
    except Exception as e:
        print(f'{code} {name}: error - {e}')
