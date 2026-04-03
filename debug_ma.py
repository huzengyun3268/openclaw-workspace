# Debug MA for pre-screened stocks
import urllib.request, re, sys, numpy as np
sys.stdout.reconfigure(encoding='utf-8')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'

def get_market(code):
    c = str(code)
    return 'sh' if c.startswith(('6', '9')) else 'sz'

def check_ma(code, name, price):
    market = get_market(code)
    code_market = f'{market}{code}'
    try:
        url = f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={code_market},day,,,40,qfq'
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://gu.qq.com'})
        r = urllib.request.urlopen(req, timeout=8)
        txt = r.read().decode('utf-8')
        idx = txt.find('qfqday')
        if idx < 0:
            print(f'{name}: no qfqday data')
            return
        start = txt.find('[', idx)
        end = txt.find(']]', start)
        items = re.findall(r'\["([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+)"\]', txt[start:end+1])
        if len(items) < 5:
            print(f'{name}: not enough data')
            return
        
        closes = [float(it[2]) for it in items]
        opens = [float(it[1]) for it in items]
        dates = [it[0] for it in items]
        
        ma5 = np.mean(closes[-5:])
        ma10 = np.mean(closes[-10:])
        ma20 = np.mean(closes[-20:])
        
        # 近30日涨停
        had_zt = any((closes[i] - opens[i]) / opens[i] * 100 >= 9.9 for i in range(-30, 0))
        
        above_ma5 = price > ma5
        print(f'{name}: 今日收{price:.2f} 最新日K:{dates[-1]}收{closes[-1]:.2f} 开{opens[-1]:.2f} MA5={ma5:.2f} MA10={ma10:.2f} MA20={ma20:.2f} 价格>MA5:{above_ma5} 近30日涨停:{had_zt}')
    except Exception as e:
        print(f'{name}: error - {e}')

stocks = [
    ('300461', '田中精机', 23.65),
    ('600207', '安彩高科', 8.93),
    ('688428', '诺诚健华', 18.85),
    ('301130', '西点药业', 19.70),
    ('600222', '太龙药业', 8.76),
]

print('Debug: 预筛选股票的MA状态\n')
for code, name, price in stocks:
    check_ma(code, name, price)
