# -*- coding: utf-8 -*-
import requests, json, sys
sys.stdout.reconfigure(encoding='utf-8')

positions = [
    {'code': '600089', 'name': '特变电工', 'shares': 52300, 'cost': 24.765, 'market': 'sh'},
    {'code': '600352', 'name': '浙江龙盛', 'shares': 106700, 'cost': 15.912, 'market': 'sh'},
    {'code': '301667', 'name': '纳百川', 'shares': 3000, 'cost': 82.715, 'market': 'sz'},
    {'code': '300033', 'name': '同花顺', 'shares': 600, 'cost': 511.22, 'market': 'sz'},
    {'code': '300189', 'name': '神农种业', 'shares': 5000, 'cost': 17.099, 'market': 'sz'},
    {'code': '920046', 'name': '亿能电力', 'shares': 12731, 'cost': 35.936, 'market': 'bj'},
    {'code': '831330', 'name': '普适导航', 'shares': 6370, 'cost': 20.415, 'market': 'bj'},
    {'code': '430046', 'name': '圣博润', 'shares': 10334, 'cost': 0.478, 'market': 'bj'},
    {'code': '600114', 'name': '东睦股份(老婆)', 'shares': 9200, 'cost': 32.428, 'market': 'sh'},
    {'code': '301638', 'name': '南网数字(老婆)', 'shares': 1700, 'cost': 32.635, 'market': 'sz'},
]

market_map = {'sh': '1.', 'sz': '0.', 'bj': '0.'}
secids = ','.join(market_map[p['market']] + p['code'] for p in positions)
url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&secids={secids}&fields=f2,f3,f4,f12,f14'
r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
raw = r.json()['data']['diff']

price_map = {item['f12']: item for item in raw}

alerts = []
for pos in positions:
    code = pos['code']
    item = price_map.get(code)
    if not item: continue
    price = item['f2']
    chg = item['f3']
    chg_pct = item['f4']
    cost = pos['cost']
    shares = pos['shares']
    profit_pct = (price - cost) / cost * 100
    alert = ''
    if chg_pct >= 3:
        alert = '🚀 涨幅警示'
    elif chg_pct <= -5:
        alert = '🚨 紧急下跌'
    elif chg_pct <= -3:
        alert = '⚠️ 下跌警示'
    if profit_pct >= 10:
        alert = '💰 大幅盈利'
    elif profit_pct <= -10:
        alert = '🔴 深度亏损'
    if alert:
        alerts.append({'name': pos['name'], 'code': code, 'price': price, 'chg_pct': chg_pct, 'profit_pct': profit_pct, 'alert': alert})
        print(f"{alert} {pos['name']}({code}) 现价={price} 今日涨跌={chg_pct:+.2f}% 持仓盈亏={profit_pct:+.1f}%")

print(f"TOTAL_ALERTS:{len(alerts)}")
