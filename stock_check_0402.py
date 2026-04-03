import requests, re, json

positions = {
    'main': [
        ('浙江龙盛', 'sh600352', 76700, 16.948, 12.0),
        ('同花顺', 'sz300033', 1200, 423.488, 280),
        ('亨通光电', 'sh600487', 3000, 43.210, 38.0),
        ('航发动力', 'sh600893', 9000, 49.184, 42.0),
        ('西部矿业', 'sh601168', 11000, 26.169, 22.0),
        ('黄金ETF', 'sh518880', 24000, 9.868, None),
        ('圣博润', 'sz430046', 10334, 0.478, None),
    ],
    'wife': [
        ('东睦股份', 'sh600114', 11100, 31.176, 25.0),
    ],
    'margin': [
        ('特变电工', 'sh600089', 52300, 24.765, 25.0),
    ]
}

codes = [p[1] for ps in positions.values() for p in ps]
url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
r = requests.get(url, timeout=5)
prices = {}
for line in r.text.strip().split('\n'):
    parts = line.split('~')
    if len(parts) > 3:
        raw_key = parts[0]
        m = re.match(r'v_(sh\d+|sz\d+|bj\d+)', raw_key)
        if m:
            key = m.group(1)
            prices[key] = float(parts[3])

all_pl = 0
print('=== main ===')
for name, code, vol, cost, stop in positions['main']:
    price = prices.get(code, 0)
    pl = (price - cost) * vol if price else 0
    pl_pct = (price - cost) / cost * 100 if cost and price else 0
    all_pl += pl
    if stop and price > 0 and price < stop:
        flag = ' <<< STOP-LOSS >>>'
    elif stop:
        flag = ' [stop OK]'
    else:
        flag = ''
    print('%s %.3f cost=%.3f pl=%+.0f(%.1f%%)%s' % (name, price, cost, pl, pl_pct, flag))

wife_pl = 0
print('\n=== wife ===')
for name, code, vol, cost, stop in positions['wife']:
    price = prices.get(code, 0)
    pl = (price - cost) * vol if price else 0
    pl_pct = (price - cost) / cost * 100 if cost and price else 0
    wife_pl += pl
    if stop and price > 0 and price < stop:
        flag = ' <<< STOP-LOSS >>>'
    elif stop:
        flag = ' [stop OK]'
    else:
        flag = ''
    print('%s %.3f cost=%.3f pl=%+.0f(%.1f%%)%s' % (name, price, cost, pl, pl_pct, flag))

margin_pl = 0
print('\n=== margin ===')
for name, code, vol, cost, stop in positions['margin']:
    price = prices.get(code, 0)
    pl = (price - cost) * vol if price else 0
    pl_pct = (price - cost) / cost * 100 if cost and price else 0
    margin_pl += pl
    if stop and price > 0 and price < stop:
        flag = ' <<< STOP-LOSS >>>'
    elif stop:
        flag = ' [stop OK]'
    else:
        flag = ''
    print('%s %.3f cost=%.3f pl=%+.0f(%.1f%%)%s' % (name, price, cost, pl, pl_pct, flag))

total = all_pl + wife_pl + margin_pl
print('\nMain: %+.0f | Wife: %+.0f | Margin: %+.0f | Total: %+.0f' % (all_pl, wife_pl, margin_pl, total))
