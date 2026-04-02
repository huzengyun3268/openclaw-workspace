"""
龙虾持仓监控脚本 v1.0
监控老胡的持仓状态，触发预警自动打印
用法: python monitor_positions.py
"""

import requests
import datetime

# ========== 持仓配置（老胡账户） ==========
POSITIONS = [
    # 主账户
    {"name": "浙江龙盛",  "code": "sh600352", "shares": 76700,  "cost": 16.948, "stop": 12.0, "account": "主3293"},
    {"name": "同花顺",    "code": "sz300033", "shares": 1200,   "cost": 423.488,"stop": 280.0, "account": "主3293"},
    {"name": "亨通光电",  "code": "sh600487", "shares": 500,    "cost": 43.210, "stop": 38.0,  "account": "主3293"},
    {"name": "航发动力",  "code": "sh600893", "shares": 1000,   "cost": 49.184, "stop": 42.0,  "account": "主3293"},
    {"name": "西部矿业",  "code": "sh601168", "shares": 11000,  "cost": 26.169, "stop": 22.0,  "account": "主3293"},
    {"name": "黄金ETF",  "code": "sh518880", "shares": 24000,  "cost": 9.868,  "stop": 0,     "account": "主3293"},
    {"name": "农业银行",  "code": "sh601288", "shares": 15000,  "cost": 6.921,  "stop": 0,     "account": "主3293"},
    # 老婆账户
    {"name": "东睦股份",  "code": "sh600114", "shares": 11100,  "cost": 31.176, "stop": 25.0,  "account": "老婆"},
    # 两融账户
    {"name": "特变电工",  "code": "sh600089", "shares": 52300,  "cost": 24.765, "stop": 25.0,  "account": "两融2306"},
]

def get_price(code):
    url = f'https://qt.gtimg.cn/q={code}'
    r = requests.get(url, timeout=5)
    d = r.text.split('~')
    if len(d) < 45:
        return None
    price = float(d[3])
    pct = float(d[32])
    high = float(d[33])
    low = float(d[34])
    return {"price": price, "pct": pct, "high": high, "low": low}

def check_positions():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'='*60}")
    print(f"[{now}] 龙虾持仓监控")
    print('='*60)

    alerts = []
    total_profit = 0
    total_cost = 0

    # 分组显示
    groups = {}
    for p in POSITIONS:
        acc = p["account"]
        if acc not in groups:
            groups[acc] = []
        groups[acc].append(p)

    for acc, positions in groups.items():
        print(f"\n【{acc}】")
        acc_profit = 0
        acc_cost = 0

        for p in positions:
            data = get_price(p["code"])
            if not data:
                print(f"  {p['name']} {p['code']}: 数据获取失败")
                continue

            price = data["price"]
            pct = data["pct"]
            profit = (price - p["cost"]) * p["shares"]
            profit_pct = (price - p["cost"]) / p["cost"] * 100
            acc_profit += profit
            acc_cost += p["cost"] * p["shares"]
            total_profit += profit
            total_cost += p["cost"] * p["shares"]

            # 状态判断
            stop_dist = (price - p["stop"]) / p["stop"] * 100 if p["stop"] > 0 else None
            if stop_dist is not None and stop_dist < 10:
                status = ""
                alerts.append(f"【{acc}】{p['name']}距止损仅{stop_dist:.1f}%！")
            elif profit > 0:
                status = "ok"
            else:
                status = "zb"

            stop_str = f" | 距止损{stop_dist:.1f}%" if stop_dist else ""
            print(f"  {status} {p['name']} {price:.2f} ({pct:+.2f}%) 成本{p['cost']:.3f} {profit/10000:+.1f}万({profit_pct:+.1f}%){stop_str}")

        print(f"  小计: {acc_profit/10000:+.1f}万")

    print(f"\n{'='*60}")
    print(f" 总盈亏: {total_profit/10000:+.1f}万 (成本{int(total_cost/10000)}万)")

    # 预警
    if alerts:
        print(f"\n!! 【预警】")
        for a in alerts:
            print(f"    {a}")

    print()
    return alerts

if __name__ == "__main__":
    check_positions()
