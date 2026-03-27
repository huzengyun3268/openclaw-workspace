import urllib.request
import json

def get_kline_sina(code, market, days=60):
    url = f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={market}{code}&scale=240&ma=5&datalen={days}'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://finance.sina.com.cn'
    })
    r = urllib.request.urlopen(req, timeout=10)
    return json.loads(r.read().decode('gbk'))

def calc_ma(closes, period):
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period

def calc_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    if len(gains) < period:
        return None
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calc_macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal:
        return None, None, None
    # EMA
    ema_fast = sum(closes[:fast]) / fast
    ema_slow = sum(closes[:slow]) / slow
    diffs = []
    for c in closes[slow:]:
        ema_fast = ema_fast * 11/13 + c * 2/13
        ema_slow = ema_slow * 25/27 + c * 2/27
        diffs.append(ema_fast - ema_slow)
    if len(diffs) < signal:
        return None, None, None
    dea = sum(diffs[:signal]) / signal
    macd_list = []
    for d in diffs[signal-1:]:
        dea = dea * 8/10 + d * 2/10
        macd_list.append(2 * (d - dea))
    return diffs[-1] * 2, dea * 2, macd_list[-1]

def calc_boll(closes, period=20):
    if len(closes) < period:
        return None, None, None
    recent = closes[-period:]
    ma = sum(recent) / period
    variance = sum((x - ma) ** 2 for x in recent) / period
    std = variance ** 0.5
    return ma, ma + 2 * std, ma - 2 * std

def analyze(code, name, cost, stop):
    try:
        market = 'sh' if code.startswith('6') or code.startswith('688') else ('sz' if len(code) == 6 else 'bj')
        kline = get_kline_sina(code, market)
        if not kline or len(kline) < 30:
            return None
        closes = [float(d['close']) for d in kline]
        now = closes[-1]
        
        ma5 = calc_ma(closes, 5)
        ma10 = calc_ma(closes, 10)
        ma20 = calc_ma(closes, 20)
        ma60 = calc_ma(closes, 60) if len(closes) >= 60 else None
        rsi6 = calc_rsi(closes, 6)
        rsi14 = calc_rsi(closes, 14)
        dif, dea, macd_hist = calc_macd(closes)
        boll_ma, boll_upper, boll_lower = calc_boll(closes)
        
        # Score
        score = 0
        signals = []
        
        # Price vs MA
        if now > ma5 and now > ma10 and now > ma20:
            score += 1
            signals.append('多头排列')
        elif now < ma5 and now < ma10 and now < ma20:
            score -= 1
            signals.append('空头排列')
        
        # RSI
        if rsi14:
            if rsi14 > 75:
                score -= 2
                signals.append(f'RSI14超买{rsi14:.0f}')
            elif rsi14 < 30:
                score += 2
                signals.append(f'RSI14超卖{rsi14:.0f}')
            elif rsi14 > 65:
                score -= 1
                signals.append(f'RSI14偏高{rsi14:.0f}')
            elif rsi14 < 40:
                score += 1
                signals.append(f'RSI14偏低{rsi14:.0f}')
        
        # MACD
        if macd_hist is not None:
            if dif > dea and macd_hist > 0:
                score += 1
                signals.append('MACD金叉/红柱')
            elif dif < dea and macd_hist < 0:
                score -= 1
                signals.append('MACD死叉/绿柱')
        
        # BOLL
        if boll_lower and now < boll_lower:
            score += 2
            signals.append('BOLL下轨支撑')
        elif boll_upper and now > boll_upper:
            score -= 1
            signals.append('BOLL上轨压力')
        
        # Cost vs price
        pl_pct = (now - cost) / cost * 100
        if pl_pct < -20:
            score += 1
            signals.append(f'深套{pl_pct:.0f}%')
        
        # vs stop
        if stop:
            dist_stop = (stop / now - 1) * 100
            if dist_stop < 5:
                score -= 2
                signals.append(f'⚠️离止损{dist_stop:.1f}%')
            elif dist_stop < 10:
                score -= 1
                signals.append(f'⚠️止损附近{dist_stop:.1f}%')
        
        # Trend (last 5 days)
        if len(closes) >= 6:
            recent_trend = sum(closes[-i] - closes[-i-1] for i in range(1, 6)) / 5
            if recent_trend > 0:
                score += 0.5
                signals.append('近期上升')
            else:
                score -= 0.5
                signals.append('近期下降')
        
        signal_label = '🟢强烈买入' if score >= 4 else '🟡谨慎买入' if score >= 2 else '🔵持有观察' if score >= 0 else '🟡谨慎持有' if score >= -2 else '🔴建议卖出'
        
        return {
            'name': name,
            'now': now,
            'cost': cost,
            'stop': stop,
            'ma5': ma5, 'ma10': ma10, 'ma20': ma20, 'ma60': ma60,
            'rsi6': rsi6, 'rsi14': rsi14,
            'dif': dif, 'dea': dea, 'macd_hist': macd_hist,
            'boll_ma': boll_ma, 'boll_upper': boll_upper, 'boll_lower': boll_lower,
            'score': score,
            'signal': signal_label,
            'signals': signals,
            'pl_pct': pl_pct,
        }
    except Exception as e:
        return {'name': name, 'error': str(e)}

# Analyze critical stocks
critical_stocks = [
    ('600352', '浙江龙盛', 16.52, 12.0),
    ('300033', '同花顺', 423.488, 280),
    ('920046', '亿能电力', 329.553, 27.0),
    ('600089', '特变电工', 24.765, 25.0),
    ('301638', '南网数字(老婆)', 32.64, 28.0),
    ('600114', '东睦股份(老婆)', 26.0, 25.0),
]

results = []
for code, name, cost, stop in critical_stocks:
    result = analyze(code, name, cost, stop)
    results.append(result)

with open(r'C:\Users\Administrator\.openclaw\workspace\ta_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('done')
