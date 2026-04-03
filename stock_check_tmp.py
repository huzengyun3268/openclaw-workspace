# -*- coding: utf-8 -*-
positions = [
    ('浙江龙盛', 'sh600352', 76700, 16.948, 13.22),
    ('同花顺', 'sz300033', 1200, 423.488, 298.1),
    ('亨通光电', 'sh600487', 3000, 43.210, 53.39),
    ('航发动力', 'sh600893', 9000, 49.184, 49.8),
    ('西部矿业', 'sh601168', 11000, 26.169, 25.5),
    ('黄金ETF', 'sh518880', 24000, 9.868, 9.738),
    ('圣博润', 'sz430046', 10334, 0.478, 0.478),
]
laopo = [('东睦股份', 'sh600114', 11100, 31.176, 27.51)]
margin = [('特变电工', 'sh600089', 52300, 24.765, 26.17)]

print('=== 主账户持仓 ===')
total_main = 0
for name, code, vol, cost, price in positions:
    pl = (price - cost) * vol
    total_main += pl
    pct = (price - cost) / cost * 100
    print(f'{name}: 现价{price} 成本{cost} 盈亏{pl:+,.0f}({pct:+.1f}%)')
print(f'主账户小计: {total_main:+,.0f}')

print()
print('=== 老婆账户 ===')
for name, code, vol, cost, price in laopo:
    pl = (price - cost) * vol
    pct = (price - cost) / cost * 100
    print(f'{name}: 现价{price} 成本{cost} 盈亏{pl:+,.0f}({pct:+.1f}%)')

print()
print('=== 两融账户 ===')
for name, code, vol, cost, price in margin:
    pl = (price - cost) * vol
    pct = (price - cost) / cost * 100
    print(f'{name}: 现价{price} 成本{cost} 盈亏{pl:+,.0f}({pct:+.1f}%)')

print()
print('=== 止损检查 ===')
stop_map = {
    '浙江龙盛': 12.0, '同花顺': 280, '亨通光电': 38.0,
    '航发动力': 42.0, '西部矿业': 22.0, '东睦股份': 25.0, '特变电工': 25.0
}
all_pos = positions + laopo + margin
alerts = []
for name, code, vol, cost, price in all_pos:
    stop = stop_map.get(name)
    if stop and price <= stop:
        alerts.append(f'【警告】{name}现价{price}已触及或跌破止损价{stop}！请注意！')

if alerts:
    for a in alerts:
        print(a)
else:
    print('暂无触及止损的持仓')

print()
print('总盈亏(主账户):', total_main)
