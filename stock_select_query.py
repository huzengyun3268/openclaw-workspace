# -*- coding: utf-8 -*-
import urllib.request
import json

def select_stocks(condition):
    url = "https://stockboot.jiuma.cn/api/dynamic-select/execute"
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0'
    }
    data = json.dumps({"sentence": condition}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    return result

# 尾盘强势股筛选：涨幅3-10%，非一字涨停，非ST
print("=" * 50)
print("【尾盘强势股筛选】涨幅3-10%，非一字涨停，非ST")
print("=" * 50)

result = select_stocks("涨幅大于3%小于10%;非ST;非一字涨停非北交所")

if result.get('code') == 200:
    stocks = result['data']['stocks']
    total = result['data']['totalCount']
    print(f"\n符合条件的股票: {total} 只\n")
    for s in stocks[:15]:
        code = s['code']
        market = 'sh' if s['marketType'] == 'SH' else 'sz' if s['marketType'] == 'SZ' else 'bj'
        name_raw = s.get('name', 'N/A')
        change = round(s.get('changeRate', 0), 2)
        tag = s.get('extraFields', {})
        tag_str = list(tag.values())[0] if tag else ''
        print(f"  {code}  {name_raw}  涨幅+{change}%  {tag_str}")
else:
    print(f"查询失败: {result}")
