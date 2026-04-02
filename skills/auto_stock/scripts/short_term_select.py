"""
龙虾激进短线选股脚本 v1.0
资金: 80万基准 | 单票上限: 24万(30%) | 止损: -4% | 止盈: 8-15%
策略: 主线强势 + 突破 + 缩量回踩
用法: python short_term_select.py [模式]
模式: 强势/突破/尾盘/热点
"""

import requests
import json
import sys
import datetime

API = "https://stockboot.jiuma.cn/api"

def wencai(sentence):
    url = f"{API}/dynamic-select/execute"
    try:
        r = requests.post(url, json={"sentence": sentence}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def calc_position(price):
    """计算仓位: 80万基准，单票上限30%=24万，止损4%"""
    capital = 800000
    max_per = capital * 0.30
    shares = int(max_per / price / 100) * 100  # 取整百
    cost = shares * price
    stop_loss = cost * 0.04
    return shares, cost, stop_loss

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "强势"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    strategies = {
        "强势": "涨幅大于5%小于10%;换手率大于5%;流通市值小于300亿;非ST;非新股",
        "突破": "涨幅大于3%小于8%;换手率大于8%;流通市值小于200亿;突破20日新高;非ST",
        "尾盘": "涨幅大于3%小于6%;换手率大于5%;流通市值小于150亿;非ST;量比大于1.5",
        "热点": "涨幅大于5%小于15%;换手率大于10%;非ST;非一字涨停",
        "回踩": "涨幅大于2%小于6%;换手率大于3%;流通市值小于200亿;非ST;近5日跌幅大于3%",
    }

    sentence = strategies.get(mode, strategies["强势"])

    print(f"\n{'='*55}")
    print(f"[{now}] 龙虾激进短线选股 | 模式: {mode}")
    print(f"资金基准: 80万 | 单票上限: 24万(30%) | 止损: -4%")
    print('='*55)
    print(f"\n条件: {sentence}")

    results = wencai(sentence)

    if "error" in results:
        print(f"查询失败: {results['error']}")
        return

    stocks = results.get("stocks", [])
    total = results.get("totalCount", 0)
    cost_ms = results.get("costTime", 0)
    print(f"筛出 {total} 只 (耗时 {cost_ms}ms)")
    print()

    if not stocks:
        print("无符合条件股票")
        return

    print(f"{'='*55}")
    print(f"{'简称':<8} {'代码':<10} {'建议仓位':>10} {'止损额':>8} {'备注'}")
    print(f"{'-'*55}")

    for i, s in enumerate(stocks[:12], 1):
        name = s.get("name", "?")
        code = s.get("code", "?")
        # 粗估价格（用市值/股本估算，实际应以实时价格为准）
        print(f"{i:2d}. {name:<8} {code:<10} {'请输入现价':>10}  {'--':>8}")

    print()
    print("请告诉我选中股票的现价，我帮你算出具体买多少股、止损多少。")
    print()

if __name__ == "__main__":
    main()
