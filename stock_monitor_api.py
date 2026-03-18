# stock_monitor_api.py
# 股票实时行情监控 - 直接调用东方财富API
# 用法: python stock_monitor_api.py

import requests
import time
import json
from datetime import datetime

# 监控的股票列表
WATCH_LIST = [
    {'secid': '1.600089', 'name': '特变电工', 'cost': 24.765},
    {'secid': '1.600352', 'name': '浙江龙盛', 'cost': 15.912},
    {'secid': '1.603248', 'name': '锡华科技', 'cost': 35.490},
    {'secid': '0.300033', 'name': '同花顺', 'cost': 511.220},
    {'secid': '0.300189', 'name': '神农种业', 'cost': 17.099},
    {'secid': '1.920046', 'name': '亿能电力', 'cost': 35.936},
    {'secid': '0.831330', 'name': '普适导航', 'cost': 20.415},
    {'secid': '0.430046', 'name': '圣博润', 'cost': 0.478},
]

def get_stock_price(secid):
    """获取单只股票价格"""
    url = 'http://push2.eastmoney.com/api/qt/stock/get'
    params = {
        'secid': secid,
        'fields': 'f43,f44,f45,f46,f47,f48,f57,f58,f107,f169,f170',
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b'
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json().get('data', {})
        if data:
            price = data.get('f43', 0) / 100  # 最新价
            open_p = data.get('f44', 0) / 100  # 开盘价
            high = data.get('f45', 0) / 100  # 最高价
            low = data.get('f46', 0) / 100  # 最低价
            volume = data.get('f47', 0)  # 成交量
            amount = data.get('f48', 0) / 10000  # 成交额(万元)
            change = data.get('f169', 0) / 100  # 涨跌额
            change_pct = data.get('f170', 0) / 100  # 涨跌幅(%)
            code = data.get('f57', '')
            name = data.get('f58', '').encode('latin1').decode('gbk')
            return {
                'code': code, 'name': name, 'price': price,
                'open': open_p, 'high': high, 'low': low,
                'volume': volume, 'amount': amount,
                'change': change, 'change_pct': change_pct
            }
    except Exception as e:
        print(f"  获取失败: {e}")
    return None

def main():
    print("=" * 60)
    print("  股票实时行情监控")
    print("=" * 60)
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    results = []
    for stock in WATCH_LIST:
        secid = stock['secid']
        name = stock['name']
        cost = stock['cost']
        
        data = get_stock_price(secid)
        if data:
            data['cost'] = cost
            data['profit'] = (data['price'] - cost) * get_quantity(secid)
            data['profit_pct'] = (data['price'] - cost) / cost * 100
            results.append(data)
            
            profit_str = f"{data['profit']:+.0f}" if data['profit'] else "N/A"
            pct_str = f"{data['change_pct']:+.2f}%" if data['change_pct'] else "N/A"
            print(f"  {data['code']} {data['name']}")
            print(f"    现价: {data['price']:.2f}  涨跌: {pct_str}  涨跌额: {data['change']:+.2f}")
            print(f"    最高: {data['high']:.2f}  最低: {data['low']:.2f}  开盘: {data['open']:.2f}")
            print(f"    成本: {cost:.3f}  盈亏: {profit_str}({data['profit_pct']:+.1f}%)")
            print()
        else:
            print(f"  {secid} {name}: 获取失败")
            print()
    
    # 统计
    if results:
        total_profit = sum(r.get('profit', 0) for r in results)
        print("-" * 60)
        print(f"  合计盈亏: {total_profit:+.0f} 元")
        print("-" * 60)

def get_quantity(secid):
    """根据股数估算(简化版,实际应从持仓读取)"""
    quantities = {
        '1.600089': 52300,  # 特变电工
        '1.600352': 141700,  # 浙江龙盛
        '1.603248': 2000,    # 锡华科技
        '0.300033': 600,     # 同花顺
        '0.300189': 5000,    # 神农种业
        '1.920046': 12731,   # 亿能电力
        '0.831330': 6370,    # 普适导航
        '0.430046': 10334,   # 圣博润
    }
    return quantities.get(secid, 0)

if __name__ == "__main__":
    main()
