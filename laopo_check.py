import requests
from datetime import datetime
stocks = [('东睦股份', '600114', '1'), ('南网数字', '301638', '0')]
print(f"=== 老婆账户  {datetime.now().strftime('%H:%M:%S')} ===")
for name, code, mkt in stocks:
    try:
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={mkt}.{code}&fields=f43,f170'
        d = requests.get(url, timeout=10).json()
        if d.get('data'):
            p = d['data']['f43'] / 100
            c = d['data']['f170'] / 100
            print(f"{name}({code}): {p:.2f} ({c:+.2f}%)")
    except Exception as e:
        print(f"{name}: {e}")
