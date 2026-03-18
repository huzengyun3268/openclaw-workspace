# A股数据测试脚本
# 使用方法: python stock_data_test.py

import akshare as ak
import tushare as ts
import pandas as pd
import json
from datetime import datetime, timedelta

print("=" * 50)
print("A股数据获取测试")
print("=" * 50)

# ====== 1. 市场行情数据 (akshare) ======
print("\n【1】大盘指数实时行情")
try:
    df = ak.stock_zh_a_spot_em()
    print(f"获取到 {len(df)} 只股票")
    print("\n上证指数:", df[df['代码'] == '000001']['最新价'].values[0] if len(df[df['代码'] == '000001']) > 0 else "N/A")
    print("深证指数:", df[df['代码'] == '399001']['最新价'].values[0] if len(df[df['代码'] == '399001']) > 0 else "N/A")
except Exception as e:
    print(f"错误: {e}")

# ====== 2. 个股K线数据 ======
print("\n【2】个股K线数据 (特变电工 600089)")
try:
    df_kline = ak.stock_zh_a_hist(symbol="600089", period="daily", start_date="20260301", end_date="20260317")
    print(df_kline.tail())
except Exception as e:
    print(f"错误: {e}")

# ====== 3. 资金流向 ======
print("\n【3】资金流向 (前10)")
try:
    df_money = ak.stock_fund_flow_rank(stock_type="北证", market="all")
    print(df_money.head(10))
except Exception as e:
    print(f"错误: {e}")

# ====== 4. 行业资金流向 ======
print("\n【4】行业资金流向 (前10)")
try:
    df_industry = ak.stock_sector_fund_flow_rank(sector_type="行业资金流", sector_name="按今日涨跌幅")
    print(df_industry.head(10))
except Exception as e:
    print(f"错误: {e}")

# ====== 5. 股票信息查询 ======
print("\n【5】个股信息 (浙江龙盛 600352)")
try:
    # 实时行情
    df_rt = ak.stock_zh_a_spot_em()
    stock = df_rt[df_rt['代码'] == '600352']
    if len(stock) > 0:
        s = stock.iloc[0]
        print(f"最新价: {s['最新价']}")
        print(f"涨跌幅: {s['涨跌幅']}%")
        print(f"成交额: {s['成交额']}")
        print(f"换手率: {s['换手率']}")
        print(f"总市值: {s['总市值']}亿")
except Exception as e:
    print(f"错误: {e}")

# ====== 6. 龙虎榜 ======
print("\n【6】今日龙虎榜")
try:
    df_lhb = ak.stock_lhb_detail_st_em(start_date="20260317", end_date="20260317")
    print(f"上榜股票数: {len(df_lhb)}")
    if len(df_lhb) > 0:
        print(df_lhb[['股票代码', '股票名称', '上榜原因']].head(5))
except Exception as e:
    print(f"错误: {e}")

print("\n" + "=" * 50)
print("测试完成!")
print("=" * 50)
