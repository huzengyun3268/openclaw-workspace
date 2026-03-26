import requests
import json

# All stocks
stocks = [
    ("600352", "浙江龙盛", 15.952, 106700, 12.0),
    ("300033", "同花顺", 423.488, 1200, 280.0),
    ("000988", "华工科技", 116.87, 1000, None),
    ("688295", "中复神鹰", 37.843, 1500, None),
    ("600487", "亨通光电", 42.391, 2000, None),
    ("300499", "高澜股份", 41.625, 1500, 38.0),
    ("601168", "西部矿业", 24.863, 2000, None),
    ("600893", "航发动力", 47.196, 1000, None),
    ("920046", "亿能电力", 329.555, 200, 27.0),
    ("600114", "东睦股份", 25.9, 4800, 25.0),
    ("301638", "南网数字", 32.635, 1700, 28.0),
    ("600089", "特变电工", 24.765, 52300, 25.0),
]

# Get quotes from eastmoney realtime API
codes = ";".join([f"{c}.{('sh' if c.startswith(('6','9')) else 'sz')}" for c, *_ in stocks])
# Note: 920xxx is Beijing exchange, needs different prefix
# Let me use the full API
# Actually let me use a simpler fetch approach

# Build quote codes for eastmoney
quote_list = []
for code, *_ in stocks:
    if code.startswith('6') or code.startswith('9'):
        quote_list.append(f"1.{code}")
    elif code.startswith('8') or code.startswith('4'):
        # Beijing/NEEQ
        quote_list.append(f"0.{code}")
    else:
        quote_list.append(f"0.{code}")

# Try eastmoney snapshot API
url = "http://push2.eastmoney.com/api/qt/ulist.np/get"
params = {
    "fltt": 2,
    "invt": 2,
    "fields": "f1,f2,f3,f4,f12,f14",
    "secids": ",".join(quote_list)
}

try:
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    print("Eastmoney API result:", json.dumps(data, ensure_ascii=False, indent=2))
except Exception as e:
    print(f"Error: {e}")
    # Fallback: try individual fetches
    print("\nFalling back to individual stock fetches...")
    
    base_url = "http://push2.eastmoney.com/api/qt/stock/get"
    results = {}
    for code, name, cost, shares, sl in stocks:
        if code.startswith(('6', '9')):
            secid = f"1.{code}"
        else:
            secid = f"0.{code}"
        
        params = {
            "secid": secid,
            "fltt": 2,
            "invt": 2,
            "fields": "f2,f3,f4,f12,f14"
        }
        try:
            r = requests.get(base_url, params=params, timeout=5)
            d = r.json()
            results[code] = d
        except Exception as ex:
            results[code] = {"error": str(ex)}
    
    for code, d in results.items():
        print(f"{code}: {d}")
