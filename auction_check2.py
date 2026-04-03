import urllib.request

# 指数
indexes = [
    ("sh000001", "上证指数"),
    ("sz399001", "深证成指"),
    ("sz399006", "创业板"),
    ("sh000300", "沪深300"),
]

for code, name in indexes:
    url = f"https://qt.gtimg.cn/q={code}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = parts[3]
                change = parts[31] if len(parts) > 31 else "N/A"
                change_pct = parts[32] if len(parts) > 32 else "N/A"
                vol = parts[36] if len(parts) > 36 else "N/A"
                print(f"{name}: {price} 涨跌{change} ({change_pct}%) 量{vol}")
    except Exception as e:
        print(f"{name}: {e}")
