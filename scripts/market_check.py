# -*- coding: utf-8 -*-
import akshare as ak
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 大盘指数
try:
    idx = ak.stock_zh_index_spot_em()
    main_idx = idx[idx['代码'].isin(['000001','399001','399006','000300','000688'])]
    for _, row in main_idx.iterrows():
        name = row['名称']
        price = row['最新价']
        pct = row['涨跌幅']
        print(f"{name}: {price} {pct:+.2%}")
except Exception as e:
    print('idx error:', e)

# 行业板块涨跌
try:
    ind = ak.stock_board_industry_name_em()
    top = ind.sort_values('涨跌幅', ascending=False)
    print('\n涨幅前5:')
    for _, r in top.head(5).iterrows():
        print(f"{r['板块名称']}: {r['涨跌幅']:+.2%}")
    print('跌幅前5:')
    for _, r in top.tail(5).iterrows():
        print(f"{r['板块名称']}: {r['涨跌幅']:+.2%}")
except Exception as e:
    print('ind error:', e)

# 概念板块
try:
    concept = ak.stock_board_concept_name_em()
    top_concept = concept.sort_values('涨跌幅', ascending=False)
    print('\n概念涨幅前5:')
    for _, r in top_concept.head(5).iterrows():
        print(f"{r['板块名称']}: {r['涨跌幅']:+.2%}")
    print('概念跌幅前5:')
    for _, r in top_concept.tail(5).iterrows():
        print(f"{r['板块名称']}: {r['涨跌幅']:+.2%}")
except Exception as e:
    print('concept error:', e)
