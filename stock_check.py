# -*- coding: utf-8 -*-
import requests
import json

# 腾讯财经API
codes = ['sh600352', 'sz300033', 'sh600487', 'sh600893', 'sh601168', 'sh518880', 'sz430046', 'sh600114', 'sh600089']
names = {'sh600352':'浙江龙盛', 'sz300033':'同花顺', 'sh600487':'亨通光电', 'sh600893':'航发动力', 'sh601168':'西部矿业', 'sh518880':'黄金ETF', 'sz430046':'圣博润', 'sh600114':'东睦股份', 'sh600089':'特变电工'}
cost = {'sh600352':16.948, 'sz300033':423.488, 'sh600487':43.210, 'sh600893':49.184, 'sh601168':26.169, 'sh518880':9.868, 'sz430046':0.478, 'sh600114':31.176, 'sh600089':24.765}
stop = {'sh600352':12.0, 'sz300033':280, 'sh600487':38.0, 'sh600893':42.0, 'sh601168':22.0, 'sh600114':25.0, 'sh600089':25.0}
holdings = {'sh600352':76700, 'sz300033':1200, 'sh600487':3000, 'sh600893':9000, 'sh601168':11000, 'sh518880':24000, 'sz430046':10334, 'sh600114':11100, 'sh600089':52300}

# 腾讯财经实时行情
url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
try:
    resp = requests.get(url, timeout=10)
    resp.encoding = 'gbk'
    lines = resp.text.strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        parts = line.split('~')
        if len(parts) < 32:
            continue
        code_raw = parts[0].replace('v_', '')
        price = float(parts[3])
        yesterday_close = float(parts[4])
        change_pct = (price - yesterday_close) / yesterday_close * 100 if yesterday_close else 0
        name = names.get(code_raw, parts[1])
        cost_price = cost.get(code_raw, 0)
        stop_price = stop.get(code_raw)
        hold = holdings.get(code_raw, 0)
        profit = (price - cost_price) * hold if cost_price else 0
        alert = ''
        if stop_price and price <= stop_price:
            alert = ' [!!触及止损]'
        elif stop_price and price <= cost_price * 1.01:
            alert = ' [警告接近成本]'
        status = '[+' if profit >= 0 else '[-'
        print(f'{name}({code_raw}): {price:.3f} {change_pct:+.2f}% 浮盈亏={profit:+.1f} {status}{alert}')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
