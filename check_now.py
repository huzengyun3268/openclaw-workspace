# -*- coding: utf-8 -*-
import urllib.request
import json
import sys

# 主账户持仓
stocks = [
    ('600352', '浙江龙盛', 12.0, 16.52),
    ('600893', '航发动力', 42.0, 49.184),
    ('300033', '同花顺', 280.0, 423.488),
    ('601168', '西部矿业', 22.0, 26.169),
    ('831330', '普适导航', 18.0, 20.361),
    ('600487', '亨通光电', 38.0, 43.998),
    ('688295', '中复神鹰', 0, 37.843),
    ('920046', '亿能电力', 27.0, 329.553),
    ('430046', '圣博润', 0, 0.478),
]

# 老婆账户
laopo = [
    ('600114', '东睦股份', 25.0, 26.0),
    ('301638', '南网数字', 28.0, 32.64),
]

# 两融账户
rzrq = [
    ('600089', '特变电工', 25.0, 24.765),
]

def get_price(code):
    """获取实时价格"""
    try:
        if code.startswith('920') or code.startswith('430'):
            # 北交所/新三板
            secid = '0.' + code
        elif code.startswith('6'):
            secid = '1.' + code
        else:
            secid = '0.' + code

        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f169,f170,f57,f58'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'http://quote.eastmoney.com'
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            if data.get('data'):
                d = data['data']
                price = float(d.get('f43', 0)) / 100 if d.get('f43') else 0
                change_pct = float(d.get('f170', 0)) / 100 if d.get('f170') else 0
                name = d.get('f58', '')
                return price, change_pct, name
    except Exception as e:
        return None, None, None
    return 0, 0, ''

print('=' * 60)
print('持仓监控 2026-03-27 收盘前检查')
print('=' * 60)

print('\n【主账户】')
for code, name, stoploss, cost in stocks:
    price, change_pct, _ = get_price(code)
    if price:
        pnl = (price - cost) * 10000
        flag = ''
        if stoploss > 0 and price < stoploss:
            flag = ' ⚠️跌破止损!'
        elif stoploss > 0 and price < stoploss * 1.05:
            flag = ' 🔶接近止损'
        print(f"  {name}({code}): 现价{price:.3f} 涨跌{change_pct:+.2f}% | 成本{cost:.3f} | 盈亏{pnl:+,.0f}元 {flag}")
    else:
        print(f"  {name}({code}): 获取失败")

print('\n【老婆账户】')
for code, name, stoploss, cost in laopo:
    price, change_pct, _ = get_price(code)
    if price:
        pnl = (price - cost) * 10000
        flag = ''
        if stoploss > 0 and price < stoploss:
            flag = ' ⚠️跌破止损!'
        elif stoploss > 0 and price < stoploss * 1.05:
            flag = ' 🔶接近止损'
        print(f"  {name}({code}): 现价{price:.3f} 涨跌{change_pct:+.2f}% | 成本{cost:.3f} | 盈亏{pnl:+,.0f}元 {flag}")
    else:
        print(f"  {name}({code}): 获取失败")

print('\n【两融账户】')
for code, name, stoploss, cost in rzrq:
    price, change_pct, _ = get_price(code)
    if price:
        pnl = (price - cost) * 10000
        flag = ''
        if stoploss > 0 and price < stoploss:
            flag = ' ⚠️跌破止损!'
        elif stoploss > 0 and price < stoploss * 1.05:
            flag = ' 🔶接近止损'
        print(f"  {name}({code}): 现价{price:.3f} 涨跌{change_pct:+.2f}% | 成本{cost:.3f} | 盈亏{pnl:+,.0f}元 {flag}")
    else:
        print(f"  {name}({code}): 获取失败")

print()
