# -*- coding: utf-8 -*-
import requests
from datetime import datetime

stocks = {
    '600352': ('浙江龙盛', 106700, 15.91),
    '600089': ('特变电工', 52300, 24.765),
    '301667': ('纳百川', 3000, 82.715),
    '920046': ('亿能电力', 12731, 35.936),
    '300033': ('同花顺', 600, 511.22),
    '831330': ('普适导航', 6370, 20.415),
    '300189': ('神农种业', 5000, 17.099),
    '430046': ('圣博润', 10334, 0.478),
    '600114': ('东睦股份_老婆', 9200, 32.428),
    '301638': ('南网数字_老婆', 1700, 32.635),
}

# Build code mapping
code_list = []
for code in stocks:
    if code.startswith('6'):
        code_list.append('sh' + code)
    elif code.startswith('92') or code.startswith('83') or code.startswith('43'):
        code_list.append('bj' + code)
    else:
        code_list.append('sz' + code)

codes_str = ','.join(code_list)
url = 'https://qt.gtimg.cn/q=' + codes_str

try:
    resp = requests.get(url, timeout=15)
    resp.encoding = 'gbk'
    raw_lines = resp.text.strip().split('\n')
except Exception as e:
    print('API请求失败: ' + str(e))
    exit(1)

price_map = {}
for line in raw_lines:
    if not line.startswith('v_'):
        continue
    try:
        # Format: v_sh600352="1~name~code~price~...
        # First split by =" to get code part
        header_and_data = line.split('="', 1)
        if len(header_and_data) < 2:
            continue
        code_part = header_and_data[0]  # v_sh600352
        data_part = header_and_data[1]  # 1~name~code~price~...
        raw_code = code_part.split('_')[1] if '_' in code_part else ''
        code = raw_code.replace('sh', '').replace('sz', '').replace('bj', '')
        parts = data_part.split('~')
        if len(parts) < 35:
            continue
        price_str = parts[3]
        change_pct_str = parts[32]
        price = float(price_str) if price_str else 0
        change_pct = float(change_pct_str) if change_pct_str else 0
        price_map[code] = {'price': price, 'change_pct': change_pct}
    except:
        continue

total_profit = 0.0
total_cost = 0.0
total_value = 0.0
result_lines = []
result_lines.append('时间: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
result_lines.append('='*80)

for code, info in stocks.items():
    name = info[0]
    qty = info[1]
    cost = info[2]
    if code in price_map and price_map[code]['price'] > 0:
        p = price_map[code]['price']
        chg = price_map[code]['change_pct']
        profit = (p - cost) * qty
        profit_pct = (p / cost - 1) * 100
        total_profit += profit
        total_cost += cost * qty
        total_value += p * qty
        sign = '+' if profit >= 0 else ''
        result_lines.append('%s(%s): 现价=%.3f 涨跌=%+.2f%% 持仓=%d股 成本=%.3f 盈亏=%s%.0f(%s%.1f%%)' % (name, code, p, chg, qty, cost, sign, profit, sign, profit_pct))
    else:
        result_lines.append(name + '(' + code + '): 行情获取失败')

result_lines.append('='*80)
if total_cost > 0:
    sign = '+' if total_profit >= 0 else ''
    result_lines.append('总盈亏: %s%.0f元  总成本: %.0f元  总市值: %.0f元  收益率: %s%.2f%%' % (sign, total_profit, total_cost, total_value, sign, total_profit/total_cost*100))

content = '\n'.join(result_lines)
with open(r'C:\Users\Administrator\.openclaw\workspace\stock_result.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print(content)
