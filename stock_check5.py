# -*- coding: utf-8 -*-
import urllib.request
import json

codes = [
    ('sh600352', 16.52, 120000, '止损12.0'),
    ('sh600893', 49.184, 9000, '止损42.0'),
    ('sz300033', 423.488, 1200, '止损280'),
    ('sh601168', 26.169, 11000, '止损22.0'),
    ('bj831330', 20.361, 7370, '止损18.0'),
    ('sh600487', 43.998, 3000, '止损38.0'),
    ('sh688295', 37.843, 1500, ''),
    ('bj920046', 329.553, 200, '观察'),
    ('bj430046', 0.478, 10334, ''),
]

names = {
    'sh600352': '浙江龙盛', 'sh600893': '航发动力', 'sz300033': '同花顺',
    'sh601168': '西部矿业', 'bj831330': '普适导航', 'sh600487': '亨通光电',
    'sh688295': '中复神鹰', 'bj920046': '亿能电力', 'bj430046': '圣博润',
}

url = 'https://hq.sinajs.cn/list=' + ','.join([c[0] for c in codes])

req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.sina.com.cn',
})

results = {}
try:
    resp = urllib.request.urlopen(req, timeout=15)
    raw = resp.read()
    try:
        content = raw.decode('gbk')
    except:
        content = raw.decode('utf-8', errors='replace')
    
    for line in content.strip().split('\n'):
        if '=' not in line:
            continue
        var = line.split('=')[0].replace('hq_str_', '').strip()
        try:
            data = line.split('"')[1]
        except:
            continue
        fields = data.split(',')
        if len(fields) < 5:
            continue
        price = float(fields[3])
        prev = float(fields[2])
        chg = (price - prev) / prev * 100
        results[var] = {'price': price, 'chg': chg}
except Exception as e:
    pass

# Build output
output_lines = []
output_lines.append("=== 主账户持仓 13:30 ===")
for code, cost, qty, stop in codes:
    name = names.get(code, code)
    if code in results:
        r = results[code]
        p = r['price']
        c = r['chg']
        pl = (p - cost) * qty
        pl_str = f"{pl:+.0f}"
        alert = ""
        if stop and '止损' in stop and p < float(stop.replace('止损','')):
            alert = " **预警**"
        output_lines.append(f"{name}: {p}  {c:+.2f}%  浮动{pl_str}元{alert}")
    else:
        output_lines.append(f"{name}: N/A")

# 亿能电力单独说明
if 'bj920046' in results:
    r = results['bj920046']
    output_lines.append(f"\n亿能电力({r['price']}): 成本329.55，跌幅极大，止损观察中")

content_out = '\n'.join(output_lines)
print(content_out)

# Save to file
with open('C:/Users/Administrator/.openclaw/workspace/stock_result.txt', 'w', encoding='utf-8') as f:
    f.write(content_out)
