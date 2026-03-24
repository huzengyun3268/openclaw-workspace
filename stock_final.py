# -*- coding: utf-8 -*-
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com'}

stocks_data = {
    '600352': ('浙江龙盛', 15.91, 106700),
    '600089': ('特变电工', 24.765, 52300),
    '301667': ('纳百川', 82.715, 3000),
    '920046': ('亿能电力', 35.936, 12731),
    '300033': ('同花顺', 511.22, 600),
    '831330': ('普适导航', 20.415, 6370),
    '300189': ('神农种业', 17.099, 5000),
    '430046': ('圣博润', 0.478, 10334),
    '600114': ('东睦股份', 32.428, 9200),
    '301638': ('南网数字', 32.635, 1700),
}

# Tencent codes for SH/SZ stocks
tc_codes = {
    '600352': 'sh600352', '600089': 'sh600089', '301667': 'sz301667',
    '920046': 'bj920046', '300033': 'sz300033', '300189': 'sz300189',
    '600114': 'sh600114', '301638': 'sz301638',
}

tc_list = list(tc_codes.values())
codes_str = ','.join(tc_list)
url = f'https://qt.gtimg.cn/q={codes_str}'
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com'}, timeout=10)
resp.encoding = 'gbk'

results = {}
# Parse Tencent data
for line in resp.text.split(';'):
    for tc in tc_list:
        if f'v_{tc}' in line:
            parts = line.split('~')
            if len(parts) > 32:
                code = parts[2]
                price = float(parts[3])
                prev = float(parts[4])
                results[code] = {'price': price, 'prev': prev}
            break

# Get BJ stocks from eastmoney
bj_codes = {'831330': '0.831330', '430046': '0.430046'}
for code, secid in bj_codes.items():
    url = f'https://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f43,f57,f58,f107,f50&secid={secid}'
    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = json.loads(r.text)
        if data.get('data'):
            price = float(data['data']['f43'])
            change_pct = float(data['data']['f50'])
            prev = price / (1 + change_pct / 100) if change_pct != 0 else price
            results[code] = {'price': price, 'prev': round(prev, 3)}
    except Exception as e:
        print(f'Error for {code}: {e}')

# Print results
total_pl = 0
total_val = 0
my_stocks = ['600352','600089','301667','920046','300033','831330','300189','430046']
wife_stocks = ['600114','301638']

print('\n=== MY ACCOUNT ===')
for code in my_stocks:
    name, cost, qty = stocks_data[code]
    if code in results:
        price = results[code]['price']
        prev = results[code]['prev']
        change_pct = (price - prev) / prev * 100
        market_val = price * qty
        cost_val = cost * qty
        pl = market_val - cost_val
        pl_pct = (price - cost) / cost * 100
        total_pl += pl
        total_val += market_val
        arrow = '+' if change_pct >= 0 else ''
        print(f'{code} {name}: {price:.3f} ({arrow}{change_pct:.2f}%) Cost={cost:.3f} Qty={qty} MktVal={market_val:.0f} PL={pl:+.2f}({pl_pct:+.1f}%)')
    else:
        print(f'{code} {name}: NO DATA (cost={cost})')
        total_pl += (0 - cost * qty)  # assume 0 if no data
        total_val += 0

print(f'\nMY Total MktVal: {total_val:.2f}')
print(f'MY Total PL: {total_pl:.2f}')

wife_pl = 0
wife_val = 0
print('\n=== WIFE ACCOUNT ===')
for code in wife_stocks:
    name, cost, qty = stocks_data[code]
    if code in results:
        price = results[code]['price']
        prev = results[code]['prev']
        change_pct = (price - prev) / prev * 100
        market_val = price * qty
        cost_val = cost * qty
        pl = market_val - cost_val
        pl_pct = (price - cost) / cost * 100
        wife_pl += pl
        wife_val += market_val
        arrow = '+' if change_pct >= 0 else ''
        print(f'{code} {name}: {price:.3f} ({arrow}{change_pct:.2f}%) Cost={cost:.3f} Qty={qty} MktVal={market_val:.0f} PL={pl:+.2f}({pl_pct:+.1f}%)')

print(f'\nWIFE Total MktVal: {wife_val:.2f}')
print(f'WIFE Total PL: {wife_pl:.2f}')
print(f'\nCOMBINED PL: {total_pl + wife_pl:+.2f}')
