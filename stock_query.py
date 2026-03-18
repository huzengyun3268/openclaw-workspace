# 股票数据查询工具
# 使用: python stock_query.py

import akshare as ak
import sys
import time

def get_stock_info(code):
    """获取个股基本信息"""
    try:
        df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20260301", end_date="20260317")
        if len(df) > 0:
            latest = df.iloc[-1]
            return {
                '代码': code,
                '最新价': latest['收盘'],
                '涨跌幅': f"{latest['涨跌幅']:.2f}%",
                '最高': latest['最高'],
                '最低': latest['最低'],
                '成交额': f"{latest['成交额']/1e8:.2f}亿"
            }
    except Exception as e:
        return {'错误': str(e)}
    return {'信息': '未找到数据'}

def get_index_info(code):
    """获取指数信息"""
    try:
        df = ak.stock_zh_index_daily(symbol=code)
        if len(df) > 0:
            latest = df.iloc[-1]
            return {
                '代码': code,
                '最新价': f"{latest['close']:.2f}",
                '最高': f"{latest['high']:.2f}",
                '最低': f"{latest['low']:.2f}",
                '成交量': f"{latest['volume']/1e8:.2f}亿"
            }
    except Exception as e:
        return {'错误': str(e)}
    return {}

# 主程序
if __name__ == "__main__":
    print("=" * 40)
    print("  股票数据查询工具")
    print("=" * 40)
    
    # 测试几个常用股票
    stocks = {
        '600089': '特变电工',
        '600352': '浙江龙盛',
        '000001': '上证指数',
        '399001': '深证成指'
    }
    
    print("\n【指数行情】")
    for code, name in [('sh000001', '上证指数'), ('sz399001', '深证成指')]:
        info = get_index_info(code)
        print(f"{name}: {info.get('最新价', 'N/A')}")
    
    print("\n【个股行情】")
    for code, name in [('600089', '特变电工'), ('600352', '浙江龙盛')]:
        info = get_stock_info(code)
        if '最新价' in info:
            print(f"{name}({code}): {info['最新价']} ({info['涨跌幅']})")
        else:
            print(f"{name}({code}): 获取失败")
    
    print("\n" + "=" * 40)
