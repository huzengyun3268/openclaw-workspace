import requests
import json

# All holdings with actual share counts
# Main account (3293)
main_stocks = {
    '600352': ('浙江龙盛', 15.952, 12.0, 106700),
    '300033': ('同花顺', 423.488, 280.0, 1200),
    '688295': ('中复神鹰', 37.843, 0, 1500),
    '600487': ('亨通光电', 42.391, 0, 2000),
    '300499': ('高澜股份', 41.625, 38.0, 1500),
    '601168': ('西部矿业', 24.863, 0, 2000),
    '600893': ('航发动力', 47.196, 0, 1000),
    '600089': ('特变电工(两融)', 24.765, 25.0, 52300),
}

# Wife account (3293)
wife_stocks = {
    '600114a': ('东睦股份(老仓)', 32.428, 0, 200),
    '600114b': ('东睦股份(新仓)', 25.9, 25.0, 4600),
    '301638': ('南网数字', 32.635, 28.0, 1700),
}

all_stocks = {**main_stocks, **wife_stocks}

# Batch query using eastmoney API
url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
secids = '1.600352,1.300033,1.688295,1.600487,1.300499,1.601168,1.600893,1.600089,1.600114,1.301638'
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
    
    # Use ASCII-safe status indicators
    print('{:<16} {:>7} {:>8} {:>7} {:>6} {:>7} {:>10} {}'.format(
        '名称', '现价', '涨跌幅', '成本', '止损', '持仓', '盈亏额', '状态'))
    print('-' * 85)
    
    total_pnl = 0
    alerts = []
    
    for item in items:
        code = item['f12']
        matched_key = None
        for k in all_stocks:
            if k.startswith(code):
                matched_key = k
                break
        
        if not matched_key:
            continue
            
        name, cost, stop, shares = all_stocks[matched_key]
        price_val = item['f2']
        chg_pct = item['f3']
        
        if price_val == '-' or price_val == 0:
            status = '[停牌]'
            price_f = 0
            pnl = 0
        else:
            price_f = float(price_val)
            chg_pct_f = float(chg_pct) if chg_pct != '-' else 0
            pnl = (price_f - cost) * shares
            
            if stop > 0 and price_f <= stop:
                status = '[!!止损!!]'
                alerts.append(f"{name} 触及止损价 {stop}，现价 {price_f}")
            elif price_f < cost * 0.95:
                status = '[!接近成本]'
                alerts.append(f"{name} 接近成本价 {cost}，现价 {price_f}")
            elif chg_pct_f < -3:
                status = '[!大跌]'
                alerts.append(f"{name} 大幅下跌 {chg_pct_f:.2f}%，现价 {price_f}")
            elif chg_pct_f > 5:
                status = '[**大涨**]'
            else:
                status = ''
        
        total_pnl += pnl
        chg_str = '{:+.2f}%'.format(chg_pct_f) if chg_pct != '-' else '-'
        stop_str = '{:.1f}'.format(stop) if stop > 0 else '-'
        print('{:<16} {:>7.3f} {:>8} {:>7.3f} {:>6} {:>7} {:>+10.1f} {}'.format(
            name, price_f, chg_str, cost, stop_str, shares, pnl, status))
    
    print('-' * 85)
    print('{:<65} {:>+10.1f} 元'.format('合计浮动盈亏', total_pnl))
    
    if alerts:
        print('\n=== 预警 ===')
        for a in alerts:
            print('  ' + a)
    
except Exception as e:
    print('Error: {}'.format(e))
    import traceback
    traceback.print_exc()
