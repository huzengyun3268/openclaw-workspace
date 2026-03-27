# -*- coding: utf-8 -*-
import akshare as ak
import warnings
warnings.filterwarnings('ignore')

stocks = [
    ('\u6d59\u6c5f\u9f99\u76db', '600352'),
    ('\u822a\u53d1\u52a8\u529b', '600893'),
    ('\u540c\u82b1\u987a', '300033'),
    ('\u897f\u90e8\u77ff\u4e1a', '601168'),
    ('\u666e\u9002\u5bfc\u822a', '831330'),
    ('\u4ea8\u901a\u5149\u7535', '600487'),
    ('\u4e2d\u590d\u795e\u9e7f', '688295'),
    ('\u4ebf\u80fd\u7535\u529b', '920046'),
    ('\u5723\u535a\u6da6', '430046'),
    ('\u7279\u53d8\u7535\u529b', '600089'),
    ('\u4e1c\u58e4\u80a1\u4efd', '600114'),
    ('\u5357\u7f51\u6570\u5b57', '301638'),
]

print('=== \u96c6\u5408\u7ade\u4ef7\u76d1\u63a7 09:25 ===')
print(f'\u65f6\u95f4: 2026-03-27')
print()

results = []
for name, code in stocks:
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['\u4ee3\u7801'] == code]
        if not row.empty:
            price = row['\u6700\u65b0\u4ef7'].values[0]
            chg_pct = row['\u6da8\u6da6\u5e45\u5ea6'].values[0]
            amount = row['\u6210\u4ea4\u989d'].values[0]
            print(f'{name}({code}): \u73b0\u4ef7={price} \u6da8\u6da6\u5e45={chg_pct}% \u6210\u4ea4\u989d={amount/1e8:.2f}\u4ebf')
            results.append((name, code, price, chg_pct, amount))
        else:
            print(f'{name}({code}): \u672a\u627e\u5230')
    except Exception as e:
        print(f'{name}({code}): \u9519\u8bef-{e}')

print()
print('=== \u5173\u6ce8\u4e8b\u9879 ===')
# Stop loss checks
stop_loss = {
    '\u4ebf\u80fd\u7535\u529b': (28.20, 27.0),
    '\u6d59\u6c5f\u9f99\u76db': (13.18, 12.0),
    '\u822a\u53d1\u52a8\u529b': (47.96, 42.0),
    '\u540c\u82b1\u987a': (295.52, 280.0),
    '\u897f\u90e8\u77ff\u4e1a': (25.04, 22.0),
    '\u666e\u9002\u5bfc\u822a': (19.97, 18.0),
    '\u4ea8\u901a\u5149\u7535': (48.01, 38.0),
    '\u4e1c\u58e4\u80a1\u4efd': ('N/A', 25.0),
    '\u5357\u7f51\u6570\u5b57': (None, 28.0),
    '\u7279\u53d8\u7535\u529b': (None, 25.0),
}

for name, code, price, chg_pct, amount in results:
    if name in stop_loss:
        cur, sl = stop_loss[name]
        if cur != 'N/A' and cur is not None and cur <= sl:
            print(f'\u26a0\ufe0f {name}: \u73b0\u4ef7{cur}\u964d\u81f3\u6b62\u635f\u4f4d{sl}, \u9700\u51fa\u552e!')
        elif chg_pct <= -5:
            print(f'\u26a0\ufe0f {name}: \u5927\u5e45\u4e0b\u8dc3 {chg_pct}%, \u6ce8\u610f\u6b62\u635f\u4f4d')
