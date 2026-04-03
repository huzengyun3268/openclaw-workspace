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

codes_str = ','.join(stocks_info.keys())
url = 'https://qt.gtimg.cn/q=' + codes_str

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.qq.com'
})
r = urllib.request.urlopen(req, timeout=10)
raw = r.read().decode('gbk')

total_pnl = 0

for line in raw.strip().split('\n'):
    if not line.strip():
        continue
    parts = line.split('~')
    if len(parts) > 32:
        code_full = parts[0].replace('v_', '')
        price_str = parts[3]
        chg_pct = parts[32]
        
        for key in stocks_info:
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
                    flag = ''
                    if stop > 0 and price <= stop:
                        flag = ' [STOP!]'
                    sys.stdout.buffer.write(f'{stock_name}({code}): {price}  {chg_p:+.2f}%  PnL:{pnl:+.0f}{flag}\n'.encode('utf-8'))
                else:
                    sys.stdout.buffer.write(f'{stock_name}({code}): no data\n'.encode('utf-8'))
            except Exception as e:
                sys.stdout.buffer.write(f'{stock_name}({code}): error\n'.encode('utf-8'))

sys.stdout.buffer.write(f'Total PnL: {total_pnl:+.0f}\n'.encode('utf-8'))
