# -*- coding: utf-8 -*-
import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# (code, market_prefix)  0=深圳, 1=上海
stocks = [
    ('600352', '1', 15.952, 12.0, '主账户'),
    ('300033', '0', 423.488, 280.0, '主账户'),
    ('831330', '0', 20.361, None, '主账户'),
    ('000988', '0', 116.87, None, '主账户'),
    ('688295', '1', 37.843, None, '主账户'),
    ('600487', '1', 42.391, None, '主账户'),
    ('300499', '0', 41.625, 38.0, '主账户'),
    ('601168', '1', 24.863, None, '主账户'),
    ('600893', '1', 47.196, None, '主账户'),
    ('920046', '0', 329.555, 27.0, '主账户'),
    ('430046', '0', 0.478, None, '主账户'),
    ('600114', '1', 25.9, 25.0, '老婆'),
    ('301638', '0', 32.635, 28.0, '老婆'),
    ('600089', '1', 24.765, 25.0, '两融'),
]

names = {
    '600352': '浙江龙盛', '300033': '同花顺', '831330': '普适导航',
    '000988': '华工科技', '688295': '中复神鹰', '600487': '亨通光电',
    '300499': '高澜股份', '601168': '西部矿业', '600893': '航发动力',
    '920046': '亿能电力', '430046': '圣博润', '600114': '东睦股份',
    '301638': '南网数字', '600089': '特变电工'
}

# User's last known prices (from 2026-03-24 screenshots)
last_prices = {
    '600352': 12.52, '300033': 303.29, '831330': 20.08,
    '000988': 108.48, '688295': 60.29, '600487': 42.67,
    '300499': 37.28, '601168': 25.03, '600893': 47.24,
    '920046': 30.78, '430046': 0.28, '600114': 25.84,
    '301638': 29.41, '600089': 28.09
}

print('=== 持仓监控 14:30 ===')
print()

alerts = []

for code, mkt, cost, sl, account in stocks:
    price = None
    pct = None
    try:
        url = f'http://push2.eastmoney.com/api/qt/stock/get?fltt=2&invt=2&fields=f43,f169,f170&secid={mkt}.{code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get('data') and d['data'].get('f43'):
            raw = d['data']['f43']
            price = round(raw / 100, 3) if raw > 1000 else raw  # 100-based or direct
            pct_raw = d['data'].get('f170', 0)
            pct = round(pct_raw / 100, 2) if pct_raw and abs(pct_raw) > 100 else pct_raw
    except:
        pass

    # Use last known price if no current data
    if price is None or price == 0:
        price = last_prices.get(code, 0)
        live = '(昨日)'
    else:
        live = ''

    pnl_pct = (price - cost) / cost * 100 if cost > 0 else 0

    flag = ''
    if sl and price <= sl:
        flag = ' ⚠️触及止损!'
        alerts.append(f'{names[code]}({code}) 现价{price} <= 止损{sl}')
    elif sl and price <= sl * 1.05:
        flag = ' ⚠️接近止损!'
        alerts.append(f'{names[code]}({code}) 现价{price} 距止损{sl}不足5%')

    print(f'{names[code]}({code}) 现价:{price}{live} 涨跌:{pct:+.2f}% 盈亏:{pnl_pct:+.1f}%{flag}')

print()
if alerts:
    print('=== 告警 ===')
    for a in alerts:
        print(f'  {a}')
else:
    print('暂无止损告警')
