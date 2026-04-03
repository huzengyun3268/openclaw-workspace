import urllib.request, re, sys, numpy as np, pandas as pd
sys.stdout.reconfigure(encoding='utf-8')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'

def fetch_kline(code_market, days=30):
    try:
        url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code_market},day,,,{days},qfq'
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://gu.qq.com'})
        r = urllib.request.urlopen(req, timeout=8)
        txt = r.read().decode('utf-8')
        # Find the qfqday data
        idx = txt.find('qfqday')
        if idx < 0:
            return None
        start = txt.find('[', idx)
        end = txt.find(']]', start)
        raw = txt[start:end+1]
        items = re.findall(r'\["([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)"\]', raw)
        if not items:
            return None
        dates, opens, closes, highs, lows, vols = [], [], [], [], [], []
        for it in items:
            dates.append(it[0])
            opens.append(float(it[1]))
            closes.append(float(it[2]))
            highs.append(float(it[3]))
            lows.append(float(it[4]))
            vols.append(float(it[5]))
        return {'date': dates, 'open': opens, 'close': closes, 'high': highs, 'low': lows, 'vol': vols}
    except Exception as e:
        print(f'Error fetching {code_market}: {e}')
        return None

def calc_score(kline, name, code):
    if not kline or len(kline['close']) < 20:
        return None
    c = np.array(kline['close'])
    
    ma5 = np.mean(c[-5:])
    ma10 = np.mean(c[-10:])
    ma20 = np.mean(c[-20:])
    current = c[-1]
    
    # MA
    ma = 0
    if current > ma5 > ma10 > ma20: ma = 40
    elif current > ma5 and ma5 > ma10: ma = 25
    elif current > ma5: ma = 10
    elif current < ma5 < ma10 < ma20: ma = -20
    
    # RSI
    d = np.diff(c)
    g = np.where(d > 0, d, 0)
    l = np.where(d < 0, -d, 0)
    ag = np.mean(g[-14:])
    al = np.mean(l[-14:])
    rsi = 100 - 100 / (1 + ag/(al+1e-10))
    rsi_s = 15 if rsi < 30 else (-10 if rsi > 70 else 0)
    
    # MACD
    ema12 = pd.Series(c).ewm(span=12).mean().values[-1]
    ema26 = pd.Series(c).ewm(span=26).mean().values[-1]
    macd = ema12 - ema26
    ema12_p = pd.Series(c[:-1]).ewm(span=12).mean().values[-1]
    ema26_p = pd.Series(c[:-1]).ewm(span=26).mean().values[-1]
    macd_prev = ema12_p - ema26_p
    macd_s = 10 if macd > macd_prev and macd > 0 else (-10 if macd < macd_prev else 0)
    
    # KDJ
    l14 = np.min(c[-14:])
    h14 = np.max(c[-14:])
    k = 50 if h14 == l14 else (current - l14) / (h14 - l14) * 100
    j = 3 * k - 100
    kdj_s = 10 if j < 20 else (-10 if j > 80 else 0)
    
    # BOLL
    std = np.std(c[-20:])
    boll_l = ma20 - 2 * std
    boll_m = ma20
    boll_s = 10 if current <= boll_l else (5 if current < boll_m else 0)
    
    total = ma + rsi_s + macd_s + kdj_s + boll_s
    return {
        'name': name, 'code': code, 'price': current,
        'MA': ma, 'RSI': round(rsi, 1), 'RSI_s': rsi_s,
        'MACD': macd_s, 'KDJ': kdj_s, 'BOLL': boll_s,
        'TOTAL': total
    }

candidates = [
    ('sh603803', '瑞斯康达'),
    ('sz002560', '通达股份'),
    ('sz002269', '美邦服饰'),
    ('sh600249', '两面针'),
    ('sh600488', '天药股份'),
    ('sh603687', '大胜达'),
    ('sz002432', '九安医疗'),
    ('sh603248', '环保股份'),
    ('sz000815', '美利云'),
    ('sh603131', '中潜股份'),
]

print(f"综合评分选股 {__import__('datetime').datetime.now().strftime('%H:%M')}\n")
results = []
for code_market, name in candidates:
    code = code_market[2:]
    market = code_market[:2]
    kline = fetch_kline(code_market, 30)
    result = calc_score(kline, name, code)
    if result:
        result['market'] = market
        result['full_code'] = code_market
        results.append(result)
        print(f"  {name}: price={result['price']:.2f} MA={result['MA']} RSI={result['RSI']} MACD={result['MACD']} KDJ={result['KDJ']} BOLL={result['BOLL']} TOTAL={result['TOTAL']}")

results.sort(key=lambda x: x['TOTAL'], reverse=True)

print(f"\n{'='*65}")
print(f"{'名称':<8} {'代码':<8} {'现价':>6} {'MA':>5} {'RSI':>5} {'MACD':>5} {'KDJ':>5} {'BOLL':>5} {'总分':>5}")
print(f"{'='*65}")
for r in results:
    print(f"{r['name']:<8} {r['code']:<8} {r['price']:>6.2f} {r['MA']:>+5} {r['RSI']:>+5.1f} {r['MACD']:>+5} {r['KDJ']:>+5} {r['BOLL']:>+5} {r['TOTAL']:>+5}")

print(f"\n{'='*65}")
print("明日开盘策略:")
print("  评分>=40: 强势，开盘轻仓")
print("  评分20-40: 一般，等回调")
print("  评分<20: 观望")
print("  止损: -3%")

top = results[:3]
if top:
    print(f"\n>>> TOP3 明日重点关注:")
    for i, r in enumerate(top, 1):
        sig = "强势可买" if r['TOTAL'] >= 40 else "一般观望" if r['TOTAL'] >= 20 else "回避"
        print(f"  {i}. {r['name']} ({r['market']}{r['code']}) 评分{r['TOTAL']} {sig}  现价{r['price']:.2f}")
