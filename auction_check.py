import urllib.request
import json
import sys

stocks = [
    ('Zhejiang Longsheng', '600352', 'sh'),
    ('Tonghuashun', '300033', 'sz'),
    ('Hendong Guangdian', '600487', 'sh'),
    ('Hangfa Dongli', '600893', 'sh'),
    ('Xibu Kuangye', '601168', 'sh'),
    ('Gold ETF', '518880', 'sh'),
    ('Dongmu Gufen', '600114', 'sh'),
    ('Teubian Diangong', '600089', 'sh'),
]

cnames = {
    '600352': '\u6d59\u6c5f\u9f99\u76db',
    '300033': '\u540c\u82b1\u987a',
    '600487': '\u4ea8\u901a\u5149\u7535',
    '600893': '\u822a\u53d1\u52a8\u529b',
    '601168': '\u897f\u90e8\u77ff\u4e1a',
    '518880': '\u9ec4\u91d1ETF',
    '600114': '\u4e1c\u5858\u80a1\u4efd',
    '600089': '\u7279\u53d8\u7535\u5de5',
}

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://finance.eastmoney.com'
}

sys.stdout.reconfigure(encoding='utf-8')

print("=== 2026-04-03 09:33 \u96c6\u5408\u7ade\u4ef7\u76d1\u63a7 ===")
print("-" * 65)

for name, code, mkt in stocks:
    try:
        if mkt == 'sh':
            secid = f'1.{code}'
        else:
            secid = f'0.{code}'
        url = f'https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f107,f169,f170'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read().decode())
        info = data.get('data', {})
        price = info.get('f43', 0)
        if price:
            price = price / 100.0
        change = info.get('f169')
        changePct = info.get('f170')
        if change is not None:
            change = change / 100.0
        if changePct is not None:
            changePct = changePct / 100.0
        vol = info.get('f47', 0)
        high = info.get('f44')
        low = info.get('f45')
        open_p = info.get('f46')
        if high:
            high = high / 100.0
        if low:
            low = low / 100.0
        if open_p:
            open_p = open_p / 100.0

        cname = cnames.get(code, name)
        prefix = f'{mkt}{code}'
        if changePct is not None:
            pct_str = f"{changePct:+.2f}%"
        else:
            pct_str = "N/A"
        if change is not None:
            chg_str = f"{change:+.3f}"
        else:
            chg_str = "N/A"

        if price > 0:
            print(f"{cname}({prefix}): \u73b0={price} \u6da8\u8dcc={chg_str}({pct_str}) \u5f00\u4e0a={open_p} \u9ad8={high} \u4f4e={low} \u6216\u4ea4={vol}")
        else:
            print(f"{cname}({prefix}): \u6682\u65e0\u6570\u636e")
    except Exception as e:
        print(f"{cnames.get(code, name)}: \u83b7\u53d6\u5931\u8d25 {e}")
