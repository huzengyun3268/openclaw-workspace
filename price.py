import requests
codes = 'sh600352,sh600089,sh518880,sh601288,sz002828'
r = requests.get('https://qt.gtimg.cn/q=' + codes, headers={'User-Agent': 'Mozilla/5.0'})
r.encoding = 'gbk'
names = {'600352':'龙盛','600089':'特变','518880':'黄金ETF','601288':'农业银行','002828':'贝肯能源'}
stop = {'600352':12.0,'600089':25.0}
for line in r.text.strip().split('\n'):
    eq = line.find('=')
    if eq < 0: continue
    raw = line[eq+1:]
    t = raw.find('~')
    if t < 0: continue
    data = raw[t+1:].strip('"').strip(';')
    f = data.split('~')
    if len(f) < 33: continue
    code = f[1]
    price = float(f[2]) if f[2] else 0
    chg = f[31]
    name = names.get(code, code)
    sl = stop.get(code, None)
    if sl:
        gap = (sl - price) / price * 100
        flag = ' ⚠️' if gap > 0 else ' 🔴'
        print(f'{name}: {price} ({chg}%) | 止损{sl} | 距止损{abs(gap):.1f}%{flag}')
    else:
        print(f'{name}: {price} ({chg}%)')
