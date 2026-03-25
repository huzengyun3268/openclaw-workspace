# -*- coding: utf-8 -*-
import urllib.request
import json
import os

outfile = r'C:\Users\Administrator\.openclaw\workspace\auction_out.txt'

def get_data(codes):
    url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk')
    return raw

lines_out = []

# Index
codes = ['sh000001','sz399001','sz399006','sh000688','sh000300']
data = get_data(codes)
lines = data.strip().split(';')
idx_names = {'sh000001':'0','sz399001':'1','sz399006':'2','sh000688':'3','sh000300':'4'}
idx_labels = ['上证指数','深证成指','创业板指','科创50','沪深300']

lines_out.append('=== INDEX ===')
for line in lines:
    if '=' not in line:
        continue
    content = line.split('=',1)[1].strip().strip('"').strip(';')
    if not content:
        continue
    parts = content.split('~')
    if len(parts) < 32:
        continue
    code = parts[2]
    label = idx_labels[list(idx_names.keys()).index(code)] if code in idx_names else code
    # 字段: 0=类型,1=name,2=code,3=当前价,4=昨收,5=... 
    curr = parts[3] if parts[3] else '0'
    yest = parts[4] if parts[4] else '0'
    open_p = parts[1] if parts[1] else '0'
    upd_time = parts[30] if len(parts) > 30 else ''
    try:
        curr_f = float(curr)
        yest_f = float(yest)
        if yest_f > 0:
            pct = (curr_f - yest_f) / yest_f * 100
        else:
            pct = 0
        lines_out.append(f'{label}|{curr}|{yest}|{curr_f-yest_f:+.2f}|{pct:+.2f}%|time:{upd_time}')
    except:
        lines_out.append(f'{label}|curr={curr}|yest={yest}')

# Stocks
stocks = {
    'sh600352':'浙江龙盛','sz300033':'同花顺','sz000988':'华工科技',
    'sh688295':'中复神鹰','sh600487':'亨通光电','sz300499':'高澜股份',
    'sh601168':'西部矿业','sh600893':'航发动力','bj920046':'亿能电力',
    'sh600114':'东睦股份','sz301638':'南网数字',
}
lines_out.append('')
lines_out.append('=== STOCKS ===')
sdata = get_data(list(stocks.keys()))
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
    yest = parts[4] if parts[4] else '0'
    curr = parts[3] if parts[3] else '0'
    open_p = parts[1] if parts[1] else '0'
    vol = parts[6] if parts[6] else '0'
    amount = parts[37] if parts[37] else '0'
    
    try:
        curr_f = float(curr)
        yest_f = float(yest)
        open_f = float(open_p)
        vol_f = float(vol)
        amount_f = float(amount)
        
        if yest_f > 0 and curr_f > 0:
            pct = (curr_f - yest_f) / yest_f * 100
            chg_f = curr_f - yest_f
            price_use = curr_f
        elif yest_f > 0 and open_f > 0:
            pct = (open_f - yest_f) / yest_f * 100
            chg_f = open_f - yest_f
            price_use = open_f
        else:
            pct = 0
            chg_f = 0
            price_use = 0
        
        direction = ''
        if open_f > 0 and yest_f > 0:
            diff = open_f - yest_f
            if abs(diff) < 0.005:
                direction = 'flat'
            elif diff > 0:
                direction = f'gap_up+{diff:.2f}'
            else:
                direction = f'gap_down{diff:.2f}'
        
        vol_str = f'{vol_f/10000:.1f}wan' if vol_f >= 10000 else f'{vol_f/100:.0f}bai'
        amt_str = f'{amount_f/1e8:.2f}y' if amount_f >= 1e8 else f'{amount_f/1e4:.0f}wan'
        
        lines_out.append(f'{name}({code})|{price_use:.2f}|{pct:+.2f}%|{chg_f:+.2f}|{open_f:.2f}|{direction}|{vol_str}|{amt_str}')
    except Exception as e:
        lines_out.append(f'{name}({code})|ERR:{e}')

import datetime
lines_out.append('')
lines_out.append(f'TIME: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

with open(outfile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print("Done")
