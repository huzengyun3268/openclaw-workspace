"""
龙虾盘前报告 v1.0
每天9:25自动推送今日热点方向+重点关注
"""
import requests, datetime, json

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

【今日大盘环境预判】
(请根据昨夜美股+消息面自行补充)

【今日主线方向】
"""
blocks = [
    ("AI算力/科技", "涨幅大于5%;换手率大于8%;流通市值小于300亿;非ST"),
    ("军工/商业航天", "涨幅大于5%;换手率大于5%;非ST"),
    ("新质生产力", "涨幅大于5%;换手率大于5%;非ST"),
    ("高股息防御(稳健)", "股息率大于3%;市盈率小于20;非ST"),
]
for label, sent in blocks:
    res = wencai(sent)
    stocks = res.get("stocks", [])[:3]
    total = res.get("totalCount", 0)
    report += f"\n{label} ({total}只强势):\n"
    for s in stocks:
        name = s.get("name", "?")
        code = s.get("code", "?")
        report += f"  - {name} {code}\n"

report += """
【操作建议】
激进仓位: 30%单票，70%总仓
止损: -4%，触发出局不犹豫
止盈: 8%减半，12%再减，15%全走
持有超3天不赚，规则强制离场

【今日禁止】
- 大盘暴跌日不开新仓
- 高位妖股不追
- 利空/ST/问题股不碰
"""
print(report)
