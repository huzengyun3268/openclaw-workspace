# 智能选股脚本 - 简化版
import akshare as ak
import pandas as pd

print("=" * 50)
print("  智能选股 - T+1 策略")
print("=" * 50)

# 获取上证指数历史数据（测试连接）
print("\n测试网络连接...")
try:
    df_idx = ak.stock_zh_index_daily(symbol="sh000001")
    print("✓ 连接成功!")
except Exception as e:
    print(f"✗ 网络问题: {e}")
    print("改用网页数据...")
    
# 获取涨幅榜
print("\n获取今日数据...")
for attempt in range(3):
    try:
        df = ak.stock_zh_a_spot_em()
        print(f"✓ 成功获取 {len(df)} 只股票")
        break
    except Exception as e:
        print(f"  尝试 {attempt+1} 失败: {str(e)[:50]}")
        import time
        time.sleep(2)
else:
    print("获取失败，使用备用方法")
    # 备用：获取板块资金
    try:
        df = ak.stock_sector_fund_flow_rank(sector_type="行业资金流", sector_name="按今日涨跌幅")
        print(f"获取到 {len(df)} 个行业")
    except Exception as e:
        print(f"备用也失败: {e}")
        exit()

# 筛选
print("\n筛选条件:")
print("  - 涨幅: 1%~7%")
print("  - 换手率: >3%")
print("  - 量比: >1.5")

try:
    df_sel = df[
        (df['涨跌幅'] > 1) & 
        (df['涨跌幅'] < 7) & 
        (df['换手率'] > 3) & 
        (df['量比'] > 1.5)
    ].sort_values('涨跌幅', ascending=False)
    
    print(f"\n符合条件: {len(df_sel)} 只")
    
    print("\n" + "=" * 50)
    print("  ⭐ 推荐股票")
    print("=" * 50)
    
    count = 0
    for i, row in df_sel.head(10).iterrows():
        name = str(row.get('名称', ''))
        if 'ST' in name or '*ST' in name:
            continue
        code = row.get('代码', '')
        price = row.get('最新价', 0)
        change = row.get('涨跌幅', 0)
        turnover = row.get('换手率', 0)
        
        print(f"\n{count+1}. {name} ({code})")
        print(f"   价格: {price}元, 涨幅: {change}%, 换手: {turnover}%")
        
        if change < 3:
            print("   → 稳健型推荐")
        elif change < 5:
            print("   → 平衡型推荐")
        else:
            print("   → 激进型注意风险")
        
        count += 1
        if count >= 5:
            break
            
except Exception as e:
    print(f"筛选失败: {e}")

print("\n" + "=" * 50)
