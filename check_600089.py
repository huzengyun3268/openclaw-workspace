import urllib.request, sys, numpy as np
sys.stdout.reconfigure(encoding='utf-8')
url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sh600089,day,,,20,qfq'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://gu.qq.com'})
r = urllib.request.urlopen(req, timeout=8)
txt = r.read().decode('utf-8')

# Parse manually
idx = txt.find('qfqday":[[')
start = idx + len('qfqday":[[')
end = txt.find(']]', start)
raw = txt[start:end]
rows = raw.split('],[')
print('特变电工(600089) 近10日K线:')
print('日期           开盘     收盘     最高     最低     涨跌幅')
for row in rows[-10:]:
    parts = row.replace('"', '').split(',')
    if len(parts) >= 6:
        date = parts[0]
        o = float(parts[1]); c = float(parts[2]); h = float(parts[3]); low = float(parts[4])
        chg = (c - o) / o * 100
        print(f'{date}  {o:>7.2f}  {c:>7.2f}  {h:>7.2f}  {low:>7.2f}  {chg:>+5.2f}%')

# 计算MA
closes = []
for row in rows[-20:]:
    parts = row.replace('"', '').split(',')
    if len(parts) >= 3:
        closes.append(float(parts[2]))
closes = closes[-20:]
ma5 = np.mean(closes[-5:])
ma10 = np.mean(closes[-10:])
ma20 = np.mean(closes[-20:])
print(f'\n均线: MA5={ma5:.2f}  MA10={ma10:.2f}  MA20={ma20:.2f}')
print(f'成本: 24.765  止损: 25.0')
print(f'今日收盘: {closes[-1]:.2f}  距止损: {(closes[-1]-25)/25*100:+.1f}%')
