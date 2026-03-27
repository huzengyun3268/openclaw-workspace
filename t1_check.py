import urllib.request, ssl, sys
sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()

stocks = [
    ('sh.000927', '中国石油'),
    ('sh.600780', '通润资源'),
    ('sz.301312', '顺威股份(创业板)'),
    ('sh.300501', '顺威股份'),
    ('sh.300749', '东岳硅材'),
    ('sh.603115', '银星能源'),
    ('sz.000973', '佛塑科技'),
    ('sh.688307', '东风科技'),
    ('sz.300168', '万润信息'),
    ('sz.000659', '珠海中富'),
]

results = []
for mkt, name in stocks:
    try:
        url = 'http://hq.sinajs.cn/list=' + mkt
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'http://finance.sina.com.cn'})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
            data = r.read().decode('gbk', errors='ignore')
        parts = data.split('"')[1].split(',')
        price = float(parts[3])
        prev = float(parts[2])
        chg = price - prev
        chg_pct = chg / prev * 100
        vol = float(parts[8]) / 10000
        arrow = '▲' if chg >= 0 else '▼'
        line = f'{name}: {price:.2f} {arrow}{abs(chg_pct):.2f}% 成交:{vol:.0f}万'
        results.append(line)
        print(line)
    except Exception as e:
        print(f'{name}: 获取失败')
        results.append(f'{name}: 获取失败')
