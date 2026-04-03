import json

with open('C:\\Users\\Administrator\\.openclaw\\workspace\\stock_prices.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

# pm maps code -> price
pm = {}
rev = {}  # name -> code
# We know the names from the previous fetch, but let's just use code as key
# The previous JSON had names as keys, so reconstruct:
name_to_code = {
    '浙江龙盛':'600352', '航发动力':'600893', '同花顺':'300033',
    '西部矿业':'601168', '亨通光电':'600487', '中复神鹰':'688295',
    '东睦股份':'600114', '特变电工':'600089'
}
for name, code in name_to_code.items():
    if name in raw:
        pm[code] = raw[name]

pos = [
    {'name':'浙江龙盛', 'code':'600352', 'vol':86700, 'cost':16.52, 'stop':12.0, 'account':'主账户'},
    {'name':'航发动力', 'code':'600893', 'vol':9000, 'cost':49.184, 'stop':42.0, 'account':'主账户'},
    {'name':'同花顺', 'code':'300033', 'vol':1200, 'cost':423.488, 'stop':280.0, 'account':'主账户'},
    {'name':'西部矿业', 'code':'601168', 'vol':11000, 'cost':26.169, 'stop':22.0, 'account':'主账户'},
    {'name':'普适导航', 'code':'831330', 'vol':7370, 'cost':20.361, 'stop':18.0, 'account':'主账户'},
    {'name':'亨通光电', 'code':'600487', 'vol':4000, 'cost':45.47, 'stop':38.0, 'account':'主账户'},
    {'name':'中复神鹰', 'code':'688295', 'vol':3000, 'cost':56.85, 'stop':0, 'account':'主账户'},
    {'name':'圣博润', 'code':'430046', 'vol':10334, 'cost':0.478, 'stop':0, 'account':'主账户'},
]
wife = [
    {'name':'东睦股份', 'code':'600114', 'vol':4900, 'cost':31.681, 'stop':25.0, 'account':'老婆账户'},
]
margin = [
    {'name':'特变电工', 'code':'600089', 'vol':52300, 'cost':24.765, 'stop':25.0, 'account':'两融账户'},
]

all_items = pos + wife + margin
total_gain = 0.0
lines = []
alerts = []

for p in all_items:
    code = p['code']
    price = pm.get(code)
    if price is None:
        lines.append(p['account'] + ' | ' + p['name'] + '(' + code + '): NO DATA')
        continue
    cost = p['cost']
    vol = p['vol']
    gain = (price - cost) * vol
    gain_pct = (price / cost - 1) * 100
    total_gain += gain
    stopped = p['stop'] > 0 and price <= p['stop']

    sign = '+' if gain >= 0 else ''
    stop_flag = ' !!STOP-HIT!!' if stopped else ''
    up_flag = ' [ZHANGTING]' if price >= cost * 1.0999 else ''
    lines.append(p['account'] + ' | ' + p['name'] + '(' + code + ') Price=' + str(price) + ' Cost=' + str(cost) + ' Gain=' + sign + str(round(gain/10000,1)) + 'w(' + sign + str(round(gain_pct,2)) + '%) Stop=' + str(p['stop']) + stop_flag + up_flag)
    if stopped:
        alerts.append(p['name'] + ' price ' + str(price) + ' <= stop ' + str(p['stop']))

lines.append('')
lines.append('Total Gain: ' + ('+' if total_gain >= 0 else '') + str(round(total_gain/10000,1)) + 'w')

with open('C:\\Users\\Administrator\\.openclaw\\workspace\\stock_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Report done. Total gain: ' + str(round(total_gain/10000,1)) + 'w')
if alerts:
    print('ALERTS: ' + '; '.join(alerts))
