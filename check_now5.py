# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

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

def get_price(code):
    try:
        if code.startswith('6'):
            tcode = 'sh' + code
        else:
            tcode = 'sz' + code
        url = 'http://qt.gtimg.cn/q=' + tcode
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://gu.qq.com',
        })
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('gbk', errors='replace')
            parts = content.split('~')
            if len(parts) > 10:
                price = float(parts[3]) if parts[3] else 0
                change_pct = float(parts[32]) if parts[32] else 0
                return price, change_pct
    except Exception as e:
        pass
    return None, None

for code, name, stoploss, cost, qty in stocks:
    price, change_pct = get_price(code)
    if price and price > 0:
        pnl = (price - cost) * qty
        flag = ''
        if stoploss > 0 and price < stoploss:
            flag = '[!!STOP!!]'
        elif stoploss > 0 and price < stoploss * 1.05:
            flag = '[!NEAR]'
        print("[OK] %s %s %.3f %+.2f%% PnL %+.0f %s" % (name, code, price, change_pct, pnl, flag))
    else:
        print("[X] %s %s FAIL" % (name, code))
