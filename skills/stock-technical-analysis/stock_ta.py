#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股技术分析脚本 v2 - 综合多指标判断
数据源: Sina Finance API
"""

import sys
import json
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import urllib.request

# ====== 股票名称映射 ======
STOCK_NAMES = {
    '600352': '浙江龙盛', '600089': '特变电工', '300033': '同花顺',
    '920046': '亿能电力', '688295': '中复神鹰', '600487': '亨通光电',
    '600893': '航发动力', '601168': '西部矿业', '300499': '高澜股份',
    '600114': '东睦股份', '831330': '普适导航', '430046': '圣博润',
    '300189': '神农种业', '600456': '宝钛股份', '600184': '光电股份',
    '600776': '东方通信', '603236': '移远通信', '600498': '烽火通信',
    '688981': '中芯国际', '688008': '澜起科技', '603986': '兆易创新',
    '002371': '北方华创', '600584': '长电科技', '688396': '华润微',
    '601600': '中国铝业', '600547': '山东黄金', '600456': '宝钛股份',
    '600150': '中国船舶', '600760': '中航沈飞', '601728': '中国电信',
    '600745': '闻泰科技', '000630': '铜陵有色', '000878': '云南铜业',
    '601989': '中国重工', '600184': '光电股份', '601166': '兴业银行',
}

def get_stock_name(code):
    code = code.replace('sh', '').replace('sz', '').replace('bj', '')
    return STOCK_NAMES.get(code, code)


def get_hist_data(code, days=60):
    """从新浪获取历史K线"""
    # 判断市场
    code = code.replace('sh', '').replace('sz', '').replace('bj', '')
    if code.startswith('6'):
        sym = 'sh' + code
    elif code.startswith('0') or code.startswith('3'):
        sym = 'sz' + code
    elif code.startswith('8') or code.startswith('4') or code.startswith('9'):
        sym = 'bj' + code
    else:
        sym = 'sh' + code

    url = f'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={sym}&scale=240&ma=no&datalen={days}'

    try:
        req = urllib.request.Request(url, headers={
            'Referer': 'http://finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('utf-8')
        records = json.loads(data)
        if not records:
            return None

        df = pd.DataFrame(records)
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df['volume'] = df['volume'].astype(float)
        return df
    except Exception as e:
        print(f'获取数据失败: {e}', file=sys.stderr)
        return None


def calculate_ma(series, period):
    return series.rolling(window=period).mean()


def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (rs + 1))


def calculate_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_hist = (dif - dea) * 2
    return dif, dea, macd_hist


def calculate_kdj(high, low, close, n=9):
    lowest_low = low.rolling(window=n).min()
    highest_high = high.rolling(window=n).max()
    rsv = (close - lowest_low) / (highest_high - lowest_low + 1e-9) * 100
    K = rsv.ewm(alpha=1/3, adjust=False).mean()
    D = K.ewm(alpha=1/3, adjust=False).mean()
    J = 3 * K - 2 * D
    return K, D, J


def calculate_boll(series, period=20, nb_std=2):
    mid = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper = mid + nb_std * std
    lower = mid - nb_std * std
    return upper, mid, lower


def analyze(code):
    df = get_hist_data(code, days=60)
    if df is None or len(df) < 20:
        return {'code': code, 'name': get_stock_name(code), 'error': True}

    close = df['close']
    high = df['high']
    low = df['low']
    volume = df['volume']

    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    price = float(latest['close'])
    prev_price = float(prev['close'])

    # 均线
    ma5 = calculate_ma(close, 5).iloc[-1]
    ma10 = calculate_ma(close, 10).iloc[-1]
    ma20 = calculate_ma(close, 20).iloc[-1]
    ma60 = calculate_ma(close, min(60, len(df))).iloc[-1]

    # RSI
    rsi14 = calculate_rsi(close, 14).iloc[-1]
    rsi6 = calculate_rsi(close, 6).iloc[-1]

    # MACD
    dif, dea, macd_hist = calculate_macd(close)
    dif_val = dif.iloc[-1]
    dea_val = dea.iloc[-1]
    macd_val = macd_hist.iloc[-1]

    # KDJ
    k, d, j = calculate_kdj(high, low, close)
    k_val = k.iloc[-1]
    j_val = j.iloc[-1]

    # BOLL
    boll_upper, boll_mid, boll_lower = calculate_boll(close)
    boll_u = boll_upper.iloc[-1]
    boll_m = boll_mid.iloc[-1]
    boll_l = boll_lower.iloc[-1]

    # 量比
    vol5 = volume.tail(5).mean()
    vol10 = volume.tail(10).mean()
    vol_ratio = vol5 / vol10 if vol10 > 0 else 1

    # 近期涨跌
    recent_10d = (close.iloc[-1] - close.iloc[-10]) / close.iloc[-10] * 100 if len(df) >= 10 else 0

    # ====== 综合评分 ======
    score = 0
    signals = []

    # 均线
    if price > ma5 > ma10 > ma20:
        signals.append('均线多头排列'); score += 2
    elif price < ma5 < ma10 < ma20:
        signals.append('均线空头排列'); score -= 2
    elif price > ma5:
        signals.append('站上短期均线'); score += 0.5
    else:
        signals.append('跌破短期均线'); score -= 0.5

    # RSI
    if rsi14 > 75: signals.append(f'RSI极度超买({rsi14:.0f})'); score -= 2
    elif rsi14 > 65: signals.append(f'RSI超买({rsi14:.0f})'); score -= 1
    elif rsi14 < 25: signals.append(f'RSI极度超卖({rsi14:.0f})'); score += 2
    elif rsi14 < 35: signals.append(f'RSI超卖({rsi14:.0f})'); score += 1
    elif rsi14 > 50: signals.append(f'RSI偏强({rsi14:.0f})'); score += 0.5
    else: signals.append(f'RSI偏弱({rsi14:.0f})'); score -= 0.5

    # MACD
    if dif_val > dea_val and macd_val > 0:
        signals.append('MACD零轴上金叉'); score += 2
    elif dif_val > dea_val and macd_val < 0:
        signals.append('MACD零轴下金叉'); score += 1
    elif dif_val < dea_val and macd_val < 0:
        signals.append('MACD零轴下死叉'); score -= 2
    else:
        signals.append('MACD零轴上死叉'); score -= 1

    # KDJ
    if j_val > 90: signals.append(f'KDJ极度超买({j_val:.0f})'); score -= 1.5
    elif j_val > 80: signals.append(f'KDJ超买({j_val:.0f})'); score -= 0.5
    elif j_val < 10: signals.append(f'KDJ极度超卖({j_val:.0f})'); score += 1.5
    elif j_val < 20: signals.append(f'KDJ超卖({j_val:.0f})'); score += 0.5

    # BOLL
    if price > boll_m: signals.append('BOLL中轨上方'); score += 0.5
    else: signals.append('BOLL中轨下方'); score -= 0.5

    # 趋势
    if recent_10d > 8: signals.append(f'短线强势(+{recent_10d:.1f}%)'); score += 1
    elif recent_10d < -8: signals.append(f'短线弱势({recent_10d:.1f}%)'); score -= 1

    # 量比
    if vol_ratio > 2: signals.append(f'明显放量({vol_ratio:.1f}x)'); score += 0.5
    elif vol_ratio > 1.5: signals.append(f'温和放量({vol_ratio:.1f}x)'); score += 0.3

    # 支撑/压力
    recent_lows = low.tail(20).min()
    recent_highs = high.tail(20).max()

    # 综合建议
    if score >= 4: rec = '🟢 强烈买入'
    elif score >= 2: rec = '🟡 谨慎买入'
    elif score >= 0: rec = '🔵 持有观察'
    elif score >= -2: rec = '🟡 谨慎持有'
    else: rec = '🔴 建议卖出'

    return {
        'code': code, 'name': get_stock_name(code),
        'price': price,
        'change_pct': (price - prev_price) / prev_price * 100,
        'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma60': ma60,
        'rsi6': rsi6, 'rsi14': rsi14,
        'dif': dif_val, 'dea': dea_val, 'macd': macd_val,
        'k': k_val, 'j': j_val,
        'boll_u': boll_u, 'boll_m': boll_m, 'boll_l': boll_l,
        'vol_ratio': vol_ratio,
        'recent_10d': recent_10d,
        'support': recent_lows, 'resistance': recent_highs,
        'score': score, 'signals': signals, 'rec': rec
    }


def format_result(r):
    if r.get('error'):
        return f"{r['name']}({r['code']}): 数据不足，无法分析"

    chg = r['change_pct']
    chg_str = f"+{chg:.2f}%" if chg >= 0 else f"{chg:.2f}%"

    lines = [
        f"📊 {r['name']}({r['code']})",
        f"{'─'*20}",
        f"💰 现价: {r['price']:.3f}  今日: {chg_str}",
        f"",
        f"📈 均线: MA5={r['ma5']:.3f} MA10={r['ma10']:.3f} MA20={r['ma20']:.3f}",
        f"   {'🟢' if r['price'] > r['ma5'] > r['ma10'] > r['ma20'] else '🔴' if r['price'] < r['ma5'] < r['ma10'] < r['ma20'] else '🟡'} {'多头' if r['price'] > r['ma5'] > r['ma10'] else '空头' if r['price'] < r['ma5'] < r['ma10'] else '震荡'}",
        f"",
        f"📉 RSI6={r['rsi6']:.0f} RSI14={r['rsi14']:.0f}  {'⚠️超买' if r['rsi14']>65 else '🔥超卖' if r['rsi14']<35 else '正常'}",
        f"📊 MACD: DIF={r['dif']:.3f} DEA={r['dea']:.3f} MACD柱={r['macd']:.3f}",
        f"   {'🟢金叉' if r['dif']>r['dea'] else '🔴死叉'} {'(0轴上)' if r['macd']>0 else '(0轴下)'}",
        f"🎯 KDJ: K={r['k']:.1f} J={r['j']:.1f}  {'⚠️超买' if r['j']>85 else '🔥超卖' if r['j']<20 else '正常'}",
        f"📐 BOLL: 上={r['boll_u']:.3f} 中={r['boll_m']:.3f} 下={r['boll_l']:.3f}",
        f"🔑 支撑 {r['support']:.3f}  压力 {r['resistance']:.3f}",
        f"📦 量比: {r['vol_ratio']:.2f}x  近10日: {r['recent_10d']:+.1f}%",
        f"",
        f"🎯 综合信号:",
    ]
    for s in r['signals']:
        lines.append(f"   • {s}")

    lines.extend([
        f"{'─'*20}",
        f"综合评分: {r['score']:+.1f}分  {r['rec']}",
        f"⚠️ 分析仅供参考，不构成投资建议",
    ])
    return '\n'.join(lines)


if __name__ == '__main__':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if len(sys.argv) < 2:
        print("用法: python ta_analysis.py <代码>")
        print("示例: python ta_analysis.py 600352")
        sys.exit(1)

    code = sys.argv[1].strip()
    result = analyze(code)
    print(format_result(result))
