# -*- coding: utf-8 -*-
import urllib.request
import re

pos = [
    {'code':'sh600352','name':'Zhejiang Longsheng','vol':86700,'cost':16.52,'stop':12.0,'account':'Main'},
    {'code':'sh600893','name':'Hangfa Power','vol':9000,'cost':49.184,'stop':42.0,'account':'Main'},
    {'code':'sz300033','name':'Tonghuashun','vol':1200,'cost':423.488,'stop':280.0,'account':'Main'},
    {'code':'sh601168','name':'Xibu Mining','vol':11000,'cost':26.169,'stop':22.0,'account':'Main'},
    {'code':'bj831330','name':'Pushi Nav','vol':7370,'cost':20.361,'stop':18.0,'account':'Main'},
    {'code':'sh600487','name':'Hengrui Optic','vol':4000,'cost':45.47,'stop':38.0,'account':'Main'},
    {'code':'sh688295','name':'Zhongfu Carbon','vol':3000,'cost':56.85,'stop':0,'account':'Main'},
    {'code':'sz430046','name':'Shenbongrun','vol':10334,'cost':0.478,'stop':0,'account':'Main'},
]
wife = [
    {'code':'sh600114','name':'Dongmu Gufen','vol':4900,'cost':31.681,'stop':25.0,'account':'Wife'},
]
margin = [
    {'code':'sh600089','name':'Tebian Power','vol':52300,'cost':24.765,'stop':25.0,'account':'Margin'},
]

names_cn = {
    'sh600352':'Zhejiang Longsheng',
    'sh600893':'Hangfa Power',
    'sz300033':'Tonghuashun',
    'sh601168':'Xibu Mining',
    'bj831330':'Pushi Nav',
    'sh600487':'Hengrui Optic',
    'sh688295':'Zhongfu Carbon',
    'sz430046':'Shenbongrun',
    'sh600114':'Dongmu Gufen',
    'sh600089':'Tebian Power',
}

all_codes = ','.join([p['code'] for p in pos+wife+margin])

try:
    url = 'https://qt.gtimg.cn/q=' + all_codes
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('gbk', 'ignore')
except Exception as e:
    print('Fetch error: ' + str(e))
    html = ''

pm = {}
for line in html.split('\n'):
    m = re.search(r'hq_str_[a-z]+\d+="([^"]+)"', line)
    if m:
        parts = m.group(1).split('~')
        if len(parts) >= 4:
            code_raw = parts[0]
            try:
                price = float(parts[3])
                if code_raw and price > 0:
                    pm[code_raw] = price
            except:
                pass

print('Prices fetched: ' + str(pm))
print('')

total_gain = 0
all_items = pos + wife + margin
stopped_list = []

for p in all_items:
    code = p['code']
    price = pm.get(code)
    if price is None:
        print(p['name'] + '(' + code + '): QUERY FAILED')
        continue
    cost = p['cost']
    vol = p['vol']
    gain = (price - cost) * vol
    gain_pct = (price / cost - 1) * 100
    total_gain += gain
    stopped = p['stop'] > 0 and price <= p['stop']
    if stopped:
        stopped_list.append(p['name'])

    sign = '+' if gain >= 0 else ''
    print(p['account'] + ' | ' + names_cn.get(code, code) + '(' + code + ')')
    print('  Price=' + str(price) + ' Cost=' + str(cost) + ' Gain=' + sign + str(round(gain,0)) + '(' + sign + str(round(gain_pct,2)) + '%) Stop=' + str(p['stop']))
    print('')

print('Total Gain: ' + str(round(total_gain, 0)))
if stopped_list:
    print('!! STOP HIT: ' + ', '.join(stopped_list))
