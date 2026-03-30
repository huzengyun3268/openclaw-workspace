# -*- coding: utf-8 -*-
"""
A股技术分析脚本
使用方法: python stock_tech_analysis.py <sh600352>
"""

import sys
import json
import urllib.request
import urllib.error
import datetime

def get_history(code, days=60):
    """获取历史K线数据 - 使用东方财富API"""
    end_date = datetime.datetime.now().strftime('%Y%m%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=days*2)).strftime('%Y%m%d')
    stk = code.replace('sh', '').replace('sz', '').replace('bj', '')
    mkt = '1' if code.startswith('sh') else '0' if code.startswith('sz') else '8'
    url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={mkt}.{stk}&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&klt=101&fqt=1&beg={start_date}&end={end_date}&smplmt={days}&lmt={days}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.eastmoney.com/'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            klines = data.get('data', {}).get('klines', [])
            result = []
            for k in klines:
                parts = k.split(',')
                if len(parts) >= 6:
                    result.append([parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], '0'])
            return result
    except Exception as e:
        print(f"获取历史数据失败: {e}")
        return []

def get_realtime(code):
    """获取实时行情"""
    url = f"https://qt.gtimg.cn/q={code}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode('gbk', errors='replace')
            parts = raw.split('~')
            if len(parts) > 32:
                return {
                    'name': parts[1],
                    'code': parts[2],
                    'price': float(parts[3]),
                    'yesterday_close': float(parts[4]),
                    'open': float(parts[5]),
                    'volume': int(parts[6]),
                    'high': float(parts[33]),
                    'low': float(parts[34]),
                    'change_pct': float(parts[32]) if parts[32] else 0,
                }
    except Exception as e:
        print(f"获取实时数据失败: {e}")
    return None

def calc_ma(prices, period):
    """计算移动平均线"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def calc_ema(prices, period):
    """计算指数移动平均线"""
    if len(prices) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (price * multiplier) + (ema * (1 - multiplier))
    return ema

def calc_rsi(prices, period=14):
    """计算RSI"""
    if len(prices) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(diff))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calc_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD"""
    if len(prices) < slow + signal:
        return None, None, None
    ema_fast = calc_ema(prices, fast)
    ema_slow = calc_ema(prices, slow)
    if ema_fast is None or ema_slow is None:
        return None, None, None
    dif = ema_fast - ema_slow
    dea = dif * 0.8
    macd = (dif - dea) * 2
    return round(dif, 3), round(dea, 3), round(macd, 3)

def calc_boll(prices, period=20, multiplier=2):
    """计算布林带"""
    if len(prices) < period:
        return None, None, None
    recent = prices[-period:]
    sma = sum(recent) / period
    variance = sum((p - sma) ** 2 for p in recent) / period
    std = variance ** 0.5
    upper = sma + (std * multiplier)
    lower = sma - (std * multiplier)
    return round(upper, 3), round(sma, 3), round(lower, 3)

def calc_kdj(highs, lows, closes, period=9):
    """计算KDJ"""
    if len(highs) < period:
        return None, None, None
    recent_high = max(highs[-period:])
    recent_low = min(lows[-period:])
    if recent_high == recent_low:
        rsv = 50
    else:
        rsv = (closes[-1] - recent_low) / (recent_high - recent_low) * 100
    k = 50
    d = 50
    k = (2/3) * k + (1/3) * rsv
    d = (2/3) * d + (1/3) * k
    j = 3 * k - 2 * d
    return round(k, 2), round(d, 2), round(j, 2)

def analyze(code):
    """完整技术分析"""
    print(f"\n{'='*50}")
    print(f"正在分析: {code}")
    print(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*50)
    
    rt = get_realtime(code)
    if rt:
        print(f"\n【实时行情】")
        print(f"  名称: {rt['name']}")
        print(f"  现价: {rt['price']:.3f} 元")
        print(f"  涨跌: {rt['change_pct']:+.2f}%")
        print(f"  今高: {rt['high']:.3f}  今低: {rt['low']:.3f}")
        print(f"  今开: {rt['open']:.3f}  昨收: {rt['yesterday_close']:.3f}")
    else:
        print("无法获取实时数据")
        return
    
    history = get_history(code, 90)
    if not history:
        print("无法获取历史数据")
        return
    
    closes = [float(d[2]) for d in history]
    highs = [float(d[3]) for d in history]
    lows = [float(d[4]) for d in history]
    
    print(f"\n【技术指标】")
    
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
    ma60 = calc_ma(closes, 60) if len(closes) >= 60 else None
    
    ma5_str = f"{ma5:.3f}" if ma5 else "N/A"
    ma10_str = f"{ma10:.3f}" if ma10 else "N/A"
    ma20_str = f"{ma20:.3f}" if ma20 else "N/A"
    ma60_str = f"{ma60:.3f}" if ma60 else "N/A"
    
    ma_signal = ""
    if ma5 and ma10:
        if ma5 > ma10:
            ma_signal = "  [MA5>MA10 金叉]"
        else:
            ma_signal = "  [MA5<MA10 死叉]"
    
    print(f"  MA5:   {ma5_str:>10}{ma_signal}")
    print(f"  MA10:  {ma10_str:>10}")
    print(f"  MA20:  {ma20_str:>10}")
    print(f"  MA60:  {ma60_str:>10}")
    
    rsi6 = calc_rsi(closes, 6)
    rsi12 = calc_rsi(closes, 12)
    rsi24 = calc_rsi(closes, 24)
    
    def rsi_signal(v):
        if v and v > 75: return "[超买]"
        if v and v < 25: return "[超卖]"
        return "[正常]"
    
    print(f"  RSI6:  {rsi6:>10.2f}  {rsi_signal(rsi6)}")
    print(f"  RSI12: {rsi12:>10.2f}  {rsi_signal(rsi12)}")
    print(f"  RSI24: {rsi24:>10.2f}  {rsi_signal(rsi24)}")
    
    dif, dea, macd = calc_macd(closes)
    if dif is not None:
        macd_color = "红柱" if macd > 0 else "绿柱"
        macd_cross = "  [DIF上穿DEA]" if dif > dea else "  [DIF下穿DEA]" if dif < dea else ""
        print(f"  MACD:  DIF={dif:>8.3f}  DEA={dea:>8.3f}  MACD={macd:>8.3f}  [{macd_color}]{macd_cross}")
    
    boll_upper, boll_mid, boll_lower = calc_boll(closes)
    if boll_upper:
        current_price = rt['price']
        boll_pos = (current_price - boll_lower) / (boll_upper - boll_lower) * 100 if boll_upper != boll_lower else 50
        boll_zone = "(下轨附近超卖)" if boll_pos < 20 else "(上轨附近超买)" if boll_pos > 80 else "(中轨附近)"
        print(f"  BOLL:  上轨={boll_upper:.3f}  中轨={boll_mid:.3f}  下轨={boll_lower:.3f}")
        print(f"         现价所处位置: {boll_pos:.1f}%  {boll_zone}")
    
    k, d, j = calc_kdj(highs, lows, closes)
    if k:
        kdj_signal = "[超买]" if j > 80 else "[超卖]" if j < 20 else "[正常]"
        print(f"  KDJ:   K={k:>8.2f}  D={d:>8.2f}  J={j:>8.2f}  {kdj_signal}")
    
    # 综合评分
    score = 0
    reasons = []
    
    if ma5 and ma10 and ma5 > ma10:
        score += 20
        reasons.append("MA5上穿MA10")
    elif ma5 and ma10 and ma5 < ma10:
        score -= 20
        reasons.append("MA5下穿MA10")
    
    if rsi6 and rsi6 < 30:
        score += 20
        reasons.append("RSI超卖")
    elif rsi6 and rsi6 > 75:
        score -= 15
        reasons.append("RSI超买")
    
    if macd and dif and dea:
        if dif > dea and dif > 0:
            score += 15
            reasons.append("MACD多头")
        elif dif < dea:
            score -= 15
            reasons.append("MACD死叉")
    
    if boll_pos and boll_pos < 20:
        score += 20
        reasons.append("触及布林下轨")
    elif boll_pos and boll_pos > 80:
        score -= 15
        reasons.append("触及布林上轨")
    
    if j and j < 20:
        score += 15
        reasons.append("KDJ超卖")
    elif j and j > 80:
        score -= 10
        reasons.append("KDJ超买")
    
    print(f"\n【综合评分】  {score:>+3d} / 100")
    if reasons:
        print(f"  信号: {', '.join(reasons)}")
    
    verdict = ""
    if score >= 30:
        verdict = "【结论】: 偏多信号，可关注买入机会"
    elif score <= -30:
        verdict = "【结论】: 偏空信号，注意止损或观望"
    else:
        verdict = "【结论】: 中性，震荡整理，观望为主"
    print(f"  {verdict}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python stock_tech_analysis.py <股票代码>")
        print("示例: python stock_tech_analysis.py sh600487")
        sys.exit(1)
    
    code = sys.argv[1]
    analyze(code)
