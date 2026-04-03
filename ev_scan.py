# -*- coding: utf-8 -*-
"""尾盘选股 - 分析涨停股明日机会"""
import akshare as ak
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

today = datetime.now().strftime('%Y%m%d')
print(f"尾盘选股分析  {datetime.now().strftime('%H:%M')}\n")

# 今日涨停池
try:
    zt = ak.stock_zt_pool_em(date=today)
    print(f"今日涨停: {len(zt)}只\n")

    # 换手率、量比、流通市值
    cols = zt.columns.tolist()
    results = []
    for _, row in zt.iterrows():
        try:
            name = str(row.get('名称', ''))
            code = str(row.get('code', ''))
            chg_pct = float(str(row.get('涨跌幅', 0)).replace('%', ''))
            turnover = float(str(row.get('换手率', 0)).replace('%', ''))
            # 流值估算（亿）
            close_p = float(str(row.get('最新价', 0)).replace('%', ''))
            vol = float(str(row.get('成交量', 0)))
            # 简单估算流通市值
            mkt_cap_est = close_p * vol / 100000000 if vol > 0 else 0

            # 筛选条件：换手率5-25%（不能太高也不能太低），涨幅10%
            if 5 <= turnover <= 25:
                score = 50 + turnover - abs(10 - chg_pct) * 10
                results.append((code, name, chg_pct, turnover, score))
        except:
            pass

    results.sort(key=lambda x: x[4], reverse=True)
    print("=" * 60)
    print(f"{'代码':<8} {'名称':<8} {'涨幅':>6} {'换手率':>6} {'评分'}")
    print("=" * 60)
    for code, name, chg, turnover, score in results[:15]:
        print(f"{code:<8} {name:<8} {chg:>+6.2f} {turnover:>6.2f}% {score:.0f}")

    print("\n" + "=" * 60)
    print("TOP 5 明日关注（换手适中 + 尾盘封板稳）:")
    for i, (code, name, chg, turnover, score) in enumerate(results[:5], 1):
        print(f"  {i}. {code} {name} 换手{turnover:.1f}%")

    # 明日开盘策略
    print("\n" + "=" * 60)
    print("尾盘策略（明天开盘用）:")
    print("  规则: 明天9:30-10:00 观察今日涨停股开盘竞价")
    print("  买: 高开2-6%且不一字板，可轻仓介入")
    print("  卖: 盘中冲高即出，不贪")
    print("  止损: -3%")

except Exception as e:
    print(f"获取失败: {e}")
    import traceback; traceback.print_exc()
