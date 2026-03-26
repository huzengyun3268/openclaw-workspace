import requests
import json

# Use eastmoney real-time API
codes = {
    '600352': ('浙江龙盛', 15.952, 12.0),
    '300033': ('同花顺', 423.488, 280.0),
    '688295': ('中复神鹰', 37.843, 0),
    '600487': ('亨通光电', 42.391, 0),
    '300499': ('高澜股份', 41.625, 38.0),
    '601168': ('西部矿业', 24.863, 0),
    '600893': ('航发动力', 47.196, 0),
    '600089': ('特变电工', 24.765, 25.0),
    '600114': ('东睦股份', 25.9, 25.0),
    '301638': ('南网数字', 32.635, 28.0),
}

# Batch query using eastmoney API
url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
params = {
    'fltt': 2,
    'invt': 2,
    'fields': 'f1,f2,f3,f4,f12,f14',
    'secids': ','.join([f'1.{k}' for k in codes.keys()])
}

try:
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    items = data.get('data', {}).get('diff', [])
    
    print(f"{'名称':<10} {'现价':>8} {'涨跌幅':>8} {'成本':>8} {'盈亏额':>10} {'止损价':>8} {'状态'}")
    print('-' * 75)
    
    for item in items:
        code = item['f12']
        name = codes[code][0]
        price = item['f2']
        chg_pct = item['f3']
        cost = codes[code][1]
        stop = codes[code][2]
        
        if price == '-':
            status = '停牌'
            pnl = 0
        else:
            price = float(price)
            chg_pct = float(chg_pct) if chg_pct != '-' else 0
            pnl = (price - cost) * 100  # approximate for 100 shares
            if price <= stop and stop > 0:
                status = '⚠️触及止损'
            elif price < cost * 0.95:
                status = '⚠️接近成本'
            elif chg_pct < -2:
                status = '⚠️跌幅较大'
            else:
                status = '正常'
        
        print(f"{name:<10} {price:>8} {chg_pct:>+7.2f}% {cost:>8.3f} {pnl:>+10.1f} {stop if stop else '-':>8} {status}")
        
except Exception as e:
    print(f"Error: {e}")
