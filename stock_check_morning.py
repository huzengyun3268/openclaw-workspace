import requests, json

positions = [
    {'name': '浙江龙盛', 'code': 'sh600352', 'shares': 86700, 'cost': 16.52, 'stop': 12.0},
    {'name': '航发动力', 'code': 'sh600893', 'shares': 9000, 'cost': 49.184, 'stop': 42.0},
    {'name': '同花顺', 'code': 'sz300033', 'shares': 1200, 'cost': 423.488, 'stop': 280.0},
    {'name': '西部矿业', 'code': 'sh601168', 'shares': 11000, 'cost': 26.169, 'stop': 22.0},
    {'name': '普适导航', 'code': 'sz831330', 'shares': 7370, 'cost': 20.361, 'stop': 18.0},
    {'name': '亨通光电', 'code': 'sh600487', 'shares': 3000, 'cost': 43.998, 'stop': 38.0},
    {'name': '中复神鹰', 'code': 'sh688295', 'shares': 1500, 'cost': 37.843, 'stop': 0},
    {'name': '亿能电力', 'code': 'bj920046', 'shares': 200, 'cost': 329.553, 'stop': 27.0},
    {'name': '圣博润', 'code': 'sz430046', 'shares': 10334, 'cost': 0.478, 'stop': 0},
]

total_pnl = 0
total_value = 0
alerts = []

for p in positions:
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={p["code"]}', timeout=5)
        raw = r.text
        fields = raw.split('~')
        if len(fields) > 10:
            price = float(fields[3])
            name = fields[1]
            pct = float(fields[32]) if fields[32] else 0
            value = price * p['shares']
            cost = p['cost'] * p['shares']
            pnl = value - cost
            total_pnl += pnl
            total_value += value
            stop = p['stop']
            warn = ''
            if stop and price <= stop:
                warn = ' [!!触及止损!!]'
                alerts.append(f'{name} 触及止损价{stop}元!')
            elif stop and price <= stop * 1.05:
                warn = ' [预警接近止损]'
                alerts.append(f'{name} 接近止损{stop}元，现价{price}')
            print(f'{name}: 现价{price} | {pct}% | 市值{value/10000:.1f}万 | 盈亏{pnl/10000:+.1f}万{warn}')
        else:
            print(f'{p["name"]}: 数据失败')
    except Exception as e:
        print(f'{p["name"]}: 请求异常 {e}')

print(f'\n总市值: {total_value/10000:.1f}万 | 总盈亏: {total_pnl/10000:+.1f}万')
if alerts:
    print('\n=== 预警 ===')
    for a in alerts:
        print(a)
