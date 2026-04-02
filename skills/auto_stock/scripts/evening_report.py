"""
龙虾盘后复盘 v2.0
资金: 73万基准 | 中线30万+短线25万+子弹18万
"""
import requests, datetime

API = "https://stockboot.jiuma.cn/api"
TOTAL_CASH = 730000

# 中线持仓（趋势股）
MIDDLE = [
    # {"name":"", "code":"", "shares":0, "cost":0, "stop":0, "buy_date":""},
]

# 短线持仓（超短1-3天）
SHORT = [
    # {"name":"", "code":"", "shares":0, "cost":0, "buy_price":0, "buy_date":""},
]

def get_price(code):
    try:
        r = requests.get(f"https://qt.gtimg.cn/q={code}", timeout=5)
        d = r.text.split("~")
        return float(d[3]) if len(d) > 3 else None
    except:
        return None

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
report = f"[龙虾盘后复盘] {now}\n"

# 中线
report += "\n【中线持仓】\n"
mid_total = 0
mid_cost = 0
for p in MIDDLE:
    price = get_price(p["code"])
    if not price: continue
    v = price * p["shares"]
    c = p["cost"] * p["shares"]
    profit = v - c
    pct = profit / c * 100
    hold = (datetime.datetime.now() - datetime.datetime.strptime(p["buy_date"], "%Y-%m-%d")).days
    dist = (price - p["stop"]) / p["stop"] * 100
    flag = "!!止损近" if dist < 8 else ("关注" if dist < 15 else "正常")
    report += f"{p['name']} {price:.2f} ({pct:+.1f}%) 持{hold}天 [{flag}]\n"
    mid_total += v
    mid_cost += c

# 短线
report += "\n【短线持仓】\n"
sht_total = 0
sht_cost = 0
for p in SHORT:
    price = get_price(p["code"])
    if not price: continue
    v = price * p["shares"]
    c = p["cost"] * p["shares"]
    profit = v - c
    pct = profit / c * 100
    hold = (datetime.datetime.now() - datetime.datetime.strptime(p["buy_date"], "%Y-%m-%d")).days
    stop_p = round(p["buy_price"] * 0.96, 2)
    if pct <= -3: flag = "止损!"
    elif pct >= 8: flag = "止盈!"
    elif hold >= 3: flag = "3天强制出!"
    else: flag = "持有"
    report += f"{p['name']} {price:.2f} ({pct:+.1f}%) 持{hold}天 [{flag}]\n"
    sht_total += v
    sht_cost += c

# 汇总
total_v = mid_total + sht_total
total_cost = mid_cost + sht_cost
profit = total_v - total_cost
pos_pct = total_cost / TOTAL_CASH * 100
report += f"\n总盈亏: {profit/10000:+.1f}万 | 总仓位: {pos_pct:.0f}%"
report += f"\n剩余现金: {(TOTAL_CASH-total_cost)/10000:.0f}万"
report += f"\n\n子弹(18万): 大盘跌到位/恐慌时出击"
report += f"\n\n【明日计划】\n- 检查中线趋势是否破坏\n- 检查短线是否触发止损/止盈/3天规则\n- 根据盘前报告决定是否开新仓"
print(report)
