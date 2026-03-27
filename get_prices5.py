import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

stocks = {
    '600352': ('sh', '浙江龙盛', 16.52, 12.0),
    '600893': ('sh', '航发动力', 49.184, 42.0),
    '300033': ('sz', '同花顺', 423.488, 280),
    '601168': ('sh', '西部矿业', 26.169, 22.0),
    '831330': ('bj', '普适导航', 20.361, 18.0),
    '600487': ('sh', '亨通光电', 43.998, 38.0),
    '688295': ('sh', '中复神鹰', 37.843, None),
    '920046': ('bj', '亿能电力', 329.553, None),
    '430046': ('bj', '圣博润', 0.478, None),
    '600089': ('sh', '特变电工(两融)', 24.765, 25.0),
    '600114': ('sh', '东睦股份(老婆)', 26.0, 25.0),
    '301638': ('sz', '南网数字(老婆)', 32.64, 28.0),
}

codes_str = ','.join([f"{v[0]}{k}" for k, v in stocks.items()])
url = f'https://hq.sinajs.cn/list={codes_str}'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.sina.com.cn'
})
r = urllib.request.urlopen(req, timeout=10)
data = r.read().decode('gbk')

lines = data.strip().split('\n')
results = {}
for line in lines:
    try:
        if '"' not in line:
            continue
        parts = line.split('"')[1].split(',')
        if len(parts) < 10:
            continue
        code_full = line.split('_')[1].split('"')[0]
        market = code_full[:2]
        code = code_full[2:]
        if code not in stocks:
            continue
        name = stocks[code][1]
        now = float(parts[3])
        high = float(parts[4])
        low = float(parts[5])
        yclose = float(parts[2])
        cost = stocks[code][2]
        stop = stocks[code][3]
        chg_pct = (now - yclose) / yclose * 100
        pl = (now - cost) / cost * 100
        pl_amt = (now - cost) * 10000
        results[code] = {
            'name': name,
            'now': now,
            'high': high,
            'low': low,
            'cost': cost,
            'stop': stop,
            'chg_pct': chg_pct,
            'pl': pl,
            'pl_amt': pl_amt,
        }
    except Exception as e:
        print(f"Parse error: {e}", file=sys.stderr)

print("=== 主账户持仓 ===")
total_pl = 0
for code in ['600352', '600893', '300033', '601168', '831330', '600487', '688295', '920046', '430046']:
    r = results.get(code)
    if not r:
        continue
    stop_pct = (r['stop'] / r['cost'] - 1) * 100 if r['stop'] else None
    print(f"{r['name']}({code}): 现价={r['now']} 成本={r['cost']} 今日涨跌={r['chg_pct']:+.2f}%")
    print(f"  持仓盈亏={r['pl']:+.1f}%({r['pl_amt']:+.0f}万)")
    if r['stop']:
        print(f"  止损={r['stop']}({stop_pct:.1f}%)")
        if r['now'] <= r['stop']:
            print(f"  ⚠️⚠️⚠️ 已触及止损！")
        elif r['now'] < r['stop'] * 1.05:
            print(f"  ⚠️ 接近止损！")
    print()
    total_pl += r['pl_amt']

print(f"主账户合计盈亏: {total_pl:+.0f}万")

print()
print("=== 两融账户 ===")
r = results.get('600089')
if r:
    print(f"{r['name']}: 现价={r['now']} 成本={r['cost']} 今日涨跌={r['chg_pct']:+.2f}%")
    print(f"  持仓盈亏={r['pl']:+.1f}%({r['pl_amt']:+.0f}万)")
    print(f"  止损={r['stop']}")
    if r['now'] <= r['stop']:
        print(f"  ⚠️⚠️⚠️ 已触及止损！")
    elif r['now'] < r['stop'] * 1.05:
        print(f"  ⚠️ 接近止损！")

print()
print("=== 老婆账户 ===")
for code in ['600114', '301638']:
    r = results.get(code)
    if not r:
        continue
    print(f"{r['name']}: 现价={r['now']} 成本={r['cost']} 今日涨跌={r['chg_pct']:+.2f}%")
    print(f"  持仓盈亏={r['pl']:+.1f}%({r['pl_amt']:+.0f}万)")
    if r['stop']:
        stop_pct = (r['stop'] / r['cost'] - 1) * 100
        print(f"  止损={r['stop']}({stop_pct:.1f}%)")
        if r['now'] <= r['stop']:
            print(f"  ⚠️⚠️⚠️ 已触及止损！")
