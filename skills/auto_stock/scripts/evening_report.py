"""
龙虾盘后复盘 v1.0
每天15:10自动推送持仓分析+明日计划
"""
import requests, datetime, json

API = "https://stockboot.jiuma.cn/api"
CAPITAL = 800000
POSITIONS = [
    {"name":"浙江龙盛",  "code":"sh600352", "shares":76700,  "cost":16.948, "buy_date":"2026-03-20"},
    {"name":"同花顺",    "code":"sz300033", "shares":1200,   "cost":423.488,"buy_date":"2026-03-20"},
    {"name":"亨通光电",  "code":"sh600487", "shares":500,    "cost":43.210, "buy_date":"2026-03-25"},
    {"name":"航发动力",  "code":"sh600893", "shares":1000,   "cost":49.184, "buy_date":"2026-03-25"},
    {"name":"西部矿业",  "code":"sh601168", "shares":11000,  "cost":26.169, "buy_date":"2026-03-20"},
    {"name":"黄金ETF",  "code":"sh518880", "shares":24000,  "cost":9.868,  "buy_date":"2026-03-31"},
    {"name":"农业银行",  "code":"sh601288", "shares":15000,  "cost":6.921,  "buy_date":"2026-04-02"},
    {"name":"东睦股份",  "code":"sh600114", "shares":11100,  "cost":31.176, "buy_date":"2026-03-20"},
    {"name":"特变电工",  "code":"sh600089", "shares":52300,  "cost":24.765, "buy_date":"2026-03-20"},
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

total_value = 0
total_cost = 0
alerts = []

for p in POSITIONS:
    price = get_price(p["code"])
    if not price:
        continue
    value = price * p["shares"]
    cost = p["cost"] * p["shares"]
    profit = value - cost
    pct = profit / cost * 100
    hold = (datetime.datetime.now() - datetime.datetime.strptime(p["buy_date"], "%Y-%m-%d")).days
    stop = round(p["cost"] * 0.96, 2)
    dist = (price - stop) / stop * 100
    total_value += value
    total_cost += cost

    flag = ""
    if dist < 8: flag = "!!距止损近"
    if pct > 15: flag = "止盈线!"
    elif pct < -15: flag = "深套!"
    elif hold > 3 and pct < 2: flag = "3天不赚，规则出!"

    report += f"{p['name']} {price:.2f} ({pct:+.1f}%) 持{hold}天 {flag}\n"

    if flag:
        alerts.append(f"{p['name']}: {flag}")

total_profit = total_value - total_cost
pos_pct = total_cost / CAPITAL * 100
report += f"\n总盈亏: {total_profit/10000:+.1f}万 | 仓位: {pos_pct:.0f}%"
if pos_pct > 70:
    report += " [仓位超限!]"
report += f"\n剩余现金: {(CAPITAL-total_cost)/10000:.0f}万"

if alerts:
    report += "\n\n【操作预警】\n" + "\n".join(alerts)
report += "\n\n【明日计划】\n- 检查持仓是否触发止损/止盈\n- 大盘环境决定是否开新仓"
print(report)
