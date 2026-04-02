"""
龙虾全自动选股脚本 v1.0
基于 stock-select API 自然语言问财选股
用法: python auto_stock_select.py [策略名称]
"""

import requests
import json
import sys
import datetime

API = "https://stockboot.jiuma.cn/api"

def wencai(sentence):
    """调用问财接口"""
    url = f"{API}/dynamic-select/execute"
    payload = {"sentence": sentence}
    try:
        r = requests.post(url, json=payload, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    strategy = sys.argv[1] if len(sys.argv) > 1 else "default"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'='*50}")
    print(f"[{now}] 龙虾选股 - 策略: {strategy}")
    print('='*50)

    if strategy == "强势":
        # 主线强势股
        results = wencai("涨幅大于3%小于6%;换手率大于5%;流通市值小于500亿;非ST;非新股")
        desc = "主线强势股（3-6%涨幅，量价配合）"
    elif strategy == "高股息":
        # 高股息防御
        results = wencai("股息率大于3.5%;市盈率小于25;非ST")
        desc = "高股息防御股（震荡市）"
    elif strategy == "尾盘":
        # 尾盘强势（今日条件）
        results = wencai("涨幅大于2%小于5%;换手率大于5%;流通市值小于200亿;非ST;非一字涨停")
        desc = "尾盘强势股（2-5%涨幅）"
    elif strategy == "短线":
        # 短线金叉
        results = wencai("涨幅大于5%小于10%;换手率大于8%;流通市值小于300亿;非ST")
        desc = "短线强势（5-10%涨幅）"
    elif strategy == "超跌":
        # 超跌反弹
        results = wencai("跌幅大于5%;市盈率小于30;非ST;非退市")
        desc = "超跌反弹候选"
    else:
        # 默认综合
        results = wencai("涨幅大于3%小于6%;换手率大于5%;流通市值小于500亿;非ST;非新股")
        desc = "综合强势股"

    print(f"\n策略: {desc}")
    if "error" in results:
        print(f"查询失败: {results['error']}")
        return

    stocks = results.get("stocks", [])
    total = results.get("totalCount", 0)
    cost = results.get("costTime", 0)
    print(f"共筛出 {total} 只（耗时 {cost}ms）")
    print()

    if stocks:
        for i, s in enumerate(stocks[:15], 1):
            print(f"{i:2d}. {s.get('name','?')} ({s.get('code','?')}) - {s.get('marketType','?')}")
    else:
        print("无符合条件股票")

    print()

if __name__ == "__main__":
    main()
