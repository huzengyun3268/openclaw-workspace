# -*- coding: utf-8 -*-
import urllib.request, json, sys

codes_to_check = {
    'sz002471': '+35',
    'sh688011': '+35',
    'sz002491': '+25',
    'sz300016': '-5',
    'sz002176': '-20',
    'sh600216': '-5',
    'sz002372': '-35',
    'sz300779': '-35',
    'sh605168': '-45',
    'sh600033': '-35',
}

# 用东方财富获取名称
base_url = "https://push2.eastmoney.com/api/qt/stock/get?fields=f14,f3&secid=0.{code}"
name_map = {}
for code in codes_to_check:
    stk = code[2:]
    mkt = '1' if code.startswith('sh') else '0'
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={mkt}.{stk}&fields=f14,f3&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            name = data.get('data', {}).get('f14', 'N/A')
            change = data.get('data', {}).get('f3', 0)
            name_map[code] = (name, change)
            print(f"{code} {name} 涨幅{change}% 评分{codes_to_check[code]}")
    except Exception as e:
        print(f"{code} 获取失败: {e}")
