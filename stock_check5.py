# -*- coding: utf-8 -*-
import requests
import datetime

positions = [
    ('sh600352', 76700, 16.948, 12.0),
    ('sz300033', 1200, 423.488, 280),
    ('sh600487', 3000, 43.210, 38.0),
    ('sh600893', 9000, 49.184, 42.0),
    ('sh601168', 11000, 26.169, 22.0),
    ('sh518880', 24000, 9.868, 0),
    ('sz430046', 10334, 0.478, 0),
    ('sh600114', 11100, 31.176, 25.0),
    ('sh600089', 52300, 24.765, 25.0),
]
names = {
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

def to_em_code(code):
    prefix, num = code[:2], code[2:]
    return ('1.' if prefix == 'sh' else '0.') + num

now = datetime.datetime.now()
print(now.strftime('%Y-%m-%d %H:%M') + ' 持仓监控')
print('=' * 55)

codes_str = ','.join([to_em_code(p[0]) for p in positions])
url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f12,f14,f3,f2&secids={codes_str}'
resp = requests.get(url, timeout=10)
diff = resp.json().get('data', {}).get('diff', [])
pmap = {item['f12']: item for item in diff}

total_pnl = 0.0
lines = []
alerts = []

for code, vol, cost, stop in positions:
    code_num = code[2:]
    item = pmap.get(code_num, {})
    name = names.get(code, code)
    if item:
        price = item.get('f2', 0)
        pct_day = item.get('f3', 0)
        if price > 0:
            pnl = (price - cost) * vol
            pct_cost = (price - cost) / cost * 100
            total_pnl += pnl
            arrow = '+' if pct_cost >= 0 else '-'
            
            tags = []
            if stop > 0 and price <= stop:
                tags.append('*STOP*')
            elif pct_cost < -20:
                tags.append('** DEEP LOSS **')
            elif pct_cost > 15:
                tags.append('** BIG GAIN **')
            elif pct_day <= -3:
                tags.append(f'drop {pct_day}%')
            
            tags_str = ' | ' + ', '.join(tags) if tags else ''
            line = f'{name}: price={price}, cost={cost}, pnl={arrow}{abs(pct_cost):.1f}%, pnl_amt={pnl/10000:+.1f}w, today={pct_day:+.2f}%{tags_str}'
            lines.append((pct_cost, name, price, cost, pnl/10000, pct_day, tags, line))
        else:
            lines.append((-999, name, 0, cost, 0, 0, [], f'{name}: NO DATA'))
    else:
        lines.append((-999, name, 0, cost, 0, 0, [], f'{name}: NOT FOUND'))

for _, _, _, _, _, _, _, line in sorted(lines):
    print(line)

print('=' * 55)
print(f'Total P&L (w): {total_pnl/10000:+.1f}w')

alert_lines = [l[-1] for l in lines if l[6]]
if alert_lines:
    print('\n== ALERTS ==')
    for a in alert_lines:
        print(a)
