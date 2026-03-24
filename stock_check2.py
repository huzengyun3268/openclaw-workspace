# -*- coding: utf-8 -*-
import requests
from datetime import datetime

stocks = {
    '600352': ('浙江龙盛', 106700, 15.91),
    '600089': ('特变电工', 52300, 24.765),
    '301667': ('纳百川', 3000, 82.715),
    '920046': ('亿能电力', 12731, 35.936),
    '300033': ('同花顺', 600, 511.22),
    '831330': ('普适导航', 6370, 20.415),
    '300189': ('神农种业', 5000, 17.099),
    '430046': ('圣博润', 10334, 0.478),
    '600114': ('东睦股份_老婆', 9200, 32.428),
    '301638': ('南网数字_老婆', 1700, 32.635),
}

secids = []
for code in stocks:
    if code.startswith('6'):
        secids.append('1.' + code)
    else:
        secids.append('0.' + code)

secids_str = ','.join(secids)
url = 'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&secids=' + secids_str + '&fields=f2,f3,f12,f14'

try:
    resp = requests.get(url, timeout=15)
    data = resp.json()
except Exception as e:
    print('API请求失败: ' + str(e))
    exit(1)

print('时间: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print('='*80)

price_map = {}
if data.get('data') and data['data'].get('diff'):
    for item in data['data']['diff']:
        code = item.get('f12', '')
        price = item.get('f2')
        change_pct = item.get('f3')
        price_map[code] = {'price': price, 'change_pct': change_pct}

total_profit = 0.0
total_cost = 0.0
total_value = 0.0

for code, info in stocks.items():
    name = info[0]
    qty = info[1]
    cost = info[2]
    if code in price_map:
        p = price_map[code]['price']
        chg = price_map[code]['change_pct']
        if p is not None and p > 0:
            profit = (p - cost) * qty
            profit_pct = (p / cost - 1) * 100
            total_profit += profit
            total_cost += cost * qty
            total_value += p * qty
            sign = '+' if profit >= 0 else ''
            print('%s(%s): 现价=%.3f 涨跌=%+.2f%% 持仓=%d股 成本=%.3f 盈亏=%s%.0f(%s%.1f%%)' % (name, code, p, chg, qty, cost, sign, profit, sign, profit_pct))
        else:
            print(name + '(' + code + '): 无有效价格数据')
    else:
        print(name + '(' + code + '): 行情获取失败')

print('='*80)
if total_cost > 0:
    sign = '+' if total_profit >= 0 else ''
    print('总盈亏: %s%.0f元  总成本: %.0f元  总市值: %.0f元  收益率: %s%.2f%%' % (sign, total_profit, total_cost, total_value, sign, total_profit/total_cost*100))
