import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
codes = 'sh600256,sh600522,sz002491'
url = 'https://qt.gtimg.cn/q=' + codes
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com/'}
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = 'gbk'
lines = resp.text.strip().split('\n')
for line in lines:
    eq = line.find('=')
    if eq < 0: continue
    raw = line[eq+1:]
    t = raw.find('~')
    if t < 0: continue
    data = raw[t+1:]
    # strip trailing garbage
    data = data.strip('"').strip(";")
    fields = data.split('~')
    # field mapping: [0]=name(garbled), [1]=code, [2]=price, [3]=prev_close, [31]=change%
    name = fields[1] if len(fields) > 1 else '?'
    price = fields[2] if len(fields) > 2 else '?'
    prev = fields[3] if len(fields) > 3 else '?'
    chg = fields[31] if len(fields) > 31 else '?'
    print(name + ': 现价' + price + ' 昨收' + prev + ' 涨跌幅' + chg + '%')
