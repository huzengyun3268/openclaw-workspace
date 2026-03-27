# -*- coding: utf-8 -*-
import ssl
import urllib.request
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

stocks = [
    ('600352', '浙江龙盛', 12.0, 16.52),
    ('600893', '航发动力', 42.0, 49.184),
    ('300033', '同花顺', 280.0, 423.488),
    ('601168', '西部矿业', 22.0, 26.169),
    ('600487', '亨通光电', 38.0, 43.998),
    ('688295', '中复神鹰', 0, 37.843),
    ('920046', '亿能电力', 27.0, 329.553),
    ('430046', '圣博润', 0, 0.478),
    ('600114', '东睦股份', 25.0, 26.0),
    ('301638', '南网数字', 28.0, 32.64),
    ('600089', '特变电工', 25.0, 24.765),
]

def get_price(code):
    try:
        if code.startswith('920') or code.startswith('430'):
            secid = '0.' + code
        elif code.startswith('6'):
            secid = '1.' + code
        else:
            secid = '0.' + code

        # Try eastmoney https
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f169,f170,f57,f58'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://quote.eastmoney.com/',
            'Accept': '*/*',
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            if data.get('data'):
                d = data['data']
                price = float(d.get('f43', 0)) / 100 if d.get('f43') else 0
                change_pct = float(d.get('f170', 0)) / 100 if d.get('f170') else 0
                name = d.get('f58', '')
                return price, change_pct, name
    except Exception as e:
        pass

    # Fallback: try Tencent Finance API
    try:
        if code.startswith('6'):
            tcode = 'sh' + code
        else:
            tcode = 'sz' + code
        url = f'https://qt.gtimg.cn/q={tcode}'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://gu.qq.com',
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            content = r.read().decode('gbk', errors='replace')
            parts = content.split('~')
            if len(parts) > 10:
                price = float(parts[3]) if parts[3] else 0
                change_pct = float(parts[32]) if parts[32] else 0
                name = parts[1]
                return price, change_pct, name
    except Exception as e:
        pass

    return None, None, None

print('=' * 55)
print('持仓监控 2026-03-27 收盘前')
print('=' * 55)

results = []
for code, name, stoploss, cost in stocks:
    price, change_pct, fetched_name = get_price(code)
    if price and price > 0:
        pnl = (price - cost) * 10000
        flag = ''
        if stoploss > 0 and price < stoploss:
            flag = ' ⚠️跌破止损!'
        elif stoploss > 0 and price < stoploss * 1.05:
            flag = ' 🔶接近止损'
        status = 'OK'
        if flag:
            status = '⚠️'
        print(f"[{status}] {name}({code}): {price:.3f} {change_pct:+.2f}% | 盈亏{pnl:+,.0f}元{flag}")
        results.append((name, code, price, change_pct, pnl, flag))
    else:
        print(f"[X] {name}({code}): 获取失败")

print()
