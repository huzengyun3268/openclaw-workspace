import urllib.request
import re
import json

# Get all data including bz stocks
positions = [
    {'name':'浙江龙盛', 'code':'600352', 'market':'sh', 'hold':86700, 'cost':16.52, 'stop':12.0},
    {'name':'航发动力', 'code':'600893', 'market':'sh', 'hold':9000, 'cost':49.184, 'stop':42.0},
    {'name':'同花顺', 'code':'300033', 'market':'sz', 'hold':1200, 'cost':423.488, 'stop':280},
    {'name':'西部矿业', 'code':'601168', 'market':'sh', 'hold':11000, 'cost':26.169, 'stop':22.0},
    {'name':'普适导航', 'code':'831330', 'market':'bz', 'hold':7370, 'cost':20.361, 'stop':18.0},
    {'name':'亨通光电', 'code':'600487', 'market':'sh', 'hold':4000, 'cost':45.47, 'stop':38.0},
    {'name':'中复神鹰', 'code':'688295', 'market':'sh', 'hold':3000, 'cost':56.85, 'stop':None},
    {'name':'圣博润', 'code':'430046', 'market':'bz', 'hold':10334, 'cost':0.478, 'stop':None},
    {'name':'东睦股份', 'code':'600114', 'market':'sh', 'hold':4900, 'cost':31.681, 'stop':25.0, 'account':'laopo'},
    {'name':'特变电工', 'code':'600089', 'market':'sh', 'hold':52300, 'cost':24.765, 'stop':25.0, 'account':'margin'},
]

# Group by API needed
shsz = [p for p in positions if p['market'] in ('sh','sz')]
bz = [p for p in positions if p['market'] == 'bz']

price_map = {}

# Tencent API for sh/sz
q_shsz = ','.join([f'{p["market"]}{p["code"]}' for p in shsz])
url1 = f'https://qt.gtimg.cn/q={q_shsz}'
req1 = urllib.request.Request(url1, headers={'User-Agent':'Mozilla/5.0','Referer':'http://gu.qq.com'})
with urllib.request.urlopen(req1, timeout=10) as r:
    raw = r.read().decode('gbk')
for line in raw.strip().split('\n'):
    m = re.match(r'v_(\w+)=\"(.+)\"', line)
    if not m: continue
    key = m.group(1)
    fields = m.group(2).split('~')
    if len(fields) < 35: continue
    code = key[2:] if len(key) == 8 else key
    price = float(fields[3]) if fields[3] else 0
    pct = float(fields[32]) if fields[32] else 0
    price_map[code] = {'price': price, 'pct': pct}

# Eastmoney API for bz
for p in bz:
    market_id = '0' if p['code'].startswith('8') or p['code'].startswith('83') else '0'
    # bz is market 0 in eastmoney
    url2 = f'http://push2.eastmoney.com/api/qt/stock/get?secid=0.{p["code"]}&fields=f43,f57,f58,f170,f171&ut=fa5fd1943c7b386f172d6893dbfba10b'
    req2 = urllib.request.Request(url2, headers={'User-Agent':'Mozilla/5.0','Referer':'http://quote.eastmoney.com'})
    try:
        with urllib.request.urlopen(req2, timeout=5) as r2:
            data = json.loads(r2.read().decode('utf-8'))
            d = data.get('data',{})
            price = d.get('f43', 0)
            price = price / 100.0 if price > 100 else price  # in cents if large
            pct = d.get('f170', 0) / 100.0 if d.get('f170') else 0
            price_map[p['code']] = {'price': price, 'pct': pct}
    except Exception as e:
        print(f'{p["name"]} error: {e}')

alerts = []
for p in positions:
    code = p['code']
    info = price_map.get(code, {})
    price = info.get('price', 0)
    pct = info.get('pct', 0)
    
    if price == 0 or price is None:
        print(f'{p["name"]}({code}): --')
        continue
    
    pl = (price - p['cost']) * p['hold']
    account = p.get('account','main')
    acc_label = {'main':'', 'laopo':'[老婆]', 'margin':'[两融]'}[account]
    
    stop_info = ''
    if p['stop']:
        dist = (price - p['stop'])/price * 100
        stop_info = f' | 止损{price-p["stop"]:.2f}元({dist:.1f}%)'
        if price <= p['stop']:
            alerts.append(f'{p["name"]}触及止损 {price}<={p["stop"]}')
    
    if pct <= -3.0:
        alerts.append(f'{p["name"]}跌幅{pct}%超3%')
    
    print(f'{p["name"]}{acc_label}: {price}({pct:+.2f}%) | 成本:{p["cost"]} | 浮亏:{pl/10000:.1f}万{stop_info}')

print(f'\n时间: 2026-03-31 09:17')
if alerts:
    print('\n=== 预警 ===')
    for a in alerts:
        print('WARNING: ' + a)
