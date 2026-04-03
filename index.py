import requests
r = requests.get('https://qt.gtimg.cn/q=s_sh000001,s_sh399001,s_sz399006', headers={'User-Agent': 'Mozilla/5.0'})
r.encoding = 'gbk'
names = {'000001':'上证指数','399001':'深证成指','399006':'创业板'}
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
    price = f[2]
    chg = f[31]
    name = names.get(code, code)
    bar = '+' if float(chg) > 0 else ''
    print(name + ': ' + price + ' ' + bar + chg + '%')
