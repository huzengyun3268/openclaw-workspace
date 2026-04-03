import requests
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

codes = [
    ('sh600352', '浙江龙盛'),
    ('sz300033', '同花顺'),
    ('sh600487', '亨通光电'),
    ('sh600893', '航发动力'),
    ('sh601168', '西部矿业'),
    ('sh518880', '黄金ETF'),
    ('sz430046', '圣博润'),
    ('sh600114', '东睦(老婆)'),
    ('sh600089', '特变(两融)'),
]

results = []
for code, name in codes:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        resp = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        text = resp.text
        parts = text.split('~')
        if len(parts) > 10:
            price = float(parts[3]) if parts[3] else 0
            yesterday = float(parts[4]) if parts[4] else 0
            chg = ((price - yesterday) / yesterday * 100) if yesterday > 0 else 0
            results.append((name, code, price, chg))
            print(f'{name}({code}): {price} ({chg:+.2f}%)')
        else:
            print(f'{name}({code}): 解析失败')
            results.append((name, code, 0, 0))
    except Exception as e:
        print(f'{name}({code}): 获取失败 {e}')
        results.append((name, code, 0, 0))
    time.sleep(0.2)

print('')
print('=== 持仓盈亏 ===')
positions = [
    ('浙江龙盛',    'sh600352', 76700,  16.948, 12.0),
    ('同花顺',      'sz300033',  1200, 423.488, 280.0),
    ('亨通光电',    'sh600487',  3000,  43.210,  38.0),
    ('航发动力',    'sh600893',  9000,  49.184,  42.0),
    ('西部矿业',    'sh601168', 11000,  26.169,  22.0),
    ('黄金ETF',     'sh518880', 24000,   9.868,  None),
    ('圣博润',      'sz430046', 10334,   0.478,  None),
    ('东睦(老婆)',  'sh600114', 11100,  31.176,  25.0),
    ('特变(两融)',  'sh600089', 52300,  24.765,  25.0),
]

total_pnl = 0
alerts = []
for name, code, shares, cost, stop in positions:
    price = None
    for rname, rcode, rprice, rchg in results:
        if rcode == code:
            price = rprice
            break
    if price and price > 0:
        pnl = (price - cost) * shares
        total_pnl += pnl
        flag = ''
        if stop and price <= stop:
            flag = ' [触碰止损]'
        elif stop and price <= cost * 0.95:
            flag = ' [低于成本5%]'
        print(f'{name}: 现价{price:.3f} | 成本{cost} | 盈亏{pnl:+,.0f}元{flag}')
        if flag:
            alerts.append(f'{name}{flag}')
    else:
        print(f'{name}: 暂无数据')

print('')
print(f'总盈亏(估算): {total_pnl:+,.0f}元')
if alerts:
    print('告警: ' + ' '.join(alerts))
