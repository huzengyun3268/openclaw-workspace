# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import json
from datetime import datetime

stocks = [
    ('浙江龙盛', 'sh600352', 16.948, 12.0, 76700, 'main'),
    ('同花顺', 'sz300033', 423.488, 280, 1200, 'main'),
    ('亨通光电', 'sh600487', 43.210, 38.0, 3000, 'main'),
    ('航发动力', 'sh600893', 49.184, 42.0, 9000, 'main'),
    ('西部矿业', 'sh601168', 26.169, 22.0, 11000, 'main'),
    ('黄金ETF', 'sh518880', 9.868, 0, 24000, 'main'),
    ('特变电工', 'sh600089', 24.765, 25.0, 52300, 'margin'),
    ('圣博润', 'sz430046', 0.478, 0, 10334, 'main'),
    ('东睦股份', 'sh600114', 31.176, 25.0, 11100, 'wife'),
]

# 腾讯行情API
codes = ','.join([s[1] for s in stocks])
url = f'https://qt.gtimg.cn/q={codes}'

try:
    resp = requests.get(url, timeout=10)
    resp.encoding = 'gb2312'
    lines = resp.text.strip().split('\n')
    
    print(f'=== 持仓监控 {datetime.now().strftime("%Y-%m-%d %H:%M")} ===')
    
    total_pnl = 0
    main_pnl = 0
    margin_pnl = 0
    wife_pnl = 0
    
    price_map = {}
    for line in lines:
        if '=' not in line:
            continue
        code_part = line.split('=')[0].replace('v_', '')
        data_str = line.split('=')[1].strip('"; ')
        fields = data_str.split('~')
        if len(fields) > 10:
            price_map[code_part] = fields
    
    for name, code, cost, stop, qty, account in stocks:
        if code not in price_map:
            print(f'  {name}({code}): N/A')
            continue
        
        fields = price_map[code]
        try:
            price = float(fields[3])
            yesterday_close = float(fields[4])
            change = price - yesterday_close
            change_pct = (change / yesterday_close * 100) if yesterday_close else 0
        except:
            print(f'  {name}({code}): parse error')
            continue
        
        pnl = (price - cost) * qty
        total_pnl += pnl
        if account == 'main':
            main_pnl += pnl
        elif account == 'margin':
            margin_pnl += pnl
        else:
            wife_pnl += pnl
        
        emoji = '🔴' if price < cost else '🟢'
        stop_str = f' 止损{stop}' if stop > 0 else ''
        stop_warn = ' ⚠️止损' if (stop > 0 and price <= stop) else ''
        print(f'{emoji} {name} {price:.3f} {change_pct:+.2f}% 盈亏{pnl:+.0f}元{stop_str}{stop_warn}')
    
    print()
    print(f'主账户盈亏: {main_pnl:+.0f}元')
    print(f'两融账户盈亏: {margin_pnl:+.0f}元')
    print(f'老婆账户盈亏: {wife_pnl:+.0f}元')
    print(f'总盈亏: {total_pnl:+.0f}元')
    
except Exception as e:
    print(f'Error: {e}')
