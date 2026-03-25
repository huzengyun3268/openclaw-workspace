# -*- coding: utf-8 -*-
import urllib.request

def get_data(codes):
    url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    raw = resp.read().decode('gbk')
    return raw

outfile = r'C:\Users\Administrator\.openclaw\workspace\auction_out.txt'
lines_out = []

# ===== 指数 =====
idx_names = {'sh000001':'上证','sz399001':'深证','sz399006':'创业板','sh000688':'科创50','sh000300':'沪深300'}
idx_codes = list(idx_names.keys())
lines_out.append('=== 指数行情 ===')
idx_data = get_data(idx_codes)
for line in idx_data.strip().split(';'):
    if '=' not in line:
        continue
    content = line.split('=',1)[1].strip().strip('"').strip(';')
    if not content:
        continue
    fields = content.split('~')
    if len(fields) < 35:
        continue
    code = 'sh' + fields[2] if fields[2].startswith('0') else 'sz' + fields[2]
    name = idx_names.get(code, fields[1])
    curr = float(fields[3]) if fields[3] else 0
    yest = float(fields[4]) if fields[4] else 0
    pct = float(fields[6]) if fields[6] else 0
    upd = fields[30] if len(fields) > 30 else ''
    t_str = f'{upd[8:10]}:{upd[10:12]}:{upd[12:14]}' if len(upd) >= 14 else ''
    gap = curr - yest if yest > 0 else 0
    gap_pct = gap / yest * 100 if yest > 0 else 0
    if abs(gap) < 0.005:
        gap_str = '平开'
    elif gap > 0:
        gap_str = f'高开+{gap:.2f}(+{gap_pct:.2f}%)'
    else:
        gap_str = f'低开{gap:.2f}({gap_pct:.2f}%)'
    lines_out.append(f'{name}: {curr} ({pct:+.2f}%) {gap_str} [{t_str}]')

# ===== 涨跌停统计 =====
lines_out.append('')
lines_out.append('=== 市场情绪 ===')

# 北向+大盘股统计用东方财富
import requests
headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://finance.eastmoney.com/"}
try:
    url_em = "http://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": 1, "pz": 1, "po": 1, "np": 1,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": 2, "invt": 2, "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
        "fields": "f12",
    }
    r = requests.get(url_em, params=params, headers=headers, timeout=8)
    total = r.json().get("data",{}).get("total",0)
    
    # 涨停
    p2 = dict(params); p2["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=9.9"
    r2 = requests.get(url_em, params=p2, headers=headers, timeout=8)
    zt = r2.json().get("data",{}).get("total",0)
    
    # 跌停
    p3 = dict(params); p3["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=-9.9"
    r3 = requests.get(url_em, params=p3, headers=headers, timeout=8)
    dt = r3.json().get("data",{}).get("total",0)
    
    # 上涨
    p4 = dict(params); p4["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=0"
    r4 = requests.get(url_em, params=p4, headers=headers, timeout=8)
    up = r4.json().get("data",{}).get("total",0)
    
    # 下跌
    p5 = dict(params); p5["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=0"
    r5 = requests.get(url_em, params=p5, headers=headers, timeout=8)
    dn = r5.json().get("data",{}).get("total",0)
    
    flat = total - up - dn
    lines_out.append(f'上涨:{up} 下跌:{dn} 平:{flat} 涨停:{zt} 跌停:{dt} (采样{total})')
except Exception as e:
    lines_out.append(f'涨跌停数据获取失败: {e}')

# ===== 持仓个股 =====
stocks = {
    'sh600352':'浙江龙盛','sz300033':'同花顺','sz000988':'华工科技',
    'sh688295':'中复神鹰','sh600487':'亨通光电','sz300499':'高澜股份',
    'sh601168':'西部矿业','sh600893':'航发动力','bj920046':'亿能电力',
    'sh600114':'东睦股份','sz301638':'南网数字',
}
cost = {
    'sh600352': 15.952, 'sz300033': 423.488, 'sz000988': 116.87,
    'sh688295': 37.843, 'sh600487': 42.391, 'sz300499': 41.625,
    'sh601168': 24.863, 'sh600893': 47.196, 'bj920046': 329.555,
    'sh600114': 32.428, 'sz301638': 32.635,
}
stop_loss = {
    'sh600352': 12.0, 'sz300033': 280.0, 'sz000988': None,
    'sh688295': None, 'sh600487': None, 'sz300499': 38.0,
    'sh601168': None, 'sh600893': None, 'bj920046': 27.0,
    'sh600114': 25.0, 'sz301638': 28.0,
}

lines_out.append('')
lines_out.append('=== 持仓个股竞价 ===')
sdata = get_data(list(stocks.keys()))
for line in sdata.strip().split(';'):
    if '=' not in line:
        continue
    content = line.split('=',1)[1].strip().strip('"').strip(';')
    if not content:
        continue
    fields = content.split('~')
    if len(fields) < 40:
        continue
    
    code = fields[2]
    name = stocks.get(code, fields[1])
    curr_f = float(fields[3]) if fields[3] else 0
    yest_f = float(fields[4]) if fields[4] else 0
    pct_f = float(fields[6]) if fields[6] else 0
    buy1_f = float(fields[9]) if fields[9] else 0
    buy1_vol = int(float(fields[10])) if fields[10] else 0
    sell1_f = float(fields[11]) if fields[11] else 0
    sell1_vol = int(float(fields[12])) if fields[12] else 0
    upd = fields[30] if len(fields) > 30 else ''
    t_str = f'{upd[8:10]}:{upd[10:12]}' if len(upd) >= 12 else ''
    
    cost_f = cost.get(code, 0)
    sl_f = stop_loss.get(code, None)
    
    # 竞价方向
    gap = curr_f - yest_f if yest_f > 0 else 0
    gap_pct = gap / yest_f * 100 if yest_f > 0 else 0
    if abs(gap) < 0.005:
        direction = '平开'
    elif gap > 0:
        direction = f'高开+{gap:.2f}(+{gap_pct:.1f}%)'
    else:
        direction = f'低开{gap:.2f}({gap_pct:.1f}%)'
    
    # 竞价完成判断
    auction_done = sell1_f > 0 and sell1_vol > 0
    
    # 浮亏
    if cost_f > 0 and curr_f > 0:
        pl_val = (curr_f - cost_f)
        pl_pct = pl_val / cost_f * 100
        pl_str = f'浮{pl_val:+.2f}({pl_pct:+.1f}%)'
    else:
        pl_str = ''
    
    # 止损预警
    alert = ''
    if sl_f and curr_f > 0 and curr_f <= sl_f:
        alert = ' ⚠️止损价!'
    elif sl_f and curr_f > 0 and curr_f <= sl_f * 1.02:
        alert = ' ⚠️接近止损!'
    
    # 竞价未完成
    if not auction_done:
        lines_out.append(f'{name}: 竞价{curr_f}({direction}) [{pl_str}]{alert}')
    else:
        lines_out.append(f'{name}: {curr_f}({pct_f:+.2f}%) {direction} [{pl_str}]{alert}')

import datetime
lines_out.append('')
lines_out.append(f'采集时间: {datetime.datetime.now().strftime("%H:%M:%S")}')

with open(outfile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print("OK")
