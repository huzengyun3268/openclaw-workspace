# -*- coding: utf-8 -*-
import requests
import time

# 东方财富实时行情API
def get_stock_price(code):
    # 判断市场前缀
    if code.startswith('6'):
        symbol = f'sh{code}'
    elif code.startswith('0') or code.startswith('3'):
        symbol = f'sz{code}'
    else:
        symbol = f'bj{code}'
    
    url = f'http://push2.eastmoney.com/api/qt/stock/get?secid=1.{code if not code.startswith("6") else code}&fields=f43,f170,f171,f47,f48,f57,f58,f107,f50,f44,f45,f46,f51,f52&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2'
    # 用更简单的接口
    api_url = f'http://push2.eastmoney.com/api/qt/stock/get?secid=1.{code if code.startswith("6") else code}&fields=f43,f57,f58,f107,f50,f44,f45,f46&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2'
    
    # 尝试不同格式
    if code.startswith('6'):
        secid = f'1.{code}'
    elif code.startswith('0') or code.startswith('3'):
        secid = f'0.{code}'
    elif code.startswith('8') or code.startswith('4'):
        secid = f'0.{code}'
    else:
        secid = f'1.{code}'
    
    url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f57,f58,f107,f170,f171,f47,f48,f50,f44,f45,f46&ut=fa5fd1943c7b386f172d6893dbfba10b&fltt=2&invt=2'
    
    try:
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get('data'):
            d = data['data']
            return {
                'code': code,
                'name': d.get('f58', ''),
                'price': d.get('f43', 0) / 100 if d.get('f43') else 0,
                'chg': d.get('f170', 0) / 100 if d.get('f170') else 0,
                'pct': d.get('f171', 0) / 100 if d.get('f171') else 0,
                'high': d.get('f44', 0) / 100 if d.get('f44') else 0,
                'low': d.get('f45', 0) / 100 if d.get('f45') else 0,
                'open': d.get('f46', 0) / 100 if d.get('f46') else 0,
                'vol': d.get('f47', 0),
                'amount': d.get('f48', 0),
            }
    except Exception as e:
        pass
    return None

# 主账户持仓
holdings_main = [
    ('600352', '浙江龙盛', 15.952, 106700),
    ('300033', '同花顺', 423.488, 1200),
    ('831330', '普适导航', 20.361, 7370),
    ('000988', '华工科技', 116.87, 1000),
    ('688295', '中复神鹰', 37.843, 1500),
    ('600487', '亨通光电', 42.391, 2000),
    ('300499', '高澜股份', 41.625, 1500),
    ('601168', '西部矿业', 24.863, 2000),
    ('600893', '航发动力', 47.196, 1000),
    ('920046', '亿能电力', 329.555, 200),
    ('430046', '圣博润', 0.478, 10334),
]

# 两融账户
holdings_margin = [
    ('600089', '特变电工', 24.765, 52300),
]

# 老婆账户
holdings_wife = [
    ('600114', '东睦股份', 32.428, 200),
    ('600114', '东睦股份(2)', 25.9, 4600),
    ('301638', '南网数字', 32.635, 1700),
]

all_codes = list(set([h[0] for h in holdings_main + holdings_margin + holdings_wife]))

print('Fetching stock prices...')
for code in all_codes:
    result = get_stock_price(code)
    if result:
        print(f"{result['code']}|{result['name']}|{result['price']}|{result['pct']}|{result['high']}|{result['low']}|{result['amount']}")
    else:
        print(f"{code}|ERROR")
    time.sleep(0.3)
