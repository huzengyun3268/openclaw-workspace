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
stop_loss = {
    'sh600352': 12.0, 'sz300033': 280.0, 'sz000988': None,
    'sh688295': None, 'sh600487': None, 'sz300499': 38.0,
    'sh601168': None, 'sh600893': None, 'bj920046': 27.0,
    'sh600114': 25.0, 'sz301638': 28.0,
}

lines_out.append('=== 持仓个股集合竞价快照 ===')
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
    
    # 确认字段: [1]=名称 [2]=代码 [3]=当前价 [4]=昨收 [5]=涨跌 [6]=涨跌幅 [30]=时间
    # [9]=买一价 [10]=买一量 [11]=卖一价 [12]=卖一量 [19]=卖五价 [20]=卖五量
    code = fields[2]
    name = stocks.get(code, fields[1])
    curr = fields[3]       # 当前价/理论开价
    yest = fields[4]       # 昨收
    chg = fields[5]        # 涨跌(当日变化)
    pct = fields[6]        # 涨跌幅%
    buy1_p = fields[9]     # 买一价
    buy1_v = fields[10]    # 买一量
    sell1_p = fields[11]   # 卖一价
    sell1_v = fields[12]   # 卖一量
    upd_time = fields[30] if len(fields) > 30 else ''
    
    try:
        curr_f = float(curr)
        yest_f = float(yest)
        chg_f = float(chg)
        pct_f = float(pct)
        cost_f = cost.get(code, 0)
        sl_f = stop_loss.get(code, None)
        buy1_f = float(buy1_p)
        buy1_vol = int(float(buy1_v)) if buy1_v else 0
        sell1_f = float(sell1_p)
        sell1_vol = int(float(sell1_v)) if sell1_v else 0
        
        # 竞价方向
        direction = ''
        if yest_f > 0 and curr_f > 0:
            gap = curr_f - yest_f
            gap_pct = gap / yest_f * 100
            if abs(gap) < 0.005:
                direction = '平开'
            elif gap > 0:
                direction = f'高开+{gap:.2f}(+{gap_pct:.2f}%)'
            else:
                direction = f'低开{gap:.2f}({gap_pct:.2f}%)'
        
        # 竞价状态: 卖一=0表示竞价未结束，无实际成交
        auction_done = sell1_f > 0 and sell1_vol > 0
        
        # 浮亏
        if cost_f > 0 and curr_f > 0:
            pl_val = (curr_f - cost_f)
            pl_pct = pl_val / cost_f * 100
            pl_str = f'浮{pl_val:+.2f}({pl_pct:+.1f}%)'
        else:
            pl_str = ''
        
        # 止损提醒
        alert = ''
        if sl_f and curr_f > 0 and curr_f <= sl_f:
            alert = ' ⚠️触及止损!'
        
        # 显示格式
        time_fmt = f'{upd_time[8:10]}:{upd_time[10:12]}:{upd_time[12:14]}' if len(upd_time) >= 14 else ''
        
        if not auction_done:
            lines_out.append(f'{name}: 竞价价={curr_f}({direction}) 时间={time_fmt} [{pl_str}]{alert}')
        else:
            lines_out.append(f'{name}: {curr_f}({pct_f:+.2f}%) {direction} [{pl_str}]{alert}')
    except Exception as e:
        lines_out.append(f'{name}|解析失败: {e}')

import datetime
lines_out.append('')
lines_out.append(f'采集: {datetime.datetime.now().strftime("%H:%M:%S")}')

with open(outfile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print("OK")
