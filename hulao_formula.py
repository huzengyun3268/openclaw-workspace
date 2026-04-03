# -*- coding: utf-8 -*-
"""老胡选股公式 - 全部强势股扫描"""
import akshare as ak
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_market(code):
    c = str(code)
    return 'sh' if c.startswith(('6', '9')) else 'sz'

def check_stock(code, name, chg, vr, tr, mc_yi, price):
    """检查单只股票是否满足全部6个条件"""
    try:
        end = datetime.now().strftime('%Y%m%d')
        start = (datetime.now() - timedelta(days=70)).strftime('%Y%m%d')
        df = ak.stock_zh_a_hist(symbol=code, period='daily',
                                 start_date=start, end_date=end, adjust='qfq')
        if df is None or len(df) < 20:
            return None
        
        df = df.sort_values('日期').tail(35).reset_index(drop=True)
        closes = df['收盘'].values.tolist()
        opens = df['开盘'].values.tolist()
        closes[-1] = price  # 替换今日收盘
        
        closes_arr = np.array(closes)
        opens_arr = np.array(opens)
        
        ma5 = np.mean(closes_arr[-5:])
        ma10 = np.mean(closes_arr[-10:])
        ma20 = np.mean(closes_arr[-20:])
        
        # 近30日涨停
        zt_count = sum(1 for i in range(-30, 0) if i > -len(closes_arr)
                        and (closes_arr[i]-opens_arr[i])/opens_arr[i]*100 >= 9.9)
        if chg >= 9.9: zt_count += 1
        had_zt = zt_count > 0
        
        # 硬条件
        if not (3.0 <= abs(chg) <= 9.5): return None
        if vr <= 1.0: return None
        if not (5.0 <= tr <= 15.0): return None
        if mc_yi > 200: return None
        if price <= ma5: return None
        
        # 均线评分
        if price > ma5 > ma10 > ma20: ma_s = 40
        elif price > ma5 > ma10: ma_s = 25
        elif price > ma5: ma_s = 10
        else: return None
        
        zt_s = 20 if had_zt else 0
        vol_s = 15 if vr > 2 else (10 if vr > 1.5 else 5)
        tr_s = 15 if 5 <= tr <= 10 else (10 if 10 < tr <= 15 else 5)
        chg_s = 15 if 3 <= chg <= 5 else (10 if 5 < chg <= 7 else 5)
        total = ma_s + zt_s + vol_s + tr_s + chg_s
        
        return {
            'name': name, 'code': code, 'market': get_market(code),
            'price': price, 'chg': chg, 'vr': vr, 'tr': tr, 'mc_yi': mc_yi,
            'had_zt': had_zt, 'TOTAL': total,
            'ma5': round(ma5,2), 'ma10': round(ma10,2), 'ma20': round(ma20,2)
        }
    except:
        return None

today = datetime.now().strftime('%Y%m%d')
print(f"选股扫描  {datetime.now().strftime('%H:%M:%S')}\n")

df = ak.stock_zt_pool_strong_em(date=today)
print(f"强势股池: {len(df)} 只，开始全量扫描...\n")

df['流通市值亿'] = df['流通市值'] / 1e8

all_results = []
batch = []

for _, r in df.iterrows():
    code = str(r['代码']).zfill(6)
    name = str(r['名称'])
    chg_v = float(r['涨跌幅'])
    vr_v = float(r['量比']) if r['量比'] else 0
    tr_v = float(r['换手率']) if r['换手率'] else 0
    mc_v = float(r['流通市值亿'])
    price_v = float(r['最新价'])
    batch.append((code, name, chg_v, vr_v, tr_v, mc_v, price_v))

# 处理
for code, name, chg_v, vr_v, tr_v, mc_v, price_v in batch:
    res = check_stock(code, name, chg_v, vr_v, tr_v, mc_v, price_v)
    if res:
        all_results.append(res)

all_results.sort(key=lambda x: x['TOTAL'], reverse=True)

print(f"符合条件: {len(all_results)} 只\n")
print(f"{'='*65}")
print(f"{'名称':<8} {'代码':<8} {'现价':>6} {'涨幅':>6} {'换手':>6} {'量比':>5} {'市值亿':>7} {'涨停':>4} {'总分':>5}")
print(f"{'='*65}")
for r in all_results:
    zt = '✅' if r['had_zt'] else ''
    print(f"{r['name']:<8} {r['market']}{r['code']:<7} {r['price']:>6.2f} {r['chg']:>+5.1f}% {r['tr']:>5.1f}% {r['vr']:>5.1f} {r['mc_yi']:>7.1f} {zt:>4} {r['TOTAL']:>5}")

if all_results:
    print(f"\n>>> 明日开盘重点 TOP3:")
    for i, r in enumerate(all_results[:3], 1):
        zt_str = '✅近30日涨停' if r['had_zt'] else '无涨停'
        print(f"  {i}. {r['name']} ({r['market']}{r['code']}) 总分{r['TOTAL']}  今日{r['chg']:+.1f}% 现价{r['price']:.2f} MA5={r['ma5']} 换手{r['tr']:.1f}% 量比{r['vr']:.1f}  {zt_str}")
    print(f"\n策略: 竞价高开2-5%非一字板轻仓；-3%止损")
