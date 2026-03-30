# -*- coding: utf-8 -*-
import urllib.request, json, datetime

API = "https://stockboot.jiuma.cn/api/dynamic-select/execute"
HEADERS = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0'}

def get_history_em(code, days=60):
    stk = code[2:]
    mkt = '1' if code.startswith('sh') else '0' if code.startswith('sz') else '8'
    end = datetime.datetime.now().strftime('%Y%m%d')
    start = (datetime.datetime.now() - datetime.timedelta(days=days*2)).strftime('%Y%m%d')
    url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
           f"?secid={mkt}.{stk}&fields1=f1,f2,f3,f4,f5,f6"
           f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58"
           f"&klt=101&fqt=1&beg={start}&end={end}&smplmt={days}&lmt={days}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.eastmoney.com/'})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode('utf-8'))
            klines = data.get('data', {}).get('klines', [])
            result = []
            for k in klines:
                p = k.split(',')
                if len(p) >= 6:
                    result.append([p[0], p[1], p[2], p[3], p[4], p[5], '0'])
            return result
    except:
        return []

def calc_score(closes, highs, lows, price):
    if len(closes) < 26:
        return -999, []
    score = 0
    reasons = []
    ma5 = sum(closes[-5:]) / 5
    ma10 = sum(closes[-10:]) / 10
    if ma5 > ma10:
        score += 20; reasons.append("MA_gold")
    else:
        score -= 20; reasons.append("MA_dead")
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i-1]
        gains.append(d if d > 0 else 0)
        losses.append(abs(d) if d < 0 else 0)
    avg_g = sum(gains[-14:]) / 14 if len(gains) >= 14 else 0
    avg_l = sum(losses[-14:]) / 14 if len(losses) >= 14 else 0
    rsi = 100 - (100 / (1 + avg_g/avg_l)) if avg_l > 0 else 100
    if rsi < 30:
        score += 20; reasons.append(f"RSI_oversold_{rsi:.0f}")
    elif rsi > 75:
        score -= 15; reasons.append(f"RSI_overbought_{rsi:.0f}")
    ema12 = closes[0]
    ema26 = closes[0]
    for c in closes[1:]:
        ema12 = c*(2/13) + ema12*(11/13)
        ema26 = c*(2/27) + ema26*(25/27)
    dif = ema12 - ema26
    dea = dif * 0.8
    macd = (dif - dea) * 2
    if dif > 0:
        score += 15; reasons.append("MACD_bull")
    else:
        score -= 15; reasons.append("MACD_bear")
    n = min(20, len(closes))
    recent = closes[-n:]
    sma = sum(recent) / n
    variance = sum((c - sma)**2 for c in recent) / n
    std = variance ** 0.5
    upper = sma + 2*std
    lower = sma - 2*std
    boll_pos = (price - lower) / (upper - lower) * 100 if upper != lower else 50
    if boll_pos < 20:
        score += 20; reasons.append(f"BOLL_low_{boll_pos:.0f}")
    elif boll_pos > 80:
        score -= 15; reasons.append(f"BOLL_high_{boll_pos:.0f}")
    kh = max(highs[-9:]) if len(highs) >= 9 else max(highs)
    kl = min(lows[-9:]) if len(lows) >= 9 else min(lows)
    rsv = (closes[-1] - kl) / (kh - kl) * 100 if kh != kl else 50
    k = (2/3)*50 + (1/3)*rsv
    d = (2/3)*50 + (1/3)*k
    j = 3*k - 2*d
    if j < 20:
        score += 15; reasons.append(f"KDJ_oversold_{j:.0f}")
    elif j > 80:
        score -= 10; reasons.append(f"KDJ_overbought_{j:.0f}")
    return score, reasons

# 执行选股
data = json.dumps({"sentence": "涨幅大于3%小于5%;量比大于1;流通市值大于50亿小于200亿;非ST"}).encode('utf-8')
req = urllib.request.Request(API, data=data, headers=HEADERS, method='POST')
with urllib.request.urlopen(req, timeout=15) as r:
    result = json.loads(r.read().decode('utf-8'))

stocks = result['data']['stocks']
print(f"Total: {len(stocks)} stocks")

ranked = []
for s in stocks:
    code = s['code']
    mkt = 'sh' if s['marketType'] == 'SH' else 'sz'
    full = f"{mkt}{code}"
    change = round(s.get('changeRate', 0), 2)
    hist = get_history_em(full, 90)
    if len(hist) < 26:
        continue
    closes = [float(d[2]) for d in hist]
    highs = [float(d[3]) for d in hist]
    lows = [float(d[4]) for d in hist]
    # 获取最新收盘价
    last_price = closes[-1]
    score, reasons = calc_score(closes, highs, lows, last_price)
    ranked.append({
        'code': code, 'mkt': mkt, 'full': full,
        'change': change, 'price': last_price,
        'score': score, 'reasons': reasons
    })

ranked.sort(key=lambda x: x['score'], reverse=True)

# 保存到文件（不用中文，避免乱码）
with open('C:/Users/Administrator/.openclaw/workspace/ranking_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"=== TOP 10 STOCKS BY SCORE ===\n\n")
    for i, s in enumerate(ranked[:10], 1):
        f.write(f"{i}. {s['full']}  score={s['score']:+3d}  change={s['change']}%  price={s['price']}\n")
        f.write(f"   signals: {', '.join(s['reasons'][:5])}\n\n")

print("Done! Results saved.")
print(f"\nTOP 10:")
for i, s in enumerate(ranked[:10], 1):
    print(f"{i}. {s['full']}  score={s['score']:+3d}  change={s['change']}%")
