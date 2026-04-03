# -*- coding: utf-8 -*-
import requests
import json

# Holdings: (eastmoney code, name, shares, cost, stop_loss, account)
holdings = [
    ('600352', '浙江龙盛', 76700, 16.948, 12.0, 'main'),
    ('300033', '同花顺', 1200, 423.488, 280, 'main'),
    ('600487', '亨通光电', 3000, 43.210, 38.0, 'main'),
    ('600893', '航发动力', 9000, 49.184, 42.0, 'main'),
    ('601168', '西部矿业', 11000, 26.169, 22.0, 'main'),
    ('518880', '黄金ETF', 24000, 9.868, 0, 'main'),
    ('831330', '普适导航', 7370, 20.361, 18.0, 'main'),
    ('430046', '圣博润', 10334, 0.478, 0, 'main'),
    ('600114', '东睦股份', 11100, 31.176, 25.0, 'wife'),
    ('600089', '特变电工', 52300, 24.765, 25.0, 'margin'),
]

# Build secid list for eastmoney
secids = []
for code, name, shares, cost, stop, account in holdings:
    if code.startswith('6'):
        secids.append(f'1.{code}')
    elif code.startswith('4') or code.startswith('8'):
        secids.append(f'0.{code}')
    else:
        secids.append(f'0.{code}')

# Fetch from eastmoney
url = 'https://push2.eastmoney.com/api/qt/ulist.np/get'
params = {
    'fltt': 2,
    'invt': 2,
    'fields': 'f12,f14,f2,f3,f4,f5,f6',
    'secids': ','.join(secids)
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://quote.eastmoney.com/'
}

try:
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    data = resp.json()
    prices = {}
    for item in data.get('data', {}).get('diff', []):
        code = item['f12']
        prices[code] = {
            'price': item['f2'] / 1000 if item['f2'] else 0,
            'change_pct': item['f3'] / 100 if item['f3'] else 0,
            'prev_close': item['f4'] / 1000 if item['f4'] else 0,
            'volume': item['f5'] or 0,
            'amount': item['f6'] or 0,
        }
    
    results = []
    for code, name, shares, cost, stop, account in holdings:
        if code in prices:
            p = prices[code]
            pnl = (p['price'] - cost) * shares
            results.append({
                'name': name, 'code': code, 'price': p['price'],
                'cost': cost, 'change_pct': p['change_pct'],
                'pnl': pnl, 'stop': stop, 'account': account
            })
        else:
            print(f'No data for {name}({code})')
    
    results.sort(key=lambda x: (x['account'], x['pnl']))
    
    print('\n=== 持仓监控 13:30 ===')
    total_pnl = 0
    current_account = ''
    for r in results:
        if r['account'] != current_account:
            if current_account:
                print()
            if r['account'] == 'main':
                print('【主账户3293】')
            elif r['account'] == 'wife':
                print('【老婆账户】')
            elif r['account'] == 'margin':
                print('【两融账户2306】')
            current_account = r['account']
        stop_signal = ' ⚠️止损' if r['stop'] > 0 and r['price'] <= r['stop'] else ''
        stop_near = ' ⚠️接近止损' if r['stop'] > 0 and r['price'] <= r['stop'] * 1.05 and r['price'] > r['stop'] else ''
        print(f"  {r['name']} 现价:{r['price']:.3f} 涨跌:{r['change_pct']:+.2f}% 盈亏:{r['pnl']:+.0f}元{stop_signal}{stop_near}")
        total_pnl += r['pnl']
    
    print(f'\n合计盈亏: {total_pnl:+.0f}元')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
