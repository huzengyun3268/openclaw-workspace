# -*- coding: utf-8 -*-
import urllib.request

# Sina API: fields[1]=yesterday_close, fields[3]=current_price
codes = [
    ('sh600352', 16.52, 86700, 12.0, '止损12.0'),
    ('sh600893', 49.184, 9000, 42.0, '止损42.0'),
    ('sz300033', 423.488, 1200, 280.0, '止损280'),
    ('sh601168', 26.169, 11000, 22.0, '止损22.0'),
    ('bj831330', 20.361, 7370, 18.0, '止损18.0'),
    ('sh600487', 43.998, 3000, 38.0, '止损38.0'),
    ('sh688295', 37.843, 1500, None, ''),
    ('bj920046', 329.553, 200, None, '观察'),
    ('bj430046', 0.478, 10334, None, ''),
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
    content = raw.decode('gbk', errors='replace')
    
    for line in content.strip().split('\n'):
        if '=' not in line or '=""' in line:
            continue
        # Extract variable name: "var hq_str_sh600352" -> "sh600352"
        var = line.split('=')[0].replace('hq_str_', '').replace('var ', '').strip()
        try:
            data = line.split('"')[1]
        except:
            continue
        fields = data.split(',')
        if len(fields) < 6:
            continue
        try:
            price = float(fields[3])
            prev_close = float(fields[1])
            chg = (price - prev_close) / prev_close * 100
            results[var] = {'price': price, 'chg': chg}
        except:
            pass
except Exception as e:
    print(f"API Error: {e}")

lines = []
lines.append("=== 主账户持仓 13:30 ===")
for code, cost, qty, stop_px, stop_label in codes:
    name = names.get(code, code)
    if code in results:
        r = results[code]
        p = r['price']
        c = r['chg']
        pl = (p - cost) * qty
        alert = ""
        if stop_px and p < stop_px:
            alert = " ⚠️触及止损"
        lines.append(f"{name}: {p:.3f}  {c:+.2f}%  浮动{pl:+.0f}元{alert}")
    else:
        lines.append(f"{name}: 无数据(停牌或退市)")

lines.append("")
lines.append("=== 止损位监控 ===")
for code, cost, qty, stop_px, stop_label in codes:
    if code in results and stop_px:
        r = results[code]
        p = r['price']
        dist = (p - stop_px) / stop_px * 100
        if dist < 5:
            lines.append(f"⚠️ {names.get(code,code)}: 现价{p:.3f} vs 止损{stop_px} (距止损{dist:+.1f}%)")
        else:
            lines.append(f"{names.get(code,code)}: 现价{p:.3f} vs 止损{stop_px} ({dist:+.1f}%)")

content = '\n'.join(lines)
print(content)

with open('C:/Users/Administrator/.openclaw/workspace/stock_result.txt', 'w', encoding='utf-8') as f:
    f.write(content)
