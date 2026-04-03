# -*- coding: utf-8 -*-
import urllib.request, json, datetime

def get_history_em(secid, days=120):
    end = datetime.datetime.now().strftime('%Y%m%d')
    start = (datetime.datetime.now() - datetime.timedelta(days=days*2)).strftime('%Y%m%d')
    url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
           f"?secid={secid}&fields1=f1,f2,f3,f4,f5,f6"
           f"&fields2=f51,f52,f53,f54,f55,f56,f57,f58"
           f"&klt=101&fqt=1&beg={start}&end={end}&smplmt={days}&lmt={days}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.eastmoney.com/'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            klines = data.get('data', {}).get('klines', [])
            result = []
            for k in klines:
                p = k.split(',')
                if len(p) >= 6:
                    result.append([p[0], p[1], p[2], p[3], p[4], p[5]])
            return result
    except:
        return []

# 上证指数: 1.000001
data = get_history_em('1.000001', 120)
if data:
    closes = [float(d[2]) for d in data]
    highs = [float(d[3]) for d in data]
    lows = [float(d[4]) for d in data]
    
    print(f"上证指数近{data.__len__()}个交易日")
    print(f"当前收盘: {closes[-1]}")
    
    # 计算关键均线
    ma20 = sum(closes[-20:])/20
    ma60 = sum(closes[-60:])/60 if len(closes)>=60 else None
    ma120 = sum(closes[-120:])/120 if len(closes)>=120 else None
    print(f"MA20: {ma20:.2f}")
    if ma60: print(f"MA60: {ma60:.2f}")
    if ma120: print(f"MA120: {ma120:.2f}")
    
    # 近60天最低点
    min60 = min(lows[-60:])
    min60_idx = lows[-60:].index(min60)
    print(f"近60日最低: {min60} (日期: {data[-60+min60_idx][0]})")
    
    # 近120天最低点
    min120 = min(lows)
    min120_idx = lows.index(min120)
    print(f"近120日最低: {min120} (日期: {data[min120_idx][0]})")
    
    # 近期支撑
    recent_lows = sorted(set([round(l,0) for l in lows[-30:]]))[:5]
    print(f"近期低点: {recent_lows}")
    
    # RSI
    gains = [closes[i]-closes[i-1] for i in range(1,len(closes)) if closes[i]-closes[i-1]>0]
    losses = [abs(closes[i]-closes[i-1]) for i in range(1,len(closes)) if closes[i]-closes[i-1]<0]
    avg_g = sum(gains[-14:])/14 if len(gains)>=14 else 0
    avg_l = sum(losses[-14:])/14 if len(losses)>=14 else 0
    rsi = 100-(100/(1+avg_g/avg_l)) if avg_l>0 else 100
    print(f"RSI14: {rsi:.1f}")
    
    # 布林带
    n = 20
    recent = closes[-20:]
    sma = sum(recent)/20
    variance = sum((c-sma)**2 for c in recent)/20
    std = variance**0.5
    upper = sma+2*std
    lower = sma-2*std
    current = closes[-1]
    boll_pos = (current-lower)/(upper-lower)*100
    print(f"BOLL: 上轨={upper:.1f} 中轨={sma:.1f} 下轨={lower:.1f}")
    print(f"现价所处位置: {boll_pos:.1f}%")
else:
    print("获取数据失败")
