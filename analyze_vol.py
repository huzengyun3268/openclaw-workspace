import urllib.request, json, ssl, math

ctx = ssl.create_default_context()
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
url = 'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600352&scale=240&ma=no&datalen=40'
req = urllib.request.Request(url, headers={'User-Agent': ua, 'Referer': 'https://finance.sina.com.cn'})
with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))

print('=== 浙江龙盛 近期量价分析 ===')
print(f"{'日期':<12} {'收盘':>7} {'涨跌%':>8} {'成交量':>10} {'量比':>6} {'状态'}")
print('-'*60)

vols = [int(d['volume']) for d in data]
avg_vol = sum(vols) / len(vols)

for d in data:
    close = float(d['close'])
    prev_close = float(d['open'])
    chg = (close - prev_close) / prev_close * 100
    vol = int(d['volume'])
    amt = vol * close / 1e8
    ratio = vol / avg_vol
    if ratio > 1.5:
        marker = '大量'
    elif ratio > 1.2:
        marker = '放量'
    elif ratio < 0.5:
        marker = '地量'
    elif ratio < 0.8:
        marker = '缩量'
    else:
        marker = ''
    arrow = '+' if chg > 0 else ''
    print(f"{d['day']:<12} {close:>7.3f} {arrow}{chg:>7.2f}% {vol/1e4:>9.1f}万 {ratio:>5.1f}x {marker}")

print('')
print(f'统计区间: {data[0]["day"]} 至 {data[-1]["day"]}')
print(f'共{len(data)}个交易日')
print(f'平均成交量: {avg_vol/1e4:.1f}万手')
print(f'今日(0327)成交量: {int(data[-1]["volume"])/1e4:.1f}万手')
print(f'量比: {int(data[-1]["volume"])/avg_vol:.2f}x')
