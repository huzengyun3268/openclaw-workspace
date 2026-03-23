import urllib.request

stocks = [('普适导航', '831330'), ('圣博润', '430046')]
for name, code in stocks:
    try:
        url = f'http://hq.sinajs.cn/list=ob{code}'
        req = urllib.request.Request(url, headers={'Referer': 'http://finance.sina.com.cn'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read().decode('gbk')
            parts = data.split('"')[1].split(',')
            price = float(parts[3])
            prev = float(parts[2])
            pct = (price - prev) / prev * 100
            print(f'{name}|{code}|{price}|{pct:.2f}')
    except Exception as e:
        print(f'{name}|{code}|ERROR|{e}')
