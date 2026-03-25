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

# 指数: 0=类型,1=名称,2=代码,3=当前价,4=昨收,5=涨跌,6=涨跌幅, ... 30=更新时间
codes_idx = ['sh000001','sz399001','sz399006','sh000688','sh000300']
idx_labels = ['上证指数','深证成指','创业板指','科创50','沪深300']

data_idx = get_data(codes_idx)
lines_out.append('=== 指数行情 ===')
for line in data_idx.strip().split(';'):
    if '=' not in line:
        continue
    parts = line.split('=',1)[1].strip().strip('"').strip(';')
    if not parts:
        continue
    fields = parts.split('~')
    if len(fields) < 10:
        continue
    code = fields[2]
    try:
        idx_i = codes_idx.index('sh'+code) if 'sh'+code in codes_idx else (codes_idx.index('sz'+code) if 'sz'+code in codes_idx else -1)
        name = idx_labels[idx_i] if idx_i >= 0 else fields[1]
    except:
        name = fields[1]
    curr = fields[3]
    yest = fields[4]
    chg = fields[5] if len(fields) > 5 else '0'
    pct = fields[6] if len(fields) > 6 else '0'
    time_str = fields[30] if len(fields) > 30 else ''
    try:
        curr_f = float(curr)
        yest_f = float(yest)
        chg_f = float(chg)
        pct_f = float(pct)
        if yest_f > 0 and curr_f == yest_f:
            lines_out.append(f'{name}: {curr_f}({pct_f:+.2f}%) [集合竞价中，暂无成交]')
        else:
            lines_out.append(f'{name}: {curr_f}({pct_f:+.2f}%) 时间:{time_str}')
    except:
        lines_out.append(f'{name}: curr={curr} yest={yest}')

# 持仓: 0=类型,1=名称,2=代码,3=当前价,4=昨收,5=涨跌,6=成交量(手),7=成交额, 9=买1价,10=买1量...
#      19=卖1价,20=卖1量... 37=成交额
stocks = {
    'sh600352':'浙江龙盛','sz300033':'同花顺','sz000988':'华工科技',
    'sh688295':'中复神鹰','sh600487':'亨通光电','sz300499':'高澜股份',
    'sh601168':'西部矿业','sh600893':'航发动力','bj920046':'亿能电力',
    'sh600114':'东睦股份','sz301638':'南网数字',
}

lines_out.append('')
lines_out.append('=== 持仓个股 ===')
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
    curr = fields[3]
    yest = fields[4]
    chg = fields[5] if len(fields) > 5 else '0'
    pct = fields[6] if len(fields) > 6 else '0'
    vol = fields[7] if len(fields) > 7 else '0'  # 手
    amount = fields[37] if len(fields) > 37 else '0'
    open_p = fields[1]  # 开盘
    
    try:
        curr_f = float(curr)
        yest_f = float(yest)
        open_f = float(open_p)
        vol_f = float(vol)
        amount_f = float(amount)
        chg_f = float(chg)
        pct_f = float(pct)
        
        # During call auction: curr=0, use open_p as reference
        price_ref = open_f if curr_f == 0 else curr_f
        if yest_f > 0 and price_ref > 0:
            pct_calc = (price_ref - yest_f) / yest_f * 100
            chg_calc = price_ref - yest_f
        else:
            pct_calc = pct_f
            chg_calc = chg_f
        
        # Gap direction
        direction = ''
        if yest_f > 0 and open_f > 0:
            gap = open_f - yest_f
            gap_pct = gap / yest_f * 100
            if abs(gap) < 0.005:
                direction = '平开'
            elif gap > 0:
                direction = f'高开+{gap:.2f}(+{gap_pct:.1f}%)'
            else:
                direction = f'低开{gap:.2f}({gap_pct:.1f}%)'
        
        # Volume/amount
        if vol_f >= 10000:
            vol_str = f'{vol_f/10000:.1f}万手'
        elif vol_f >= 100:
            vol_str = f'{vol_f/100:.0f}百手'
        else:
            vol_str = f'{vol_f:.0f}手'
        
        if amount_f >= 1e8:
            amt_str = f'{amount_f/1e8:.2f}亿'
        elif amount_f >= 1e4:
            amt_str = f'{amount_f/1e4:.0f}万'
        else:
            amt_str = f'{amount_f:.0f}'
        
        if curr_f == 0:
            lines_out.append(f'{name}: 竞价中={open_f:.2f}({direction}) 量:{vol_str} 额:{amt_str}')
        else:
            lines_out.append(f'{name}: {curr_f}({pct_calc:+.2f}%) 开:{open_f} {direction} 量:{vol_str} 额:{amt_str}')
    except Exception as e:
        lines_out.append(f'{name}|{code}|ERR:{e}|raw:{curr},{yest}')

import datetime
lines_out.append('')
lines_out.append(f'采集时间: {datetime.datetime.now().strftime("%H:%M:%S")}')

with open(outfile, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_out))
print("OK")
