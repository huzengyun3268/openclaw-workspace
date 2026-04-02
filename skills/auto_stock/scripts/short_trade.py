"""
龙虾激进短线交易系统 v2.0
资金: 73万基准 | 死钱: 龙盛76手(套牢)
中线30万 + 短线25万 + 子弹18万
止损: -4% | 止盈: 8-12-15% | 超短1-3天
"""

import requests
import datetime
import sys

API = "https://stockboot.jiuma.cn/api"

# ========== 资金配置 ==========
TOTAL_CASH = 730000        # 73万可用现金
MIDDLE_POS = 300000        # 中线仓位30万
SHORT_POS = 250000         # 短线仓位25万
BULLET = 180000            # 备用子弹18万
MAX_PER = 0.30             # 单票上限30%
MAX_TOTAL = 0.70           # 总仓上限70%（留子弹）
STOP_LOSS = 0.04           # 止损4%
TP1 = 0.08                 # 止盈第一档8%
TP2 = 0.12                 # 止盈第二档12%
TP3 = 0.15                 # 止盈第三档15%

# ========== 持仓配置 ==========
# 每次买卖后手动更新
# MIDDLE: 中线持仓（趋势为主，持有1-3个月）
MIDDLE_POSITIONS = [
    # {"name":"", "code":"", "shares":0, "cost":0, "stop":0, "buy_date":"", "reason":""},
]

# SHORT: 短线持仓（1-3天，超短）
SHORT_POSITIONS = [
    # {"name":"", "code":"", "shares":0, "cost":0, "buy_date":"", "buy_price":0, "note":""},
]

# ========== 历史记录（用于计算连续止损）==========
STOP_LOSS_COUNT = 0  # 连续止损次数，明天开盘前重置
LAST_STOP_DATE = ""  # 上次止损日期

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

def calc_shares(price, budget):
    """根据预算计算买入股数"""
    amount = min(budget * MAX_PER, budget)
    shares = int(amount / price / 100) * 100
    return shares, shares * price

def cmd_help():
    print(f"""
龙虾激进短线交易系统 v2.0
资金配置: 73万 | 中线30万 | 短线25万 | 子弹18万

命令:
  选股     - 盘中选股（热点强势/回踩/突破）
  中线     - 查看中线持仓
  短线     - 查看短线持仓
  风控     - 风控规则
  热点     - 今日热点方向
  配仓     - 查看资金配置
""")

def cmd_select():
    now = datetime.datetime.now().strftime("%H:%M")
    print(f"\n[{now}] 盘中选股")

    strategies = [
        ("热点强势", "涨幅大于5%小于12%;换手率大于8%;流通市值小于300亿;非ST;非一字涨停;量比大于1.5"),
        ("回踩低吸", "涨幅大于1%小于5%;换手率大于5%;流通市值小于200亿;非ST;近5日跌幅大于3%"),
        ("超跌反弹", "跌幅大于5%;市盈率小于30;非ST;近5日跌幅大于8%"),
    ]

    for label, sent in strategies:
        res = wencai(sent)
        stocks = res.get("stocks", [])[:5]
        total = res.get("totalCount", 0)
        print(f"\n【{label}】筛出{total}只:")
        for s in stocks:
            print(f"  {s.get('name')} {s.get('code')}")

    print(f"\n短线预算: {SHORT_POS/10000:.0f}万 (单票上限{SHORT_POS*MAX_PER/10000:.0f}万)")
    print("告诉我你想进的股票，我帮你算仓位和止损价")

def cmd_middle():
    if not MIDDLE_POSITIONS:
        print("\n中线持仓为空，等待盘前报告选股")
        return
    print(f"\n{'='*50}")
    print(f"中线持仓 (预算{MIDDLE_POS/10000:.0f}万)")
    print('='*50)
    total_v = 0
    for p in MIDDLE_POSITIONS:
        d = get_price(p["code"])
        if not d:
            print(f"  {p['name']}: 数据获取失败")
            continue
        v = d["price"] * p["shares"]
        cost = p["cost"] * p["shares"]
        profit = v - cost
        pct = profit / cost * 100
        hold = (datetime.datetime.now() - datetime.datetime.strptime(p["buy_date"], "%Y-%m-%d")).days
        dist = (d["price"] - p["stop"]) / p["stop"] * 100
        print(f"\n  {p['name']} {p['code']}")
        print(f"    现价: {d['price']} ({d['pct']:+.2f}%) | 成本: {p['cost']}")
        print(f"    盈亏: {profit/10000:+.1f}万 ({pct:+.1f}%) | 持: {hold}天")
        print(f"    止损: {p['stop']} | 距止损: {dist:.1f}%")
        total_v += v
    print(f"\n中线市值: {total_v/10000:.1f}万")

def cmd_short():
    if not SHORT_POSITIONS:
        print("\n短线持仓为空")
        return
    print(f"\n{'='*50}")
    print(f"短线持仓 (预算{SHORT_POS/10000:.0f}万)")
    print('='*50)
    for p in SHORT_POSITIONS:
        d = get_price(p["code"])
        if not d:
            print(f"  {p['name']}: 数据失败")
            continue
        cost_t = p["cost"] * p["shares"]
        v = d["price"] * p["shares"]
        profit = v - cost_t
        pct = profit / cost_t * 100
        hold = (datetime.datetime.now() - datetime.datetime.strptime(p["buy_date"], "%Y-%m-%d")).days
        stop_price = round(p["buy_price"] * 0.96, 2)
        print(f"\n  {p['name']} {p['code']}")
        print(f"    现价: {d['price']} ({d['pct']:+.2f}%) | 买入价: {p['buy_price']}")
        print(f"    盈亏: {profit/10000:+.1f}万 ({pct:+.1f}%) | 持: {hold}天")
        # 卖出判断
        if d["pct"] <= -3:
            print(f"    >> 止损线! 建议出局")
        elif pct >= TP1 * 100:
            print(f"    >> 止盈线! 建议减半 (TP1={round(p['buy_price']*(1+TP1),2)})")
        elif hold >= 3:
            print(f"    >> 持有3天! 规则强制离场!")
        else:
            print(f"    >> 继续持有观察")
    print(f"\n注意: 短线止损{p['buy_price']*0.96}，炸板/不板/超3天全部出")

def cmd_risk():
    print(f"""
{'='*50}
风控规则 (73万基准)
{'='*50}
  中线仓位: {MIDDLE_POS/10000:.0f}万 | 短线仓位: {SHORT_POS/10000:.0f}万 | 子弹: {BULLET/10000:.0f}万
  单票上限: {SHORT_POS*MAX_PER/10000:.0f}万 | 总仓上限: 70%
  止损: -4% (触发立即走，不犹豫)
  止盈: +8%减半 | +12%再减 | +15%全走
  持有期限: 短线1-3天(强制) | 中线趋势走坏出
  炸板: 先出一半
  连续2次止损: 当日禁止开新仓
  大盘冰点: 空仓观望
{'='*50}
""")

def cmd_hot():
    now = datetime.datetime.now().strftime("%H:%M")
    print(f"\n[{now}] 今日热点方向")
    blocks = [
        ("AI算力/科技", "涨幅大于5%;换手率大于8%;非ST"),
        ("军工/商业航天", "涨幅大于5%;换手率大于5%;非ST"),
        ("油气/能源", "涨幅大于3%;换手率大于5%;非ST"),
        ("新质生产力", "涨幅大于5%;换手率大于5%;非ST"),
    ]
    for label, sent in blocks:
        res = wencai(sent)
        stocks = res.get("stocks", [])[:3]
        total = res.get("totalCount", 0)
        print(f"\n{label} ({total}只强势):")
        for s in stocks:
            print(f"  {s.get('name')} {s.get('code')}")

def cmd_alloc():
    print(f"""
资金配置 (73万)
{'='*40}
  中线仓位: {MIDDLE_POS/10000:.0f}万 (41%) - 趋势股，持有1-3月
  短线仓位: {SHORT_POS/10000:.0f}万 (34%) - 强势股，1-3天
  备用子弹: {BULLET/10000:.0f}万 (25%) - 等机会，大跌/恐慌时用
  总可用:   {TOTAL_CASH/10000:.0f}万
  单票上限: {SHORT_POS*MAX_PER/10000:.0f}万 (短线单票)
{'='*40}
龙盛76手: 死钱，不动，靠其他账户赚钱
""")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "选股":    cmd_select()
    elif cmd == "中线":  cmd_middle()
    elif cmd == "短线":  cmd_short()
    elif cmd == "风控":  cmd_risk()
    elif cmd == "热点":  cmd_hot()
    elif cmd == "配仓":  cmd_alloc()
    else:                cmd_help()

if __name__ == "__main__":
    main()
