"""
龙虾盘前报告 v2.0
资金: 73万 | 中线30万+短线25万+子弹18万
"""
import requests, datetime

API = "https://stockboot.jiuma.cn/api"

def wencai(sentence):
    try:
        r = requests.post(f"{API}/dynamic-select/execute", json={"sentence": sentence}, timeout=30)
        return r.json()
    except:
        return {}

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
report = f"""
[龙虾盘前报告] {now}

【资金配置】
中线仓位: 30万 | 短线仓位: 25万 | 子弹: 18万
单票上限: 8万(短线) | 止损: -4% | 止盈: 8-12-15%

【今日主线方向】"""

blocks = [
    ("主线热点", "涨幅大于5%小于12%;换手率大于8%;流通市值小于300亿;非ST;非一字涨停;量比大于1.5"),
    ("回踩低吸", "涨幅大于1%小于5%;换手率大于5%;流通市值小于200亿;非ST;近5日跌幅大于3%"),
    ("超跌反弹", "跌幅大于5%;市盈率小于30;非ST;近5日跌幅大于8%"),
]

for label, sent in blocks:
    res = wencai(sent)
    stocks = res.get("stocks", [])[:3]
    total = res.get("totalCount", 0)
    report += f"\n{label} ({total}只):\n"
    for s in stocks:
        report += f"  - {s.get('name')} {s.get('code')}\n"

report += """
【操作计划】
中线(30万): 选1-2只主线趋势股，站稳均线买入
短线(25万): 选1-2只强势股，突破/回踩确认后买入
子弹(18万): 等大盘跌到位/恐慌时出手

【今日禁止】
- 大盘暴跌不开新仓
- 高位妖股不追
- 止损-4%触发出局不犹豫
- 连续2次止损当天禁止开新仓
"""
print(report)
