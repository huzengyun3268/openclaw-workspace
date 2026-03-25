# -*- coding: utf-8 -*-
import urllib.request
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_stock_data(codes):
    url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk')
    return raw

# Index
codes = ['sh000001','sz399001','sz399006','sh000688','sh000300']
data = get_stock_data(codes)
lines = data.strip().split(';')
idx_names = {'sh000001':'上证指数','sz399001':'深证成指','sz399006':'创业板指','sh000688':'科创50','sh000300':'沪深300'}
print('=== INDEX ===')
for line in lines:
    if '=' not in line:
        continue
    content = line.split('=',1)[1].strip().strip('"').strip(';')
    if not content:
        continue
    parts = content.split('~')
    if len(parts) < 35:
        continue
    code = parts[2]
    name = idx_names.get(code, parts[1])
    yest = float(parts[4]) if parts[4] else 0
    curr = float(parts[3]) if parts[3] else 0
    open_p = float(parts[1]) if parts[1] else 0
    time_str = parts[30] if len(parts) > 30 else ''
    print(f'{name}|{open_p}|{yest}|{time_str}')

# 持仓个股
print('=== STOCKS ===')
stocks = {
    'sh600352':'浙江龙盛','sz300033':'同花顺','sz000988':'华工科技',
    'sh688295':'中复神鹰','sh600487':'亨通光电','sz300499':'高澜股份',
    'sh601168':'西部矿业','sh600893':'航发动力','bj920046':'亿能电力',
    'sh600114':'东睦股份','sz301638':'南网数字',
}
sdata = get_stock_data(list(stocks.keys()))
slines = sdata.strip().split(';')
for line in slines:
    if '=' not in line:
        continue
    content = line.split('=',1)[1].strip().strip('"').strip(';')
    if not content:
        continue
    parts = content.split('~')
    if len(parts) < 38:
        continue
    code = parts[2]
    name = stocks.get(code, parts[1])
    yest = float(parts[4]) if parts[4] else 0
    curr = float(parts[3]) if parts[3] else 0
    open_p = float(parts[1]) if parts[1] else 0
    vol = float(parts[6]) if parts[6] else 0
    amount = float(parts[37]) if parts[37] else 0
    
    if yest > 0 and curr > 0:
        pct = (curr - yest) / yest * 100
    elif yest > 0 and open_p > 0:
        pct = (open_p - yest) / yest * 100
        curr = open_p
    else:
        pct = 0
    
    direction = ''
    if open_p > 0 and yest > 0:
        diff = open_p - yest
        if abs(diff) < 0.01:
            direction = 'flat'
        elif diff > 0:
            direction = f'up+{diff:.2f}'
        else:
            direction = f'down{diff:.2f}'
    
    vol_str = f'{vol/10000:.1f}wan' if vol >= 10000 else f'{vol/100:.0f}bai'
    amt_str = f'{amount/1e8:.2f}y' if amount >= 1e8 else f'{amount/1e4:.0f}wan'
    price_str = f'{curr:.2f}' if curr > 0 else f'{open_p:.2f}'
    print(f'{name}|{price_str}|{pct:+.2f}|{open_p:.2f}|{direction}|{vol_str}|{amt_str}')
