# -*- coding: utf-8 -*-
import urllib.request, sys

stocks = [
    ('浙江龙盛', 'sh600352'),
    ('航发动力', 'sh600893'),
    ('同花顺', 'sz300033'),
    ('西部矿业', 'sh601168'),
    ('普适导航', 'sh831330'),
    ('亨通光电', 'sh600487'),
    ('中复神鹰', 'sh688295'),
    ('圣博润', 'sz430046'),
    ('东睦股份', 'sh600114'),
    ('特变电工', 'sh600089'),
]

for name, code in stocks:
    try:
        url = 'https://qt.gtimg.cn/q=' + code
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            raw = r.read()
        data = raw.decode('gbk', errors='replace')
        fields = data.split('~')
        if len(fields) > 4:
            price = float(fields[3])
            pct = float(fields[32]) if len(fields) > 32 else 0
            print(f'{name}|{code}|{price}|{pct}')
        else:
            print(f'{name}|PARSE_ERROR|{data[:100]}')
    except Exception as e:
        print(f'{name}|ERROR|{e}')
