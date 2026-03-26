import requests
# 验证同花顺实际价格
url = 'http://push2.eastmoney.com/api/qt/stock/get?secid=0.300033&fields=f43,f170,f57,f58,f169'
d = requests.get(url, timeout=10).json()
if d.get('data'):
    print(f"secid=0.300033: price={d['data']['f43']}, change={d['data']['f170']}, name={d['data']['f58']}")

# 也试试不同市场
for mkt, label in [('0','深圳'), ('1','上海'), ('2','北京')]:
    url2 = f'http://push2.eastmoney.com/api/qt/stock/get?secid={mkt}.300033&fields=f43,f170,f58'
    d2 = requests.get(url2, timeout=10).json()
    if d2.get('data'):
        p = d2['data']['f43'] / 100
        c = d2['data']['f170'] / 100
        n = d2['data'].get('f58', '')
        print(f"secid={mkt}.300033 [{label}]: {p:.2f} ({c:+.2f}%) name={n}")
    else:
        print(f"secid={mkt}.300033 [{label}]: 无数据")
