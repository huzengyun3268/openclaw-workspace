# -*- coding: utf-8 -*-
import urllib.request
import sys

stocks = [
    ('sh600352', '\u6d59\u6c5f\u9f99\u76db'),
    ('sz300033', '\u540c\u82b1\u987a'),
    ('sh600487', '\u4ea8\u901a\u5149\u7535'),
    ('sh600893', '\u822a\u53d1\u52a8\u529b'),
    ('sh601168', '\u897f\u90e8\u77ff\u4e1a'),
    ('sh518880', '\u9ec4\u91d1ETF'),
    ('sz430046', '\u5723\u535a\u6da6'),
    ('sh600114', '\u4e1c\u6155\u80a1\u4efd'),
    ('sh600089', '\u7279\u53d8\u7535\u5de5'),
]

print('\u7b2c\u4e00\u90e8\u5206\u76ee\u76d1\u63a7 2026-04-02 13:30')
print('')

for code, name in stocks:
    try:
        url = 'https://qt.gtimg.cn/q=' + code
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=5)
        raw = resp.read()
        try:
            data = raw.decode('gbk')
        except:
            data = raw.decode('utf-8', errors='replace')
        parts = data.split('~')
        if len(parts) > 4:
            price = parts[3]
            pct = parts[32] if len(parts) > 32 else '0'
            print(f'{name}({code}): \u73b0\u4ef7={price}  \u6da8\u8dcc%={pct}')
        else:
            print(f'{name}({code}): \u6570\u636e\u89e3\u6790\u5931\u8d25')
    except Exception as e:
        print(f'{name}({code}): \u83b7\u53d6\u5931\u8d25 - {e}')
