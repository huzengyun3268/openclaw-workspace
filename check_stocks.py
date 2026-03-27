# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

stocks = {
    '600352': '浙江龙盛',
    '600893': '航发动力',
    '300033': '同花顺',
    '601168': '西部矿业',
    '831330': '普适导航',
    '600487': '亨通光电',
    '688295': '中复神鹰',
    '920046': '亿能电力',
    '430046': '圣博润',
    '600089': '特变电工',
}

try:
    df = ak.stock_zh_a_spot_em()
    print('=== 持仓行情监控 ===')
    print(f'时间: 2026-03-27 13:00')
    print()
    
    positions = {
        '600352': (16.52, 12.0, 86700),
        '600893': (49.184, 42.0, 9000),
        '300033': (423.488, 280, 1200),
        '601168': (26.169, 22.0, 11000),
        '831330': (20.361, 18.0, 7370),
        '600487': (43.998, 38.0, 3000),
        '688295': (37.843, None, 1500),
        '920046': (329.553, 27, 200),
        '430046': (0.478, None, 10334),
        '600089': (24.765, 25.0, 52300),
    }
    
    total_pl = 0
    alerts = []
    
    for code, name in stocks.items():
        row = df[df['代码'] == code]
        if not row.empty:
            price = float(row['最新价'].values[0])
            change = float(row['涨跌幅'].values[0])
            cost, stop, shares = positions[code]
            pl = (price - cost) * shares
            total_pl += pl
            
            status = '✓'
            if stop and price <= stop:
                status = '⚠️ 止损!'
            elif stop and price <= cost * 0.95:
                status = '⚠️ 接近止损'
            elif change <= -2:
                status = '📉'
            elif change >= 2:
                status = '📈'
            
            print(f'{status} {code} {name}: 现价{price:.3f} ({change:+.2f}%) | 成本{cost:.3f} | 盈亏{pl:+,.0f}元')
            
            if stop and price <= stop:
                alerts.append(f'【止损提醒】{name}({code}) 现价{price} <= 止损价{stop}')
        else:
            print(f'  {code} {name}: 未找到')
    
    print()
    print(f'浮动盈亏合计: {total_pl:+,.0f}元')
    
    if alerts:
        print()
        print('=== 告警 ===')
        for a in alerts:
            print(a)
    
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
