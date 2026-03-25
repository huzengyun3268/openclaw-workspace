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

lines_out.append('=== 持仓个股集合竞价快照 09:23 ===')
sdata = get_data(list(stocks.keys()))
for line in sdata.strip().split(';'):
    if '=' not in line:
        continue
    parts = line.split('=',1)[1].strip().strip('"').strip(';')
    if not parts:
        continue
    fields = parts.split('~')
    if len(fields) < 38:
        continue
    
    # 字段映射(腾讯行情):
    # [1]=名称 [2]=代码 [3]=当前价 [4]=昨收 [5]=涨跌 [6]=涨跌幅% [7]=成交量(手)
    # [8]=成交额 [9]=买1价 [10]=买1量 [11]=卖1价 [12]=卖1量
    # ... [17]=买5价 [18]=买5量 [19]=卖5价 [20]=卖5量
    # [27]=日期 [30]=时间 [32]=状态(1=已成交)
    code = fields[2]
    name = stocks.get(code, fields[1])
    curr_str = fields[3]   # 当前价(集合竞价期间=成交价，竞价完成前=理论价)
    yest_str = fields[4]  # 昨收
    chg_str = fields[5]   # 涨跌额
    pct_str = fields[6]   # 涨跌幅%
    status_flag = fields[32] if len(fields) > 32 else '0'  # 1=已成交
    
    try:
        curr_f = float(curr_str)
        yest_f = float(yest_str)
        chg_f = float(chg_str)
        pct_f = float(pct_str)
        cost_f = cost.get(code, 0)
        status = int(status_flag) if status_flag.isdigit() else 0
        
        # 竞价方向判断: 当前价 vs 昨收
        direction = ''
        if yest_f > 0 and curr_f > 0:
            gap = curr_f - yest_f
            gap_pct = gap / yest_f * 100
            if abs(gap) < 0.005:
                direction = '平开'
            elif gap > 0:
                direction = f'高开+{gap:.2f}(+{gap_pct:.1f}%)'
            else:
                direction = f'低开{gap:.2f}({gap_pct:.1f}%)'
        
        # 盈亏
        if cost_f > 0 and curr_f > 0:
            pl_val = (curr_f - cost_f)
            pl_pct = pl_val / cost_f * 100
            pl_str = f'浮{pl_val:+.2f}({pl_pct:+.1f}%)'
        else:
            pl_str = ''
        
        # 状态
        if status == 0 and abs(pct_f) < 0.001 and yest_f == curr_f:
            price_line = f'竞价价={curr_f:.2f}'
        else:
            price_line = f'{curr_f:.2f}({pct_f:+.2f}%)'
        
        line_str = f'{name}: {price_line} {direction}'
        if pl_str:
            line_str += f' [{pl_str}]'
        lines_out.append(line_str)
    except Exception as e:
        lines_out.append(f'{name}|ERR:{e}')

import datetime
lines_out.append('')
lines_out.append(f'采集时间: {datetime.datetime.now().strftime("%H:%M:%S")}')

with open(outfile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print("OK")
