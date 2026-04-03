import urllib.request, sys, re

stocks = {
    'sh600352': '浙江龙盛',
    'sz300033': '同花顺',
    'sh600487': '亨通光电',
    'sh600893': '航发动力',
    'sh601168': '西部矿业',
    'sh518880': '黄金ETF',
    'sz430046': '圣博润',
    'sh600114': '东睦股份',
    'sh600089': '特变电工',
}

positions = {
    'sh600352': (76700, 16.948, 12.0),
    'sz300033': (1200, 423.488, 280),
    'sh600487': (3000, 43.210, 38.0),
    'sh600893': (9000, 49.184, 42.0),
    'sh601168': (11000, 26.169, 22.0),
    'sh518880': (24000, 9.868, None),
    'sz430046': (10334, 0.478, None),
    'sh600114': (11100, 31.176, 25.0),
    'sh600089': (52300, 24.765, 25.0),
}

codes = ','.join(stocks.keys())
url = f'http://qt.gtimg.cn/q={codes}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk', errors='replace')

results = []
lines = data.strip().split('\n')
print(f'DEBUG: got {len(lines)} lines')

for line in lines:
    if '~' not in line:
        continue
    m = re.search(r'v_(\w+)=', line)
    if not m:
        continue
    code = m.group(1)
    if code not in stocks:
        continue
    parts = line.split('~')
    if len(parts) < 36:
        print(f'DEBUG short: {code} parts={len(parts)}')
        continue
    name = stocks[code]
    try:
        price = float(parts[3]) if parts[3] else 0
        prev = float(parts[4]) if parts[4] else 0
    except:
        print(f'DEBUG parse error: {code}')
        continue
    chg = price - prev
    chg_pct = (chg / prev * 100) if prev else 0
    direction = '+' if chg > 0 else '-' if chg < 0 else ' '
    pnl = 0
    stop_flag = ''
    if code in positions:
        shares, cost, stop = positions[code]
        pnl = (price - cost) * shares
        stop_flag = ' **止损**' if stop and price <= stop else ''
    results.append((code, name, price, direction, chg_pct, pnl, stop_flag))

print('')
print('='*60)
print('  持仓监控 2026-04-03 收盘')
print('='*60)

main_total = 0
for code, name, price, d, pct, pnl, stop in results:
    tag = ''
    if code in ('sh600352','sz300033','sh600487','sh600893','sh601168','sh518880','sz430046'):
        tag = '[主]'
        main_total += pnl
    elif code == 'sh600114':
        tag = '[老婆]'
    elif code == 'sh600089':
        tag = '[两融]'
    print(f'{tag}{name}({code}): {price:.3f} {d}{abs(pct):.2f}%  浮亏{abs(pnl)/1e4:.1f}万{stop}')

print('')
print(f'主账户持仓浮动盈亏: {main_total/1e4:.2f}万')
print('')
print('止损检查:')
for code, name, price, d, pct, pnl, stop in results:
    if code in positions:
        shares, cost, stop_price = positions[code]
        if stop_price:
            if price <= stop_price:
                print(f'  !! {name} 现价{price:.3f} <= 止损{stop_price} 触发止损线 !!')
            else:
                print(f'  OK {name} {price:.3f} > 止损{stop_price}')
