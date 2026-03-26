import requests

# Stocks from USER.md - with share counts and cost
stocks_info = {
    '600352': ('浙江龙盛', 15.952, 12.0, 106700, 'main'),
    '300033': ('同花顺', 423.488, 280.0, 1200, 'main'),
    '688295': ('中复神鹰', 37.843, 0, 1500, 'main'),
    '600487': ('亨通光电', 42.391, 0, 2000, 'main'),
    '300499': ('高澜股份', 41.625, 38.0, 1500, 'main'),
    '601168': ('西部矿业', 24.863, 0, 2000, 'main'),
    '600893': ('航发动力', 47.196, 0, 1000, 'main'),
    '920046': ('亿能电力', 329.555, 27.0, 200, 'main'),
    '600114': ('东睦股份', 25.9, 25.0, 4800, 'wife'),
    '301638': ('南网数字', 32.635, 28.0, 1700, 'wife'),
    '600089': ('特变电工', 24.765, 25.0, 52300, 'margin'),
}

# Query all at once
url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
secids = ','.join(['1.'+c for c in stocks_info.keys()])
params = {
    'fltt': 2,
    'invt': 2,
    'fields': 'f1,f2,f3,f4,f12,f14',
    'secids': secids
}

try:
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    items = data.get('data', {}).get('diff', [])
    
    print('=== 持仓监控 {} ==='.format('15:15'))
    print('')
    
    total_pnl = 0
    alerts = []
    missing = []
    
    for item in items:
        code = item['f12']
        if code not in stocks_info:
            continue
        
        name, cost, stop, shares, account = stocks_info[code]
        price_val = item['f2']
        chg_pct = item['f3']
        
        if price_val == '-' or price_val == 0:
            price_f = 0
            chg_pct_f = 0
            pnl = 0
            status = '[停牌]'
        else:
            price_f = float(price_val)
            chg_pct_f = float(chg_pct) if chg_pct != '-' else 0
            pnl = (price_f - cost) * shares
            
            if stop > 0 and price_f <= stop:
                status = '[!!止损触发!!]'
                alerts.append('{} 现价={:.3f} 止损={:.1f} 需操作!'.format(name, price_f, stop))
            elif stop > 0 and price_f <= stop * 1.03:
                status = '[!接近止损]'
                alerts.append('{} 现价={:.3f} 止损={:.1f} 接近触发!'.format(name, price_f, stop))
            elif price_f < cost * 0.97:
                status = '[!亏损扩大]'
                alerts.append('{} 现价={:.3f} vs 成本={:.3f}'.format(name, price_f, cost))
            elif chg_pct_f < -3:
                status = '[!跌幅较大]'
                alerts.append('{} 跌幅 {:.2f}%，现价={:.3f}'.format(name, chg_pct_f, price_f))
            elif chg_pct_f > 5:
                status = '[**大涨**]'
            else:
                status = ''
        
        total_pnl += pnl
        chg_str = '{:+.2f}%'.format(chg_pct_f) if chg_pct != '-' else '-'
        stop_str = '{:.1f}'.format(stop) if stop > 0 else '-'
        
        if price_f > 0:
            print('{:<14} {:>8.3f} {:>8} {:>7.3f} {:>6} {:>7} {:>+12.1f} {}'.format(
                name, price_f, chg_str, cost, stop_str, shares, pnl, status))
    
    print('-' * 90)
    print('{:<70} {:>+12.1f} 元'.format('合计浮动盈亏', total_pnl))
    
    if alerts:
        print('')
        print('=== 预警 ({}) ==='.format(len(alerts)))
        for a in alerts:
            print('  - ' + a)
    
except Exception as e:
    print('Error: {}'.format(e))
    import traceback
    traceback.print_exc()
