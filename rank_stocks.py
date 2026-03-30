# -*- coding: utf-8 -*-
import urllib.request, json, datetime

API = "https://stockboot.jiuma.cn/api/dynamic-select/execute"
HIST_URL = "https://qt.gtimg.cn/q="
HEADERS = {'Content-Type': 'application/json; charset=utf-8', 'User-Agent': 'Mozilla/5.0'}

def get_realtime(code):
    url = f"{HIST_URL}{code}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            raw = r.read().decode('gbk', errors='replace')
            parts = raw.split('~')
            if len(parts) > 34:
                return {
                    'price': float(parts[3]),
                    'change': float(parts[32]) if parts[32] else 0,
                    'high': float(parts[33]),
                    'low': float(parts[34]),
                    'vol': int(parts[6]) if parts[6].isdigit() else 0,
                }
    except:
        pass
    return None

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
    
    # MA
    ma5 = sum(closes[-5:]) / 5
    ma10 = sum(closes[-10:]) / 10
    ma20 = sum(closes[-20:]) / 20
    if ma5 > ma10:
        score += 20
        reasons.append("MA金叉")
    else:
        score -= 20
        reasons.append("MA死叉")
    
    # RSI
    gains, losses = [], []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i-1]
        gains.append(d if d > 0 else 0)
        losses.append(abs(d) if d < 0 else 0)
    avg_g = sum(gains[-14:]) / 14 if len(gains) >= 14 else 0
    avg_l = sum(losses[-14:]) / 14 if len(losses) >= 14 else 0
    rsi = 100 - (100 / (1 + avg_g/avg_l)) if avg_l > 0 else 100
    if rsi < 30:
        score += 20; reasons.append(f"RSI超卖({rsi:.0f})")
    elif rsi > 75:
        score -= 15; reasons.append(f"RSI超买({rsi:.0f})")
    
    # MACD
    ema12 = closes[0]
    ema26 = closes[0]
    m = 2/13
    for c in closes[1:]:
        ema12 = c*m + ema12*(1-m)
    m = 2/27
    for c in closes[1:]:
        ema26 = c*m + ema26*(1-m)
    dif = ema12 - ema26
    dea = dif * 0.8
    macd = (dif - dea) * 2
    if dif > 0 and macd > 0:
        score += 15; reasons.append("MACD多头")
    elif dif < 0:
        score -= 15; reasons.append("MACD空头")
    
    # BOLL
    n = min(20, len(closes))
    recent = closes[-n:]
    sma = sum(recent) / n
    variance = sum((c - sma)**2 for c in recent) / n
    std = variance ** 0.5
    upper = sma + 2*std
    lower = sma - 2*std
    boll_pos = (price - lower) / (upper - lower) * 100 if upper != lower else 50
    if boll_pos < 20:
        score += 20; reasons.append(f"BOLL下轨({boll_pos:.0f}%)")
    elif boll_pos > 80:
        score -= 15; reasons.append(f"BOLL上轨({boll_pos:.0f}%)")
    
    # KDJ
    kh = max(highs[-9:]) if len(highs) >= 9 else max(highs)
    kl = min(lows[-9:]) if len(lows) >= 9 else min(lows)
    if kh != kl:
        rsv = (closes[-1] - kl) / (kh - kl) * 100
    else:
        rsv = 50
    k = (2/3)*50 + (1/3)*rsv
    d = (2/3)*50 + (1/3)*k
    j = 3*k - 2*d
    if j < 20:
        score += 15; reasons.append(f"KDJ超卖({j:.0f})")
    elif j > 80:
        score -= 10; reasons.append(f"KDJ超买({j:.0f})")
    
    return score, reasons

# 执行选股
data = json.dumps({"sentence": "涨幅大于3%小于5%;量比大于1;流通市值大于50亿小于200亿;非ST"}).encode('utf-8')
req = urllib.request.Request(API, data=data, headers=HEADERS, method='POST')
with urllib.request.urlopen(req, timeout=15) as r:
    result = json.loads(r.read().decode('utf-8'))

stocks = result['data']['stocks']
print(f"选出 {len(stocks)} 只股票，开始技术分析...\n")

ranked = []
for s in stocks:
    code = s['code']
    mkt = 'sh' if s['marketType'] == 'SH' else 'sz'
    full = f"{mkt}{code}"
    name = s.get('name', 'N/A')
    change = round(s.get('changeRate', 0), 2)
    extra = s.get('extraFields', {})
    vol_ratio = list(extra.values())[0] if extra else ''
    
    rt = get_realtime(full)
    if not rt:
        continue
    
    hist = get_history_em(full, 90)
    if len(hist) < 26:
        continue
    
    closes = [float(d[2]) for d in hist]
    highs = [float(d[3]) for d in hist]
    lows = [float(d[4]) for d in hist]
    
    score, reasons = calc_score(closes, highs, lows, rt['price'])
    ranked.append({
        'code': code, 'name': name, 'mkt': mkt,
        'price': rt['price'], 'change': change,
        'vol_ratio': vol_ratio,
        'score': score, 'reasons': reasons
    })
    print(f"  {code} {name} 评分:{score:>+3d}  {' '.join(reasons[:3])}")

# 排序
ranked.sort(key=lambda x: x['score'], reverse=True)

print(f"\n{'='*55}")
print(f"【评分排名 TOP 10】")
print(f"{'='*55}")
for i, s in enumerate(ranked[:10], 1):
    print(f"{i}. {s['code']} {s['name']} 评分:{s['score']:>+3d}")
    print(f"   现价:{s['price']} 涨幅:{s['change']}%  量比:{s['vol_ratio']}")
    print(f"   信号: {' '.join(s['reasons'][:4])}")
    print()
