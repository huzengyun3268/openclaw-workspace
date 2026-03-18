# stock_monitor_v2.py
# 股票实时行情监控 - 带重试和伪浏览器头
# 用法: python stock_monitor_v2.py

import requests
import time
import random
from datetime import datetime

# 监控的股票列表
WATCH_LIST = [
    {'secid': '1.600089', 'name': '特变电工', 'cost': 24.765, 'qty': 52300},
    {'secid': '1.600352', 'name': '浙江龙盛', 'cost': 15.912, 'qty': 141700},
    {'secid': '1.603248', 'name': '锡华科技', 'cost': 35.490, 'qty': 2000},
    {'secid': '0.300033', 'name': '同花顺', 'cost': 511.220, 'qty': 600},
    {'secid': '0.300189', 'name': '神农种业', 'cost': 17.099, 'qty': 5000},
    {'secid': '1.920046', 'name': '亿能电力', 'cost': 35.936, 'qty': 12731},
    {'secid': '0.831330', 'name': '普适导航', 'cost': 20.415, 'qty': 6370},
    {'secid': '0.430046', 'name': '圣博润', 'cost': 0.478, 'qty': 10334},
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'http://quote.eastmoney.com/',
    'Accept': 'text/javascript, application/javascript, */*; q=0.01',
}

def get_stock_price(secid, name):
    """获取单只股票价格，带重试"""
    url = 'http://push2.eastmoney.com/api/qt/stock/get'
    params = {
        'secid': secid,
        'fields': 'f43,f44,f45,f46,f47,f48,f57,f58,f169,f170',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        '_': int(time.time() * 1000)
    }
    
    for attempt in range(3):
        try:
            session = requests.Session()
            r = session.get(url, params=params, headers=HEADERS, timeout=8)
            session.close()
            
            if r.status_code == 200:
                data = r.json().get('data', {})
                if data:
                    price = data.get('f43', 0) / 100
                    open_p = data.get('f44', 0) / 100
                    high = data.get('f45', 0) / 100
                    low = data.get('f46', 0) / 100
                    volume = data.get('f47', 0)
                    amount = data.get('f48', 0) / 10000
                    change = data.get('f169', 0) / 100
                    change_pct = data.get('f170', 0) / 100
                    code = data.get('f57', '')
                    return {
                        'code': code, 'price': price,
                        'open': open_p, 'high': high, 'low': low,
                        'volume': volume, 'amount': amount,
                        'change': change, 'change_pct': change_pct
                    }
            time.sleep(1)
        except Exception as e:
            print(f"    重试 {attempt+1}: {e}")
            time.sleep(2)
    return None

def main():
    print("=" * 60)
    print("  股票实时行情监控 v2")
    print("=" * 60)
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    results = []
    for stock in WATCH_LIST:
        secid = stock['secid']
        name = stock['name']
        cost = stock['cost']
        qty = stock['qty']
        
        print(f"  正在获取 {name}...")
        data = get_stock_price(secid, name)
        
        if data:
            profit = (data['price'] - cost) * qty
            profit_pct = (data['price'] - cost) / cost * 100
            data['cost'] = cost
            data['qty'] = qty
            data['profit'] = profit
            data['profit_pct'] = profit_pct
            data['name'] = name
            results.append(data)
            
            print(f"    现价: {data['price']:.2f}  涨跌: {data['change_pct']:+.2f}%")
            print(f"    成本: {cost:.3f}  盈亏: {profit:+.0f}({profit_pct:+.1f}%)")
            print()
        else:
            print(f"    获取失败")
            print()
        
        time.sleep(0.5)  # 避免请求过快
    
    if results:
        total_profit = sum(r.get('profit', 0) for r in results)
        print("-" * 60)
        print(f"  合计盈亏: {total_profit:+.0f} 元")
        print("-" * 60)

if __name__ == "__main__":
    main()
