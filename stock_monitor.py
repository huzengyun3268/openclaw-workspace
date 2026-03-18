# stock_monitor.py
# 股票实时行情监控脚本
# 用法: python stock_monitor.py

import akshare as ak
import time
import json

# 监控的股票列表
WATCH_LIST = {
    '600089': '特变电工',
    '600352': '浙江龙盛', 
    '603248': '锡华科技',
    '300033': '同花顺',
    '300189': '神农种业',
    '920046': '亿能电力',
    '831330': '普适导航',
    '430046': '圣博润'
}

def get_stock_prices():
    """获取股票实时行情"""
    try:
        print("正在获取行情数据...")
        df = ak.stock_zh_a_spot_em()
        
        results = []
        for code, name in WATCH_LIST.items():
            try:
                # 精确匹配
                row = df[df['代码'] == code]
                if not row.empty:
                    price = float(row['最新价'].values[0])
                    change = float(row['涨跌幅'].values[0])
                    volume = row['成交量'].values[0]
                    amount = row['成交额'].values[0]
                    results.append({
                        'code': code,
                        'name': name,
                        'price': price,
                        'change_pct': change,
                        'volume': volume,
                        'amount': amount
                    })
                    print(f"  {code} {name}: {price} ({change:+.2f}%)")
                else:
                    print(f"  {code} {name}: 未找到")
            except Exception as e:
                print(f"  {code} {name}: 获取失败 - {e}")
        
        return results
    except Exception as e:
        print(f"获取数据失败: {e}")
        return []

if __name__ == "__main__":
    print("=" * 50)
    print("股票实时行情监控")
    print("=" * 50)
    print()
    
    results = get_stock_prices()
    
    if results:
        print()
        print("=" * 50)
        print(f"共监控 {len(results)} 只股票")
        print("=" * 50)
    else:
        print("未能获取到数据")
