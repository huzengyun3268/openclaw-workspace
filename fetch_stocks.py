# -*- coding: utf-8 -*-
import urllib.request
import json

codes = 'sh600352,sz300033,sh600487,sh600893,sh601168,sh518880,sz430046,sh600114,sh600089'
url = f'http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids={codes}'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
r = urllib.request.urlopen(req, timeout=10)
data = json.loads(r.read().decode('utf-8'))

stocks_info = {
    'sh600352': ('浙江龙盛', 16.948, 12.0, 76700, '主账户'),
    'sz300033': ('同花顺', 423.488, 280.0, 1200, '主账户'),
    'sh600487': ('亨通光电', 43.210, 38.0, 3000, '主账户'),
    'sh600893': ('航发动力', 49.184, 42.0, 9000, '主账户'),
    'sh601168': ('西部矿业', 26.169, 22.0, 11000, '主账户'),
    'sh518880': ('黄金ETF', 9.868, 0.0, 24000, '主账户'),
    'sz430046': ('圣博润', 0.478, 0.0, 10334, '主账户'),
    'sh600114': ('东睦股份', 31.176, 25.0, 11100, '老婆账户'),
    'sh600089': ('特变电工', 24.765, 25.0, 52300, '两融账户'),
}

items = data.get('data', {}).get('diff', [])
total_pnl = 0
alerts = []

for item in items:
    code = item.get('f12', '')
    price = item.get('f2', 0)
    chg_pct = item.get('f3', 0)
    chg_amt = item.get('f4', 0)
    
    if code in stocks_info:
        name, cost, stop, qty, account = stocks_info[code]
        if price > 0:
            pnl = (price - cost) * qty
            total_pnl += pnl
            flag = ''
            if stop > 0 and price <= stop:
                flag = ' [止损!]'
            print(f'{name}({code}) [{account}]: {price}  {chg_pct:+.2f}%  盈亏:{pnl:+.0f}元{flag}')
        else:
            print(f'{name}({code}): 无数据')
    else:
        print(f'{code}: {price}  {chg_pct:+.2f}%')

print(f'\n当日估算总盈亏: {total_pnl:+.0f}元')
