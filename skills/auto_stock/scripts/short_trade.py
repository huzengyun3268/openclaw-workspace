"""
龙虾激进短线交易系统 v1.0
资金: 80万基准 | 单票上限: 24万(30%) | 总仓上限: 56万(70%)
止损: -4% | 止盈: 8%/12%/15% | 超短: 1-3天
用法: python short_trade.py [命令]
命令: 选股/持仓/风控/热点/清仓
"""

import requests
import datetime
import sys

API = "https://stockboot.jiuma.cn/api"
CAPITAL = 800000       # 80万基准
MAX_PER = 0.30         # 单票上限30%
MAX_TOTAL = 0.70       # 总仓上限70%
STOP_LOSS = 0.04       # 止损4%
TAKE_PROFIT_1 = 0.08   # 止盈第一档8%
TAKE_PROFIT_2 = 0.12   # 止盈第二档12%
TAKE_PROFIT_3 = 0.15   # 止盈第三档15%

# ========== 持仓配置 ==========
# 每次买卖后手动更新这里
POSITIONS = [
    # {"name":"", "code":"", "shares":0, "cost":0, "buy_date":"", "note":""},
    # 示例: {"name":"XXX", "code":"sh600xxx", "shares":10000, "cost":10.50, "buy_date":"2026-04-02", "note":"短线"},
]

# ========== 自选股池 ==========
WATCH_POOL = [
    # {"name":"", "code":"", "min_price":0, "max_price":0, "reason":""},
]

def get_price(code):
    try:
        url = f"https://qt.gtimg.cn/q={code}"
        r = requests.get(url, timeout=5)
        d = r.text.split("~")
        if len(d) < 45:
            return None
        return {
            "name": d[1], "price": float(d[3]),
            "pct": float(d[32]), "high": float(d[33]),
            "low": float(d[34]), "vol": float(d[36]),
            "turnover": float(d[38]), "vr": float(d[37]),
        }
    except:
        return None

def wencai(sentence):
    try:
        r = requests.post(f"{API}/dynamic-select/execute",
                          json={"sentence": sentence}, timeout=30)
        return r.json()
    except:
        return {}

def calc_trade(price):
    """根据股价计算仓位"""
    max_amount = CAPITAL * MAX_PER
    shares = int(max_amount / price / 100) * 100
    amount = shares * price
    stop_price = round(price * (1 - STOP_LOSS), 2)
    tp1 = round(price * (1 + TAKE_PROFIT_1), 2)
    tp2 = round(price * (1 + TAKE_PROFIT_2), 2)
    tp3 = round(price * (1 + TAKE_PROFIT_3), 2)
    risk = amount * STOP_LOSS
    return {
        "shares": shares, "amount": amount,
        "stop": stop_price, "tp1": tp1, "tp2": tp2, "tp3": tp3,
        "risk": risk, "capital_used_pct": amount / CAPITAL * 100,
    }

def cmd_select():
    """选股: 热点强势"""
    print(f"\n{'='*55}")
    print(f"[{datetime.datetime.now().strftime('%H:%M')}] 激进短线选股 - 热点强势模式")
    print(f"{'='*55}")

    sents = [
        ("主线突破", "涨幅大于5%小于12%;换手率大于8%;流通市值小于300亿;非ST;非一字涨停;量比大于1.5"),
        ("回踩低吸", "涨幅大于1%小于5%;换手率大于5%;流通市值小于200亿;非ST;近5日跌幅大于5%"),
        ("板块龙头", "涨幅大于5%小于15%;换手率大于10%;非ST;非新股"),
    ]

    for label, sent in sents:
        print(f"\n--- {label} ---")
        print(f"条件: {sent}")
        res = wencai(sent)
        stocks = res.get("stocks", [])[:5]
        total = res.get("totalCount", 0)
        print(f"筛出 {total} 只:" if total else "无结果")
        for s in stocks:
            print(f"  {s.get('name','?')} {s.get('code','?')}")

def cmd_positions():
    """持仓分析"""
    if not POSITIONS:
        print("\n持仓为空，请先添加持仓配置")
        return

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'='*55}")
    print(f"[{now}] 持仓分析 | 基准资金: 80万")
    print('='*55)

    total_cost = 0
    total_value = 0
    total_stop_risk = 0
    alerts = []

    for p in POSITIONS:
        d = get_price(p["code"])
        if not d:
            print(f"  {p['name']}: 数据获取失败")
            continue

        price = d["price"]
        pct = d["pct"]
        value = price * p["shares"]
        cost_total = p["cost"] * p["shares"]
        profit = value - cost_total
        profit_pct = profit / cost_total * 100
        hold_days = (datetime.datetime.now() - datetime.datetime.strptime(p["buy_date"], "%Y-%m-%d")).days if p.get("buy_date") else 0
        stop_price = round(p["cost"] * (1 - STOP_LOSS), 2)
        stop_risk = cost_total * STOP_LOSS
        dist_to_stop = (price - stop_price) / price * 100

        total_cost += cost_total
        total_value += value
        total_stop_risk += stop_risk

        # 风险判断
        status = "OK"
        action = ""
        if dist_to_stop < 8:
            status = "WARN"
            alerts.append(f"【{p['name']}】距止损{dist_to_stop:.1f}%，谨慎!")
        if profit_pct >= TAKE_PROFIT_1 * 100:
            status = "TAKE"
            action = f"建议止盈至TP1({round(p['cost']*(1+TAKE_PROFIT_1),2)})"
        if hold_days >= 3 and profit_pct < 2:
            status = "EXIT"
            action = "持有3天不赚钱，规则强制离场!"
        if pct <= -3:
            status = "DANGER"
            action = "跌幅接近止损，密切观察!"

        print(f"\n  {p['name']} {p['code']}")
        print(f"    现价: {price} ({pct:+.2f}%) | 成本: {p['cost']} | 持有: {hold_days}天")
        print(f"    盈亏: {profit/10000:+.1f}万 ({profit_pct:+.1f}%) | 状态: [{status}]")
        print(f"    止损价: {stop_price} (风险{stop_risk/10000:.1f}万) | {action}")

    total_profit = total_value - total_cost
    total_pos_pct = total_cost / CAPITAL * 100
    print(f"\n{'='*55}")
    print(f"  总市值: {total_value/10000:.1f}万 | 总盈亏: {total_profit/10000:+.1f}万")
    print(f"  总仓位: {total_pos_pct:.1f}% (上限70%) | 剩余现金: {(CAPITAL-total_cost)/10000:.1f}万")
    print(f"  最大止损暴露: {total_stop_risk/10000:.1f}万")
    if total_pos_pct > MAX_TOTAL * 100:
        print(f"  !! 仓位超限({total_pos_pct:.0f}%>70%)，建议减仓!")

    if alerts:
        print(f"\n  【预警】")
        for a in alerts:
            print(f"    ! {a}")

def cmd_risk():
    """风控规则说明"""
    print(f"\n{'='*55}")
    print(f"  龙虾激进短线风控规则")
    print(f"{'='*55}")
    print(f"  资金基准: {CAPITAL/10000:.0f}万")
    print(f"  单票上限: {MAX_PER*100:.0f}% = {CAPITAL*MAX_PER/10000:.0f}万")
    print(f"  总仓上限: {MAX_TOTAL*100:.0f}% = {CAPITAL*MAX_TOTAL/10000:.0f}万")
    print(f"  止损线: -{STOP_LOSS*100:.0f}% (触发立即走)")
    print(f"  止盈线: +{TAKE_PROFIT_1*100:.0f}% -> 减半 | +{TAKE_PROFIT_2*100:.0f}% -> 再减半 | +{TAKE_PROFIT_3*100:.0f}% -> 全走")
    print(f"  持有期限: 1-3天(规则强制)")
    print(f"  炸板规则: 涨停炸板 -> 先出一半")
    print(f"  连续止损: 2次后当天禁止开新仓")
    print(f"  大盘冰点: 空仓休息，只看不做")
    print(f"{'='*55}")

def cmd_hot():
    """今日热点方向"""
    print(f"\n{'='*55}")
    print(f"[{datetime.datetime.now().strftime('%H:%M')}] 今日热点方向")
    print(f"{'='*55}")

    hot_blocks = [
        ("军工航天", "涨幅大于3%;换手率大于5%;非ST"),
        ("半导体", "涨幅大于3%;换手率大于5%;非ST"),
        ("AI算力", "涨幅大于3%;换手率大于5%;非ST"),
        ("新质生产力", "涨幅大于3%;换手率大于5%;非ST"),
    ]

    for label, sent in hot_blocks:
        res = wencai(sent)
        stocks = res.get("stocks", [])[:3]
        total = res.get("totalCount", 0)
        if stocks:
            print(f"\n{label} ({total}只涨停/强势):")
            for s in stocks:
                print(f"  {s.get('name')} {s.get('code')}")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "选股":
        cmd_select()
    elif cmd == "持仓":
        cmd_positions()
    elif cmd == "风控":
        cmd_risk()
    elif cmd == "热点":
        cmd_hot()
    elif cmd == "清仓":
        print("\n清仓提醒: 请确认全部持仓已卖出，确认请回复'确认清仓'")
    else:
        print(f"\n龙虾激进短线交易系统 v1.0")
        print(f"用法: python short_trade.py [命令]")
        print(f"命令: 选股/持仓/风控/热点/清仓")

if __name__ == "__main__":
    main()
