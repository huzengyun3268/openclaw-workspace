# A股数据测试脚本 v3 - 简化版
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

print("=" * 50)
print("A股数据获取测试 v3")
print("=" * 50)

# 1. 上证指数历史数据 - 成功
print("\n【1】上证指数历史K线")
try:
    df_idx = ak.stock_zh_index_daily(symbol="sh000001")
    print(df_idx.tail(5))
except Exception as e:
    print(f"错误: {e}")

# 2. 深证成指
print("\n【2】深证成指历史K线")
try:
    df_sz = ak.stock_zh_index_daily(symbol="sz399001")
    print(df_sz.tail(5))
except Exception as e:
    print(f"错误: {e}")

# 3. 个股K线 - 重试
print("\n【3】特变电工(600089)历史K线")
for i in range(3):
    try:
        df = ak.stock_zh_a_hist(symbol="600089", period="daily", start_date="20260301", end_date="20260317")
        print(df[['日期', '开盘', '收盘', '涨跌幅', '成交额']].tail())
        break
    except Exception as e:
        print(f"重试 {i+1}/3 失败: {str(e)[:50]}")
        import time
        time.sleep(2)

# 4. 期货数据
print("\n【4】股指期货行情")
try:
    df_future = ak.futures_zh_index_spot_em(symbol="IF")
    print(df_future)
except Exception as e:
    print(f"错误: {e}")

# 5. 可转债
print("\n【5】可转债行情")
try:
    df_bond = ak.bond_zh_hs_cov()
    print(df_bond.head(5))
except Exception as e:
    print(f"错误: {e}")

# 6. 新股申购
print("\n【6】今日新股申购")
try:
    df_new = ak.stock_new_shares()
    print(df_new)
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试完成!")
print("=" * 50)
