# -*- coding: utf-8 -*-
import requests
import json
import sys

# 用东方财富实时接口
codes = ['600352', '300033', '000988', '688295', '600487', '300499', '601168', '600893', '920046']

def get_stock_data(code):
    # 判断市场前缀
    if code.startswith('6') or code.startswith('9'):
        market = 'sh'
    elif code.startswith('0') or code.startswith('3'):
        market = 'sz'
    else:
        market = 'bj'
    
    url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://quote.eastmoney.com/'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        data = r.json()
        if data and data.get('data'):
            d = data['data']
            name = d.get('f58', code)
            price = d.get('f43', '-')  # 最新价
            open_p = d.get('f60', '-')  # 今开
            high = d.get('f44', '-')   # 最高
            low = d.get('f45', '-')    # 最低
            vol = d.get('f47', '-')    # 成交量(手)
            change = d.get('f169', '-')  # 涨跌额
            pct = d.get('f170', '-')   # 涨跌幅
            # 转换价格单位：价格*100
            if price != '-':
                price = float(price) / 100
            if open_p != '-':
                open_p = float(open_p) / 100
            if high != '-':
                high = float(high) / 100
            if low != '-':
                low = float(low) / 100
            if pct != '-':
                pct = round(float(pct) / 100, 2)
            if change != '-':
                change = round(float(change) / 100, 2)
            return f"{code} {name}: 现价={price} 今开={open_p} 涨跌幅={pct}% 最高={high} 最低={low}"
    except Exception as e:
        return f"{code}: 获取失败 {e}"

for code in codes:
    print(get_stock_data(code))
