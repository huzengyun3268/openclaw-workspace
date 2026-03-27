# -*- coding: utf-8 -*-
import ssl
import urllib.request
import json
import sys

# 设置stdout编码
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

stocks = [
    ('600352', '浙江龙盛', 12.0, 16.52, 86700),
    ('600893', '航发动力', 42.0, 49.184, 9000),
    ('300033', '同花顺', 280.0, 423.488, 1200),
    ('601168', '西部矿业', 22.0, 26.169, 11000),
    ('600487', '亨通光电', 38.0, 43.998, 3000),
    ('688295', '中复神鹰', 0, 37.843, 1500),
    ('920046', '亿能电力', 27.0, 329.553, 200),
    ('430046', '圣博润', 0, 0.478, 10334),
    ('600114', '东睦股份', 25.0, 26.0, 4900),
    ('301638', '南网数字', 28.0, 32.64, 1700),
    ('600089', '特变电工', 25.0, 24.765, 52300),
]

def get_price_em(code):
    try:
        if code.startswith('920') or code.startswith('430'):
            secid = '0.' + code
        elif code.startswith('6'):
            secid = '1.' + code
        else:
            secid = '0.' + code
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f169,f170,f57,f58'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://quote.eastmoney.com/',
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            if data.get('data'):
                d = data['data']
                price = float(d.get('f43', 0)) / 100 if d.get('f43') else 0
                change_pct = float(d.get('f170', 0)) / 100 if d.get('f170') else 0
                name = d.get('f58', '')
                return price, change_pct
    except Exception as e:
        pass
    return None, None

results = []
for code, name, stoploss, cost, qty in stocks:
    price, change_pct = get_price_em(code)
    if price and price > 0:
        pnl = (price - cost) * qty
        flag = ''
        if stoploss > 0 and price < stoploss:
            flag = '[!!跌破止损!!]'
        elif stoploss > 0 and price < stoploss * 1.05:
            flag = '[!接近止损]'
        results.append(f"[{name}] 现价{price:.3f} 涨跌{change_pct:+.2f}% | 成本{cost:.3f} | 盈亏{pnl:+,.0f}元 {flag}")
    else:
        results.append(f"[X] {name}({code}): 获取失败")

for r in results:
    print(r)
