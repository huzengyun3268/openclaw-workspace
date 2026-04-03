import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

codes = 'sh512480,sh512760,sh518880,sz159915,sh512800,sz159928,sh512690,sh600487,sz002460,sz300750,sh601899,sh600028'
r = requests.get('https://qt.gtimg.cn/q=' + codes, headers={'User-Agent': 'Mozilla/5.0'})
r.encoding = 'gbk'
results = []
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
    chg = float(f[31]) if f[31] else 0
    high = f[32] if len(f) > 32 else '?'
    prev = float(f[3]) if f[3] else 0
    name_map = {
        '512480': '半导体ETF', '512760': '芯片ETF', '518880': '黄金ETF',
        '159915': '创业板ETF', '512800': '银行ETF', '159928': '消费ETF',
        '512690': '国防ETF', '600487': '亨通光电', '002460': '赣锋锂业',
        '300750': '宁德时代', '601899': '紫金矿业', '600028': '中国石化'
    }
    name = name_map.get(code, code)
    results.append((chg, name, code, price, chg, high))
    print(f'{name}: 现价{price} 涨跌{chg}% 最高{high}')

results.sort(key=lambda x: x[0], reverse=True)
print('\n=== 今日板块强弱排序 ===')
for chg, name, code, price, pct, high in results:
    bar = '+' if pct > 0 else ''
    print(f'{bar}{pct}%  {name}')
