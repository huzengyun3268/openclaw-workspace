# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
import pandas as pd
from datetime import datetime

# Holdings data
positions = [
    # Main account
    {'账号': '主账户', '股票': '浙江龙盛', 'code': '600352', '持仓': 106700, '成本': 15.952, '备注': '止损12.0'},
    {'账号': '主账户', '股票': '同花顺', 'code': '300033', '持仓': 1200, '成本': 423.488, '备注': '止损280'},
    {'账号': '主账户', '股票': '普适导航', 'code': '831330', '持仓': 7370, '成本': 20.361, '备注': '新三板'},
    {'账号': '主账户', '股票': '华工科技', 'code': '000988', '持仓': 1000, '成本': 116.87, '备注': ''},
    {'账号': '主账户', '股票': '中复神鹰', 'code': '688295', '持仓': 1500, '成本': 37.843, '备注': '科创板'},
    {'账号': '主账户', '股票': '亨通光电', 'code': '600487', '持仓': 2000, '成本': 42.391, '备注': ''},
    {'账号': '主账户', '股票': '高澜股份', 'code': '300499', '持仓': 1500, '成本': 41.625, '备注': '止损38.0'},
    {'账号': '主账户', '股票': '西部矿业', 'code': '601168', '持仓': 2000, '成本': 24.863, '备注': ''},
    {'账号': '主账户', '股票': '航发动力', 'code': '600893', '持仓': 1000, '成本': 47.196, '备注': ''},
    {'账号': '主账户', '股票': '亿能电力', 'code': '920046', '持仓': 200, '成本': 329.555, '备注': '止损27'},
    {'账号': '主账户', '股票': '圣博润', 'code': '430046', '持仓': 10334, '成本': 0.478, '备注': '新三板'},
    # Wife account
    {'账号': '老婆账户', '股票': '东睦股份', 'code': '600114', '持仓': 4800, '成本': 26.7, '备注': '止损25.0'},
    {'账号': '老婆账户', '股票': '南网数字', 'code': '301638', '持仓': 1700, '成本': 32.635, '备注': '止损28.0'},
    # Margin account
    {'账号': '两融账户', '股票': '特变电工', 'code': '600089', '持仓': 52300, '成本': 24.765, '备注': '止损25.0'},
]

# Use eastmoney realtime API
url = 'https://push2.eastmoney.com/api/qt/ulist.np/get'
codes_str = ','.join([f'{p["code"]}{"SH" if p["code"].startswith("6") else "SZ" if not p["code"].startswith(("4","8","9")) else "BJ"}' for p in positions])

# Build secids
secids = []
for p in positions:
    code = p['code']
    if code.startswith('6'):
        secids.append(f'1.{code}')
    elif code.startswith('0') or code.startswith('3'):
        secids.append(f'0.{code}')
    elif code.startswith('4') or code.startswith('8'):
        secids.append(f'0.{code}')
    elif code.startswith('9'):
        secids.append(f'1.{code}')

secid_str = ','.join(secids)

params = {
    'secids': secid_str,
    'fields': 'f1,f2,f3,f4,f12,f14',
    'ut': 'b2884a393a59ad64002292a3e90d46a5',
    'fltt': '2',
    'invt': '2',
}

try:
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    
    price_map = {}
    if data.get('data') and data['data'].get('diff'):
        for item in data['data']['diff']:
            code = item.get('f12', '')
            price = item.get('f2')
            chg = item.get('f3')
            price_map[code] = {'price': price, 'chg': chg}
    
    print(f"Fetched {len(price_map)} prices")
    for p in positions:
        code = p['code']
        if code in price_map:
            p['现价'] = price_map[code]['price']
            p['涨跌%'] = price_map[code]['chg']
            p['盈亏'] = round((p['现价'] - p['成本']) * p['持仓'], 0)
            p['盈亏%'] = round((p['现价'] / p['成本'] - 1) * 100, 2)
        else:
            p['现价'] = 'N/A'
            p['涨跌%'] = 'N/A'
            p['盈亏'] = 'N/A'
            p['盈亏%'] = 'N/A'
    
    df = pd.DataFrame(positions)
    print(df[['账号','股票','现价','涨跌%','成本','盈亏','盈亏%','备注']].to_string(index=False))
    
    # Summary by account
    print("\n=== 分账号汇总 ===")
    accounts = {}
    for p in positions:
        acc = p['账号']
        if acc not in accounts:
            accounts[acc] = {'成本总额': 0, '盈亏': 0}
        if p['盈亏'] != 'N/A':
            accounts[acc]['成本总额'] += p['成本'] * p['持仓']
            accounts[acc]['盈亏'] += p['盈亏']
    for acc, v in accounts.items():
        pct = round(v['盈亏'] / v['成本总额'] * 100, 2) if v['成本总额'] else 0
        print(f"{acc}: 成本{v['成本总额']:,.0f}元  盈亏{v['盈亏']:,.0f}元({pct:+.2f}%)")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
