# -*- coding: utf-8 -*-
positions = {
    '600352': ('浙江龙盛', 16.52, 12.0, 86700, 13.37),
    '600893': ('航发动力', 49.184, 42.0, 9000, 48.12),
    '300033': ('同花顺', 423.488, 280, 1200, 302.88),
    '601168': ('西部矿业', 26.169, 22.0, 11000, 25.32),
    '831330': ('普适导航', 20.361, 18.0, 7370, 19.94),
    '600487': ('亨通光电', 43.998, 38.0, 3000, 49.07),
    '688295': ('中复神鹰', 37.843, None, 1500, 57.12),
    '920046': ('亿能电力', 329.553, 27, 200, 28.12),
    '430046': ('圣博润', 0.478, None, 10334, 0.30),
}

total_pl = 0
print('=== 主账户持仓监控 2026-03-27 13:06 ===')
print()
for code, (name, cost, stop, shares, price) in positions.items():
    pl = (price - cost) * shares
    total_pl += pl
    pct = (price - cost) / cost * 100
    
    status = '✓'
    alert = ''
    if stop and price <= stop:
        status = '⚠️ 止损!'
        alert = ' ← 触发止损!'
    elif stop and price <= cost * 0.95:
        status = '⚠️ 接近止损'
        alert = ' ← 接近止损!'
    
    print(f'{status} {code} {name}: 现价{price} | 成本{cost} | 盈亏{pl:+,.0f}元({pct:+.1f}%) | 止损{stop}{alert}')

print()
print(f'浮动盈亏合计: {total_pl:+,.0f}元')
print()
print('=== 今日涨幅 ===')
changes = {
    '600352': 1.36, '600893': 0.25, '300033': 2.03, '601168': 0.96,
    '831330': -0.20, '600487': 2.49, '688295': -5.27, '920046': -1.06,
    '430046': 3.45, '600089': 0.25
}
gainers = [(code, name, chg) for code, (name, *_) in positions.items() if (chg := changes.get(code, 0)) > 0]
losers = [(code, name, chg) for code, (name, *_) in positions.items() if (chg := changes.get(code, 0)) < 0]
print('涨幅:', ', '.join([f'{n}({c:+g:.2f}%)' for c,n,g in gainers]) if gainers else '无')
print('跌幅:', ', '.join([f'{n}({c:+g:.2f}%)' for c,n,g in losers]) if losers else '无')
