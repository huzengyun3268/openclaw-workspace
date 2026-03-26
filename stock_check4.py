import requests
from datetime import datetime

stocks = [
    ('浙江龙盛', '600352'),
    ('同花顺', '300033'),
    ('华工科技', '000988'),
    ('中复神鹰', '688295'),
    ('亨通光电', '600487'),
    ('高澜股份', '300499'),
    ('西部矿业', '601168'),
    ('航发动力', '600893'),
    ('亿能电力', '920046'),
    ('普适导航', '831330'),
    ('圣博润', '430046'),
]

print(f"=== 持仓监控 {datetime.now().strftime('%H:%M:%S')} ===\n")

for name, code in stocks:
    try:
        if code.startswith('6'):
            secid = f'1.{code}'
        elif code.startswith('9'):
            secid = f'0.{code}'  # 北交所
        elif code.startswith('8') or code.startswith('4'):
            secid = f'0.{code}'  # 新三板
        else:
            secid = f'0.{code}'
        
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f170,f57,f58'
        resp = requests.get(url, timeout=10)
        d = resp.json()
        if d.get('data'):
            price = d['data'].get('f43', 'N/A')
            change = d['data'].get('f170', 0)
            print(f"{name}({code}): {price} ({change:+.2f}%)")
        else:
            print(f"{name}({code}): 无数据")
    except Exception as e:
        print(f"{name}({code}): 错误-{e}")

print()
print("=== 止损位检查 ===")
# This requires re-fetching, but for brevity just hardcode alert checks
checks = [
    ('浙江龙盛', '600352', 12.0),
    ('同花顺', '300033', 280.0),
    ('高澜股份', '300499', 38.0),
    ('亿能电力', '920046', 27.0),
]
for name, code, sl in checks:
    try:
        if code.startswith('6'):
            secid = f'1.{code}'
        elif code.startswith('9'):
            secid = f'0.{code}'
        elif code.startswith('8') or code.startswith('4'):
            secid = f'0.{code}'
        else:
            secid = f'0.{code}'
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43'
        resp = requests.get(url, timeout=10)
        d = resp.json()
        if d.get('data'):
            price = float(d['data'].get('f43', 0))
            if price > 0 and price <= sl:
                print(f"⚠️ {name}({code}) 现价{price} <= 止损位{sl} !")
            elif price > 0:
                print(f"  {name}({code}) 现价{price} > 止损位{sl} ✓")
    except:
        pass
