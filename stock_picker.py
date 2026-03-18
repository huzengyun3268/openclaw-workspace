# 智能选股脚本 - T+1策略
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

print("=" * 60)
print("  智能选股 - T+1 低风险策略")
print("=" * 60)

# 1. 获取今日涨跌幅排行
print("\n【1】获取今日A股数据...")
try:
    df = ak.stock_zh_a_spot_em()
    print(f"共获取 {len(df)} 只股票")
except Exception as e:
    print(f"获取失败: {e}")
    exit()

# 2. 筛选条件
print("\n【2】智能筛选条件:")
print("  - 涨幅: 1%~8% (太高的不追)")
print("  - 换手率: >3% (有资金关注)")
print("  - 量比: >1.5 (量价配合)")
print("  - 成交额: >3亿 (流动性好)")

# 筛选
df_filtered = df[
    (df['涨跌幅'] > 1) & 
    (df['涨跌幅'] < 8) & 
    (df['换手率'] > 3) & 
    (df['量比'] > 1.5) &
    (df['成交额'] > 300000000)  # 3亿
].copy()

# 按涨幅排序
df_filtered = df_filtered.sort_values('涨跌幅', ascending=False)

print(f"\n【3】符合条件的股票: {len(df_filtered)} 只")

# 3. 获取资金流向
print("\n【4】获取资金流向...")
try:
    money_df = ak.stock_fund_flow_rank(stock_type="all", market="all")
    money_dict = dict(zip(money_df['代码'], money_df['名称']))
except:
    money_dict = {}

# 4. 输出推荐
print("\n" + "=" * 60)
print("  ⭐ 今日T+1推荐股票 (按涨幅排序)")
print("=" * 60)

if len(df_filtered) > 0:
    for i, row in df_filtered.head(15).iterrows():
        code = row['代码']
        name = row['名称']
        price = row['最新价']
        change = row['涨跌幅']
        turnover = row['换手率']
        amount = row['成交额']
        
        # 过滤ST股票
        if 'ST' in name or '*ST' in name:
            continue
            
        print(f"\n📈 {name} ({code})")
        print(f"   现价: {price:.2f}元")
        print(f"   涨幅: {change:.2f}%")
        print(f"   换手: {turnover:.2f}%")
        print(f"   成交: {amount/1e8:.1f}亿")
        
        # 判断理由
        if change < 3:
            reason = "  → 稳健型，还有上涨空间"
        elif change < 5:
            reason = "  → 平衡型，量价配合好"
        else:
            reason = "  → 激进型，谨慎追高"
        print(reason)
else:
    print("没有符合条件的股票")

# 5. 特别关注 - 资金流入
print("\n" + "=" * 60)
print("  💰 资金流入前五")
print("=" * 60)
try:
    top_money = money_df.head(5)
    for i, row in top_money.iterrows():
        print(f"  {row['名称']} ({row['代码']}): {row['涨跌幅']:.2f}%")
except:
    print("  数据获取失败")

print("\n" + "=" * 60)
print("  选股完成!")
print("=" * 60)
