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

# 持仓: ~分隔
# 字段: 0=?,1=名称,2=代码,3=当前价,4=昨收,5=涨跌,6=涨跌幅,7=成交量(手),8=成交额(万?),37=成交额(元)
stocks = {
    'sh600352':'浙江龙盛','sz300033':'同花顺','sz000988':'华工科技',
    'sh688295':'中复神鹰','sh600487':'亨通光电','sz300499':'高澜股份',
    'sh601168':'西部矿业','sh600893':'航发动力','bj920046':'亿能电力',
    'sh600114':'东睦股份','sz301638':'南网数字',
}

# 成本价(来自USER.md)
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
    code = fields[2]
    name = stocks.get(code, fields[1])
    curr_str = fields[3]   # 当前价
    yest_str = fields[4]   # 昨收
    chg_str = fields[5]    # 涨跌
    pct_str = fields[6]    # 涨跌幅
    open_str = fields[1]   # 开盘价(集合竞价成交价)
    
    try:
        curr_f = float(curr_str)
        yest_f = float(yest_str)
        chg_f = float(chg_str)
        pct_f = float(pct_str)
        open_f = float(open_str)
        cost_f = cost.get(code, 0)
        
        # Gap analysis
        direction = ''
        if yest_f > 0 and open_f > 0:
            gap = open_f - yest_f
            gap_pct = gap / yest_f * 100
            if abs(gap) < 0.005:
                direction = '平开'
            elif gap > 0:
                direction = f'高开 +{gap:.2f}(+{gap_pct:.1f}%)'
            else:
                direction = f'低开 {gap:.2f}({gap_pct:.1f}%)'
        
        # P/L
        if cost_f > 0 and open_f > 0:
            pl_pct = (open_f - cost_f) / cost_f * 100
            pl_val = (open_f - cost_f)
            pl_str = f'浮:{pl_val:+.2f}({pl_pct:+.1f}%)'
        elif cost_f > 0 and curr_f > 0:
            pl_pct = (curr_f - cost_f) / cost_f * 100
            pl_val = (curr_f - cost_f)
            pl_str = f'浮:{pl_val:+.2f}({pl_pct:+.1f}%)'
        else:
            pl_str = ''
        
        # Price display
        if open_f > 0 and curr_f == 0:
            price_disp = open_f
            status = '竞价'
        elif curr_f > 0:
            price_disp = curr_f
            status = '成交'
        else:
            price_disp = open_f
            status = '竞价'
        
        if pct_f == 0 and yest_f == open_f:
            lines_out.append(f'{name}: 竞价{price_disp:.2f} {direction} [{pl_str}]')
        else:
            lines_out.append(f'{name}: {price_disp:.2f}({pct_f:+.2f}%) {direction} [{pl_str}]')
    except Exception as e:
        lines_out.append(f'{name}|ERR:{e}|{curr_str},{yest_str}')

import datetime
lines_out.append('')
lines_out.append(f'采集时间: {datetime.datetime.now().strftime("%H:%M:%S")}')

with open(outfile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print("OK")
