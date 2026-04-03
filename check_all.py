# -*- coding: utf-8 -*-
import urllib.request
import sys

stocks_info = {
    'sh600352': ('浙江龙盛', 16.948, 12.0, 76700, '主账户'),
    'sz300033': ('同花顺', 423.488, 280.0, 1200, '主账户'),
    'sh600487': ('亨通光电', 43.210, 38.0, 3000, '主账户'),
    'sh600893': ('航发动力', 49.184, 42.0, 9000, '主账户'),
    'sh601168': ('西部矿业', 26.169, 22.0, 11000, '主账户'),
    'sh518880': ('黄金ETF', 9.868, 0.0, 24000, '主账户'),
    'sz430046': ('圣博润', 0.478, 0.0, 10334, '主账户'),
    'sh600114': ('东睦股份', 31.176, 25.0, 11100, '老婆账户'),
    'sh600089': ('特变电工', 24.765, 25.0, 52300, '两融账户'),
}

# fetch main stocks
codes_str = ','.join(['sh600352','sz300033','sh600487','sh600893','sh601168','sh518880','sh600114','sh600089'])
url = 'https://qt.gtimg.cn/q=' + codes_str
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'})
r = urllib.request.urlopen(req, timeout=10)
raw = r.read().decode('gbk')

total_pnl = 0
main_pnl = 0
wife_pnl = 0
margin_pnl = 0
stop_stocks = []

for line in raw.strip().split('\n'):
    if not line.strip():
        continue
    parts = line.split('~')
    if len(parts) > 32:
        code_full = parts[0].replace('v_', '')
        price_str = parts[3]
        chg_pct = parts[32]
        
        for key in stocks_info:
            if key == 'sz430046':
                continue
            code_num = key.replace('sh', '').replace('sz', '')
            if code_num in code_full:
                code = key
                break
        else:
            continue
        
        if code in stocks_info:
            info = stocks_info[code]
            stock_name, cost, stop, qty, account = info
            try:
                price = float(price_str) if price_str else 0
                chg_p = float(chg_pct) if chg_pct else 0
                
                if price > 0:
                    pnl = (price - cost) * qty
                    total_pnl += pnl
                    if account == '主账户':
                        main_pnl += pnl
                    elif account == '老婆账户':
                        wife_pnl += pnl
                    elif account == '两融账户':
                        margin_pnl += pnl
                    flag = ''
                    if stop > 0 and price <= stop:
                        flag = ' [STOP!]'
                        stop_stocks.append(stock_name)
                    msg = f'{stock_name}: {price} {chg_p:+.2f}% | PnL: {pnl:+.0f} | 成本:{cost} 止损:{stop if stop>0 else "-"}{flag}'
                    sys.stdout.buffer.write((msg + '\n').encode('utf-8'))
                else:
                    sys.stdout.buffer.write((f'{stock_name}: no data\n').encode('utf-8'))
            except:
                pass

# 圣博润 - use different API
try:
    url2 = 'https://qt.gtimg.cn/q=sz430046'
    req2 = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'})
    r2 = urllib.request.urlopen(req2, timeout=10)
    raw2 = r2.read().decode('gbk')
    if 'none_match' not in raw2:
        parts2 = raw2.split('~')
        if len(parts2) > 3 and parts2[3]:
            price = float(parts2[3])
            info = stocks_info['sz430046']
            pnl = (price - info[1]) * info[3]
            total_pnl += pnl
            main_pnl += pnl
            sys.stdout.buffer.write((f'{info[0]}: {price} | PnL: {pnl:+.0f} | 成本:{info[1]} (新三板/数据有限)\n').encode('utf-8'))
    else:
        sys.stdout.buffer.write(('圣博润(430046): 新三板，数据不可用，当前参考成本价 0.478\n').encode('utf-8'))
        pnl = 0
        info = stocks_info['sz430046']
        total_pnl += 0
        main_pnl += 0
except Exception as e:
    sys.stdout.buffer.write((f'圣博润: 查询失败\n').encode('utf-8'))

sys.stdout.buffer.write(('\n--- 汇总 ---\n').encode('utf-8'))
sys.stdout.buffer.write((f'主账户盈亏: {main_pnl:+.0f}\n').encode('utf-8'))
sys.stdout.buffer.write((f'老婆账户盈亏: {wife_pnl:+.0f}\n').encode('utf-8'))
sys.stdout.buffer.write((f'两融账户盈亏: {margin_pnl:+.0f}\n').encode('utf-8'))
sys.stdout.buffer.write((f'估算总盈亏: {total_pnl:+.0f}\n').encode('utf-8'))
if stop_stocks:
    sys.stdout.buffer.write((f'触及止损: {", ".join(stop_stocks)}\n').encode('utf-8'))
