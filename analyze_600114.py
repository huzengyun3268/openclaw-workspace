import urllib.request, json, ssl
ctx = ssl.create_default_context()
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600114&scale=240&ma=no&datalen=40'
req = urllib.request.Request(url, headers={'User-Agent': ua, 'Referer': 'https://finance.sina.com.cn'})
with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))

print('=== 东睦股份 近期量价分析 ===')
print(f"{'日期':<12} {'收盘':>7} {'涨跌%':>8} {'成交量':>10} {'成交额':>9} {'量比':>6}")
print('-'*55)

vols = [int(d['volume']) for d in data]
avg_vol = sum(vols) / len(vols)

for d in data:
    close = float(d['close'])
    open_p = float(d['open'])
    chg = (close - open_p) / open_p * 100
    vol = int(d['volume'])
    amt = vol * close / 1e8
    ratio = vol / avg_vol
    if ratio > 1.5: marker = '大量'
    elif ratio > 1.2: marker = '放量'
    elif ratio < 0.5: marker = '地量'
    elif ratio < 0.8: marker = '缩量'
    else: marker = ''
    arrow = '+' if chg > 0 else ''
    print(f"{d['day']:<12} {close:>7.2f} {arrow}{chg:>7.2f}% {vol/1e4:>9.1f}万 {amt:>8.2f}亿 {ratio:>5.1f}x {marker}")

print('')
print(f'统计区间: {data[0]["day"]} 至 {data[-1]["day"]}')
print(f'共{len(data)}个交易日')
print(f'平均成交量: {avg_vol/1e4:.1f}万手/日')
avg_amt = sum(int(d['volume'])*float(d['close']) for d in data)/len(data)/1e8
print(f'平均成交额: {avg_amt:.2f}亿/日')
print(f'今日(0327)参考成交量: {int(data[-1]["volume"])/1e4:.1f}万手')
