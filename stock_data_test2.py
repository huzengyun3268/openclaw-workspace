# A股数据测试脚本 v2
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

print("=" * 50)
print("A股数据获取测试 v2")
print("=" * 50)

# 1. K线数据 - 成功
print("\n【1】个股K线数据 (特变电工 600089)")
try:
    df_kline = ak.stock_zh_a_hist(symbol="600089", period="daily", start_date="20260301", end_date="20260317")
    print(df_kline[['日期', '开盘', '收盘', '涨跌幅', '成交额']].tail())
except Exception as e:
    print(f"错误: {e}")

# 2. 个股信息
print("\n【2】个股实时行情 (浙江龙盛 600352)")
try:
    df = ak.stock_zh_a_hist(symbol="600352", period="daily", start_date="20260310", end_date="20260317")
    print(df[['日期', '开盘', '收盘', '涨跌幅']].tail())
except Exception as e:
    print(f"错误: {e}")

# 3. 指数行情
print("\n【3】上证指数行情")
try:
    df_idx = ak.stock_zh_index_daily(symbol="sh000001")
    print(df_idx.tail())
except Exception as e:
    print(f"错误: {e}")

# 4. 热门股票
print("\n【4】今日涨幅榜 (前10)")
try:
    # 使用新版API
    from akshare import stock_zh_a_spot_em
    df_spot = stock_zh_a_spot_em()
    df_top = df_spot.nlargest(10, '涨跌幅')[['代码', '名称', '最新价', '涨跌幅']]
    print(df_top.to_string(index=False))
except Exception as e:
    print(f"错误: {e}")

# 5. 板块行情
print("\n【5】行业板块资金流向")
try:
    from akshare import stock_fund_flow_industry
    df_fund = stock_fund_flow_industry(symbol="今日", n=10)
    print(df_fund)
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试完成!")
print("=" * 50)
