# -*- coding: utf-8 -*-
import requests
import json
import time

stocks_main = {
    '600352': {'name': 'ZheJiangLongSheng', 'hold': 106700, 'cost': 15.952, 'stop': 12.0},
    '300033': {'name': 'TongHuaShun', 'hold': 1200, 'cost': 423.488, 'stop': 280},
    '831330': {'name': 'PuShiDaoHang', 'hold': 7370, 'cost': 20.361, 'stop': 0},
    '000988': {'name': 'HuaGongKeJi', 'hold': 1000, 'cost': 116.87, 'stop': 0},
    '688295': {'name': 'ZhongFuShenYing', 'hold': 1500, 'cost': 37.843, 'stop': 0},
    '600487': {'name': 'HengTongGuangDian', 'hold': 2000, 'cost': 42.391, 'stop': 0},
    '300499': {'name': 'GaoLanGuFen', 'hold': 1500, 'cost': 41.625, 'stop': 38.0},
    '601168': {'name': 'XiBuKuangYe', 'hold': 2000, 'cost': 24.863, 'stop': 0},
    '600893': {'name': 'HangFaDongLi', 'hold': 1000, 'cost': 47.196, 'stop': 0},
    '920046': {'name': 'YiNengDianLi', 'hold': 200, 'cost': 329.555, 'stop': 27},
    '430046': {'name': 'ShengBoRun', 'hold': 10334, 'cost': 0.478, 'stop': 0},
}

stocks_margin = {
    '600089': {'name': 'TeBianDianGong', 'hold': 52300, 'cost': 24.765, 'stop': 25.0},
}

stocks_wife = {
    '600114': {'name': 'DongMuGuFen', 'hold': 4800, 'cost': 26.2, 'stop': 25.0},
    '301638': {'name': 'NanWangShuZi', 'hold': 1700, 'cost': 32.635, 'stop': 28.0},
}

all_codes = list(stocks_main.keys()) + list(stocks_margin.keys()) + list(stocks_wife.keys())

# Use eastmoney API directly
codes_str = ','.join([f'"{c}"' for c in all_codes])

for attempt in range(3):
    try:
        url = 'https://push2.eastmoney.com/api/qt/ulist.np/get'
        params = {
            'fltt': 2,
            'invt': 2,
            'fields': 'f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18',
            'secids': ','.join([f'1.{c}' if not c.startswith('4') and not c.startswith('8') and not c.startswith('9') else f'0.{c}' for c in all_codes])
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://quote.eastmoney.com/'
        }
        
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('data') and data['data'].get('diff'):
            items = data['data']['diff']
            for item in items:
                code = item.get('f12', '')
                name = item.get('f14', '')
                price = item.get('f2', 0) / 100 if item.get('f2') else 0
                change_pct = item.get('f3', 0) / 100 if item.get('f3') else 0
                high = item.get('f15', 0) / 100 if item.get('f15') else 0
                low = item.get('f16', 0) / 100 if item.get('f16') else 0
                vol = item.get('f5', 0)
                amount = item.get('f6', 0)
                
                # Get cost and stop from our data
                info = stocks_main.get(code) or stocks_margin.get(code) or stocks_wife.get(code)
                cost = info['cost'] if info else 0
                stop = info['stop'] if info else 0
                hold = info['hold'] if info else 0
                
                profit = (price - cost) * hold if price and cost else 0
                stop_warning = ' **STOP**' if stop and price <= stop else ''
                
                print(f'{code} {name}: price={price:.3f} change={change_pct:+.2f}% high={high:.3f} low={low:.3f} cost={cost:.3f} stop={stop} profit={profit:+.0f}{stop_warning}')
        else:
            print(f'No data returned: {data}')
        break
    except Exception as e:
        print(f'Attempt {attempt+1} failed: {e}')
        if attempt < 2:
            time.sleep(3)
