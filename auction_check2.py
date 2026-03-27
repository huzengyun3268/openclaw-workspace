# -*- coding: utf-8 -*-
import requests
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

# Convert to secid format for eastmoney
secids = []
for name, code in stocks:
    if code.startswith('6'):
        secids.append(f'1.{code}')
    elif code.startswith('9'):
        secids.append(f'0.{code}')
    else:
        secids.append(f'0.{code}')

secid_str = ','.join(secids)

url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&secids={secid_str}&fields=f2,f3,f4,f5,f6,f7,f8,f12,f14&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=jQuery&_=1'

try:
    resp = requests.get(url, timeout=10)
    text = resp.text
    # Parse JSONP
    import json
    start = text.find('(')
    end = text.rfind(')')
    data = json.loads(text[start+1:end])
    
    print('=== \u96c6\u5408\u7ade\u4ef7\u76d1\u63a7 09:25 ===')
    print(f'\u65f6\u95f4: 2026-03-27')
    print()
    
    items = data.get('data', {}).get('diff', [])
    for item in items:
        code = item.get('f12', '')
        name = item.get('f14', '')
        price = item.get('f2', 0)
        chg_pct = item.get('f3', 0)
        amount = item.get('f6', 0)
        
        if price and price != '-' and price != 0:
            price_str = f'{price}'
            chg_str = f'{chg_pct}'
            amount_str = f'{amount/1e8:.2f}\u4ebf' if amount else 'N/A'
            print(f'{name}({code}): \u73b0\u4ef7={price_str} \u6da8\u6da6\u5e45={chg_str}% \u6210\u4ea4\u989d={amount_str}')
        else:
            print(f'{name}({code}): \u6682\u65e0\u6570\u636e')
    
    print()
    print('=== \u5173\u6ce8\u4e8b\u9879 ===')
    print('\u26a0\ufe0f \u4ebf\u80fd\u7535\u529b: \u6b63\u80fd\u529b\u5e02\uff0c\u4eca\u65e5\u5fc5\u987b\u6e05\u4ed3\uff01')
    
except Exception as e:
    print(f'\u9519\u8bef: {e}')
