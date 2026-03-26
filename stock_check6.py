import requests
from datetime import datetime

stocks = [
    ('浙江龙盛', '600352', '1'),
    ('同花顺', '300033', '0'),
    ('华工科技', '000988', '0'),
    ('中复神鹰', '688295', '1'),
    ('亨通光电', '600487', '1'),
    ('高澜股份', '300499', '0'),
    ('西部矿业', '601168', '1'),
    ('航发动力', '600893', '1'),
    ('亿能电力', '920046', '0'),
    ('普适导航', '831330', '0'),
    ('圣博润', '430046', '0'),
    ('东睦股份', '600114', '1'),
    ('南网数字', '301638', '0'),
]

print(f"=== 持仓监控 {datetime.now().strftime('%H:%M:%S')} ===\n")

results = []
for name, code, mkt in stocks:
    try:
        secid = f'{mkt}.{code}'
        url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f170,f57,f58'
        resp = requests.get(url, timeout=10)
        d = resp.json()
        if d.get('data'):
            raw_price = d['data'].get('f43', 0)
            raw_chg = d['data'].get('f170', 0)
            
            # 判断价格单位：如果>10000则以"分"为单位，否则以"厘"为单位
            if raw_price > 100000:
                price = raw_price / 10000  # 万分之一，即"厘"
                change = raw_chg / 100
            elif raw_price > 1000:
                price = raw_price / 100  # 百分之一，即"分"/元
                change = raw_chg / 100
            elif raw_price > 0:
                price = raw_price
                change = raw_chg / 100
            else:
                price = 0
                change = 0
            
            chg_str = f"{change:+.2f}%"
            results.append((name, code, price, change))
            print(f"{name}({code}): {price:.2f} ({chg_str})")
        else:
            print(f"{name}({code}): 无数据")
            results.append((name, code, None, None))
    except Exception as e:
        print(f"{name}({code}): 错误-{e}")
        results.append((name, code, None, None))

print()
print("=== 止损位检查 ===")
stop_loss = {
    '600352': ('浙江龙盛', 12.0),
    '300033': ('同花顺', 280.0),
    '300499': ('高澜股份', 38.0),
    '920046': ('亿能电力', 27.0),
    '600114': ('东睦股份', 25.0),
    '301638': ('南网数字', 28.0),
}
for name, code, price, change in results:
    if code in stop_loss and price is not None and price > 0:
        nm, sl = stop_loss[code]
        if price <= sl:
            print(f"[ALERT] {nm}({code}) 现价{price:.2f} <= 止损位{sl} !")
        else:
            print(f"  {nm}({code}) 现价{price:.2f} > 止损位{sl} [OK]")
