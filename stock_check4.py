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
    
    print(f"{'名称':<16} {'现价':>7} {'涨跌幅':>8} {'成本':>7} {'止损':>6} {'持仓':>7} {'盈亏额':>10} {'状态'}")
    print('-' * 85)
    
    total_pnl = 0
    
    for item in items:
        code = item['f12']
        # Match to our stocks
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
            status = '停牌'
            price_f = 0
            pnl = 0
        else:
            price_f = float(price_val)
            chg_pct_f = float(chg_pct) if chg_pct != '-' else 0
            pnl = (price_f - cost) * shares
            
            if stop > 0 and price_f <= stop:
                status = '⚠️触及止损'
            elif price_f < cost * 0.95:
                status = '⚠️接近成本'
            elif chg_pct_f < -3:
                status = '⚠️大幅下跌'
            elif chg_pct_f > 5:
                status = '🔥大涨'
            else:
                status = '正常'
        
        total_pnl += pnl
        chg_str = f"{chg_pct_f:+.2f}%" if chg_pct != '-' else '-'
        stop_str = f"{stop:.1f}" if stop > 0 else '-'
        print(f"{name:<16} {price_f:>7.3f} {chg_str:>8} {cost:>7.3f} {stop_str:>6} {shares:>7} {pnl:>+10.1f} {status}")
    
    print('-' * 85)
    print(f"{'合计浮动盈亏':>65} {total_pnl:>+10.1f} 元")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
