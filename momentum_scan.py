# -*- coding: utf-8 -*-
"""动量反转选股 - 尾盘策略"""
import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print(f"  动量反转选股  {datetime.now().strftime('%H:%M')}")
print("=" * 50)

# 获取今日涨幅前50
try:
    df = ak.stock_zt_pool_em(date=datetime.now().strftime('%Y%m%d'))
    print(f"\n涨停股数量: {len(df)}")
    # 找涨停股中有动量反转信号的
    if len(df) > 0:
        print("\n今日涨停强势股:")
        cols = df.columns.tolist()
        # 找关键列
        for _, row in df.head(20).iterrows():
            try:
                name = str(row.get('名称', row.get('code', '?')))
                code = str(row.get('code', row.get('代码', '?')))
                chg_pct = float(str(row.get('涨跌幅', row.get('change_rt', 0))).replace('%', ''))
                print(f"  {code} {name} {'+' if chg_pct > 0 else ''}{chg_pct:.2f}%")
            except:
                pass
except Exception as e:
    print(f"涨停池获取失败: {e}")

# 获取今日强势股（涨幅榜）
print("\n" + "=" * 50)
print("今日强势股（涨幅>3%，含动量）:")
try:
    df2 = ak.stock_marketMostLoseEm()
    if len(df2) > 0:
        for _, row in df2.head(10).iterrows():
            print(f"  {row.iloc[0]} {row.iloc[1]} +{row.iloc[3]}%")
except:
    pass

# 获取今日跌幅大的超卖股（可能有反弹机会）
print("\n" + "=" * 50)
print("今日强势超跌反弹候选:")
try:
    df3 = ak.stock_marketOverTurnEm(start_date=datetime.now().strftime('%Y%m%d'), end_date=datetime.now().strftime('%Y%m%d'))
    # 按换手率排序
    df3 = df3.sort_values('换手率', ascending=False)
    if len(df3) > 0:
        print(f"换手率最高的10只:")
        for _, row in df3.head(10).iterrows():
            try:
                code = str(row.get('代码', ''))
                name = str(row.get('名称', ''))
                chg = float(str(row.get('涨跌幅', '0')).replace('%', ''))
                turnover = float(str(row.get('换手率', '0')).replace('%', ''))
                print(f"  {code} {name} {'+' if chg > 0 else ''}{chg:.2f}% 换手{turnover:.2f}%")
            except:
                pass
except Exception as e:
    print(f"获取失败: {e}")

print("\n" + "=" * 50)
print("策略说明:")
print("  尾盘策略: 14:30后买强势股，次日开盘卖")
print("  动量反转: 超跌+缩量+缩脚 = 反弹概率高")
print("  止损: -5%止损，不补仓")
