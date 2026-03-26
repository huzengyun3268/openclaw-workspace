# -*- coding: utf-8 -*-
import urllib.request
import json

stocks = {
    '600352': '浙江龙盛',
    '300033': '同花顺',
    '831330': '普适导航',
    '000988': '华工科技',
    '688295': '中复神鹰',
    '600487': '亨通光电',
    '300499': '高澜股份',
    '601168': '西部矿业',
    '600893': '航发动力',
    '920046': '亿能电力',
    '430046': '圣博润',
    '600089': '特变电工',
    '600114': '东睦股份',
    '301638': '南网数字',
}

codes = list(stocks.keys())
url = 'http://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids=' + ','.join(codes)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
    items = data.get('data', {}).get('diff', [])
    for item in items:
        code = item.get('f12', '')
        name = stocks.get(code, code)
        price = item.get('f2', 0)
        chg = item.get('f3', 0)
        chg_pct = item.get('f4', 0)
        if price and price != '-':
            print(f"{name}({code}): {price} 涨跌:{chg}% 涨跌幅:{chg_pct}%")
        else:
            print(f"{name}({code}): 无数据")
except Exception as e:
    print(f'Error: {e}')
