import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# All stocks: (code, name, cost, shares, stop_loss, account, is_bj)
# account: 主账户/老婆账户/两融账户
stocks_config = [
    # Main account
    ("600352", "浙江龙盛", 15.952, 106700, 12.0, "主账户", False),
    ("300033", "同花顺", 423.488, 1200, 280.0, "主账户", False),
    ("831330", "普适导航", 20.361, 7370, None, "主账户", True),  # NEEQ
    ("000988", "华工科技", 116.87, 1000, None, "主账户", False),
    ("688295", "中复神鹰", 37.843, 1500, None, "主账户", False),
    ("600487", "亨通光电", 42.391, 2000, None, "主账户", False),
    ("300499", "高澜股份", 41.625, 1500, 38.0, "主账户", False),
    ("601168", "西部矿业", 24.863, 2000, None, "主账户", False),
    ("600893", "航发动力", 47.196, 1000, None, "主账户", False),
    ("920046", "亿能电力", 329.555, 200, 27.0, "主账户", True),  # Beijing
    ("430046", "圣博润", 0.478, 10334, None, "主账户", True),  # NEEQ
    # Wife account
    ("600114", "东睦股份", 25.9, 4800, 25.0, "老婆账户", False),
    ("301638", "南网数字", 32.635, 1700, 28.0, "老婆账户", False),
    # Margin account
    ("600089", "特变电工", 24.765, 52300, 25.0, "两融账户", False),
]

# Separate A-shares from NEEQ/Beijing
a_stocks = [(c, n, co, sh, sl, acc) for c, n, co, sh, sl, acc, is_bj in stocks_config if not is_bj]
bj_stocks = [(c, n, co, sh, sl, acc) for c, n, co, sh, sl, acc, is_bj in stocks_config if is_bj]

# Get A-share quotes
quote_list = []
for code, *_ in a_stocks:
    if code.startswith(('6', '9')):
        quote_list.append(f"1.{code}")
    else:
        quote_list.append(f"0.{code}")

url = "http://push2.eastmoney.com/api/qt/ulist.np/get"
params = {
    "fltt": 2,
    "invt": 2,
    "fields": "f2,f3,f12,f14",
    "secids": ",".join(quote_list)
}

quotes = {}
try:
    resp = requests.get(url, params=params, timeout=10)
    data = resp.json()
    if data.get("rc") == 0 and data.get("data", {}).get("diff"):
        for item in data["data"]["diff"]:
            code = item["f12"]
            quotes[code] = {
                "price": item["f2"],
                "change_pct": item["f3"]
            }
except Exception as e:
    print(f"获取A股行情失败: {e}")

# Get Beijing/NEEQ quotes separately
for code, name, cost, shares, sl, acc in bj_stocks:
    try:
        if code.startswith('9'):
            secid = f"1.{code}"  # Beijing
        else:
            secid = f"0.{code}"  # NEEQ
        url2 = "http://push2.eastmoney.com/api/qt/stock/get"
        params2 = {"secid": secid, "fltt": 2, "invt": 2, "fields": "f2,f3,f12,f14"}
        r = requests.get(url2, params=params2, timeout=5)
        d = r.json()
        if d.get("data"):
            item = d["data"]
            quotes[code] = {
                "price": item.get("f2"),
                "change_pct": item.get("f3")
            }
        else:
            quotes[code] = {"price": None, "change_pct": None}
    except:
        quotes[code] = {"price": None, "change_pct": None}

# Now generate report
print("=" * 70)
print("📈 持仓监控  2026-03-26 10:00")
print("=" * 70)

total_pl = 0
alerts = []

for account_type in ["主账户", "老婆账户", "两融账户"]:
    acc_stocks = [(c, n, co, sh, sl) for c, n, co, sh, sl, acc in stocks_config if acc == account_type]
    print(f"\n【{account_type}】")
    print("-" * 60)
    for code, name, cost, shares, sl in acc_stocks:
        q = quotes.get(code, {})
        price = q.get("price")
        change_pct = q.get("change_pct")
        
        if price is None or price == "-":
            print(f"  {code} {name}: ⚠️ 行情获取失败")
            continue
        
        try:
            price = float(price)
            change_pct = float(change_pct) if change_pct else 0
        except:
            print(f"  {code} {name}: ⚠️ 数据解析异常")
            continue
        
        pl = (price - cost) * shares
        pl_pct = (price - cost) / cost * 100
        total_pl += pl
        
        emoji = "🔴" if pl < 0 else "🟢"
        
        # Status indicators
        status_parts = []
        if change_pct >= 9.9:
            status_parts.append("【涨停】")
        elif change_pct <= -9.9:
            status_parts.append("【跌停】")
        if sl and price <= sl:
            alerts.append(f"🚨 {name}({code}) 现价{price:.2f}元 ≤ 止损{sl}元！")
            status_parts.append("⚠️触及止损")
        
        status_str = " ".join(status_parts)
        
        print(f"  {emoji} {name}({code})")
        print(f"     现价:{price:.2f}  涨跌:{change_pct:+.2f}%  {status_str}")
        print(f"     成本:{cost:.2f}  盈亏:{pl:+.0f}元({pl_pct:+.1f}%)  持仓:{shares}股")

print(f"\n{'=' * 70}")
print(f"📊 持仓总盈亏: {total_pl:+.0f} 元")

if alerts:
    print(f"\n{'=' * 70}")
    print("🚨 【预警提醒】")
    for a in alerts:
        print(f"  {a}")
