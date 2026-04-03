import requests
import urllib.request
import json
from datetime import datetime

headers = {
    'Referer': 'http://finance.sina.com.cn',
    'User-Agent': 'Mozilla/5.0'
}

codes = 'sh600352,sz300033,sh600487,sh600893,sh601168,sh518880,sz430046'
url = f'https://hq.sinajs.cn/list={codes}'

req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')

positions = {
    'sh600352': ('浙江龙盛', 76700, 16.948, 12.0),
    'sz300033': ('同花顺', 1200, 423.488, 280.0),
    'sh600487': ('亨通光电', 3000, 43.210, 38.0),
    'sh600893': ('航发动力', 9000, 49.184, 42.0),
    'sh601168': ('西部矿业', 11000, 26.169, 22.0),
    'sh518880': ('黄金ETF', 24000, 9.868, None),
    'sz430046': ('圣博润', 10334, 0.478, None),
}

lines = data.strip().split('\n')
print(f"=== 持仓监控 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")

alerts = []
for line in lines:
    if '=' not in line:
        continue
    parts = line.split('"')
    if len(parts) < 2:
        continue
    code = line.split('=')[0].split('_')[-1]
    vals = parts[1].split(',')
    if len(vals) < 10:
        continue
    
    name = vals[0]
    price = float(vals[3])
    pre_close = float(vals[2])
    chg_pct = (price - pre_close) / pre_close * 100
    
    if code in positions:
        pname, vol, cost, stop = positions[code]
        profit = (price - cost) * vol
        flag = ""
        if stop and price < stop:
            flag = " [止损警告]"
        elif price < cost * 0.9:
            flag = " [深套]"
        print(f"{pname}: {price:.3f}  {chg_pct:+.2f}%  盈亏{profit:+.0f}元{flag}")
        if stop and price < stop:
            alerts.append(f"{pname}现价{price:.3f}低于止损价{stop}元!")
    else:
        print(f"{name}: {price:.3f}  {chg_pct:+.2f}%")

if alerts:
    print("\n=== 预警 ===")
    for a in alerts:
        print(a)
else:
    print("\n暂无预警，持仓正常。")
