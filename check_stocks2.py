# -*- coding: utf-8 -*-
import requests
import json

# Stock codes and positions
stocks_info = {
    '600352': ('浙江龙盛', 16.52, 12.0, 86700),
    '600893': ('航发动力', 49.184, 42.0, 9000),
    '300033': ('同花顺', 423.488, 280, 1200),
    '601168': ('西部矿业', 26.169, 22.0, 11000),
    '831330': ('普适导航', 20.361, 18.0, 7370),
    '600487': ('亨通光电', 43.998, 38.0, 3000),
    '688295': ('中复神鹰', 37.843, None, 1500),
    '920046': ('亿能电力', 329.553, 27, 200),
    '430046': ('圣博润', 0.478, None, 10334),
    '600089': ('特变电工', 24.765, 25.0, 52300),
}

# Try eastmoney quote API
codes = ','.join(stocks_info.keys())
url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f5,f6,f12,f14&secids=1.{codes}'

try:
    resp = requests.get(url, timeout=10)
    data = resp.json()
    
    print('=== 持仓行情监控 2026-03-27 13:00 ===')
    print()
    
    results = data.get('data', {}).get('diff', [])
    
    total_pl = 0
    alerts = []
    
    for item in results:
        code = item.get('f12', '')
        name = item.get('f14', '')
        price = item.get('f2', 0)
        change_pct = item.get('f3', 0)
        
        if code in stocks_info:
            cost, stop, shares = stocks_info[code]
            if price and price > 0:
                pl = (price - cost) * shares
                total_pl += pl
                
                status = '正常'
                if stop and price <= stop:
                    status = '⚠️ 止损!'
                    alerts.append(f'【止损】{name}({code}) 现价{price} <= 止损价{stop}')
                elif stop and price <= cost * 0.95:
                    status = '⚠️ 接近止损'
                
                arrow = '↑' if change_pct > 0 else '↓' if change_pct < 0 else '-'
                print(f'{status} {code} {name}: {price}({arrow}{abs(change_pct):.2f}%) | 成本{cost} | 盈亏{pl:+,.0f}元 | {shares}股')
    
    print()
    print(f'浮动盈亏合计: {total_pl:+,.0f}元')
    
    if alerts:
        print()
        for a in alerts:
            print(a)
            
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
