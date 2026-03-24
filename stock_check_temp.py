import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

stocks = {
    '600352': '浙江龙盛',
    '600089': '特变电工',
    '301667': '纳百川',
    '920046': '亿能电力',
    '300033': '同花顺',
    '831330': '普适导航',
    '300189': '神农种业',
    '430046': '圣博润',
    '600114': '东睦股份(老婆)',
    '301638': '南网数字(老婆)',
}

results = []
for code, name in stocks.items():
    try:
        secid = '1' if code.startswith('6') else '0'
        url = f'http://push2his.eastmoney.com/api/qt/stock/get?secid={secid}.{code}&fields=f43,f169,f170,f171,f57,f58&ut=fa5fd1943c7b386f172d6893dbfba10b'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
            data = json.loads(r.read())
            f = data.get('data', {})
            price = f.get('f43', 0) / 100 if f.get('f43') else 0
            change_pct = f.get('f170', 0) / 100 if f.get('f170') else 0
            results.append((code, name, price, change_pct, None))
    except Exception as e:
        results.append((code, name, None, None, str(e)))

for code, name, price, chg, err in results:
    if price is not None and price > 0:
        chg_str = f'{chg:+.2f}%'
        print(f'{name}({code}): {price:.3f} {chg_str}')
    else:
        print(f'{name}({code}): 获取失败 {err}')

# 计算持仓盈亏
positions = {
    '600352': (106700, 15.91),
    '600089': (52300, 24.765),
    '301667': (3000, 82.715),
    '920046': (12731, 35.936),
    '300033': (600, 511.22),
    '831330': (6370, 20.415),
    '300189': (5000, 17.099),
    '430046': (10334, 0.478),
}

wife_positions = {
    '600114': (9200, 32.428),
    '301638': (1700, 32.635),
}

current_prices = {code: price for code, name, price, chg, err in results if price}

print('\n--- 自己账户持仓盈亏 ---')
total_cost = 0
total_value = 0
for code, (shares, cost) in positions.items():
    if code in current_prices:
        price = current_prices[code]
        cost_total = shares * cost
        value = shares * price
        profit = value - cost_total
        pct = profit / cost_total * 100
        total_cost += cost_total
        total_value += value
        print(f'{stocks[code]}: 浮盈{profit:+.0f}元 ({pct:+.1f}%) 现价{price:.3f}')

if total_cost > 0:
    total_profit = total_value - total_cost
    total_pct = total_profit / total_cost * 100
    print(f'账户合计: 浮盈{total_profit:+.0f}元 ({total_pct:+.1f}%) 总值{total_value:.0f}元')

print('\n--- 老婆账户持仓盈亏 ---')
for code, (shares, cost) in wife_positions.items():
    if code in current_prices:
        price = current_prices[code]
        cost_total = shares * cost
        value = shares * price
        profit = value - cost_total
        pct = profit / cost_total * 100
        print(f'{stocks[code]}: 浮盈{profit:+.0f}元 ({pct:+.1f}%) 现价{price:.3f}')
