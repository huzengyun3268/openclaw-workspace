"""
美股+国际股市数据获取脚本
数据来源：Nasdaq API + Stooq
使用方法：python us_market_report.py
"""
import urllib.request, json, ssl, sys, re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
ctx = ssl.create_default_context()
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'

def get_nasdaq_etf(sym):
    """ETF/指数数据（Nasdaq API）"""
    try:
        url = f'https://api.nasdaq.com/api/quote/{sym}/info?assetclass=etf'
        req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            data = json.loads(r.read())
        d = data.get('data', {})
        primary = d.get('primaryData') or {}
        last = primary.get('lastSalePrice', 'N/A')
        pct = primary.get('percentageChange', 'N/A')
        return last, pct
    except:
        return None, None

def get_nasdaq_stock(sym):
    """个股数据（Nasdaq API）"""
    try:
        url = f'https://api.nasdaq.com/api/quote/{sym}/info?assetclass=stocks'
        req = urllib.request.Request(url, headers={'User-Agent': ua, 'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            data = json.loads(r.read())
        d = data.get('data', {})
        primary = d.get('primaryData') or {}
        last = primary.get('lastSalePrice', 'N/A')
        pct = primary.get('percentageChange', 'N/A')
        return last, pct
    except:
        return None, None

def get_btc():
    """比特币数据（Stooq）"""
    try:
        url = 'https://stooq.com/q/d/l/?s=btc.v&i=d'
        req = urllib.request.Request(url, headers={'User-Agent': ua})
        with urllib.request.urlopen(req, timeout=8, context=ctx) as r:
            data = r.read().decode('utf-8', errors='ignore')
        lines = [l for l in data.strip().split('\n') if l and 'Date' not in l]
        if lines:
            parts = lines[-1].split(',')
            if len(parts) >= 5:
                curr = float(parts[4])
                prev = float(lines[-2].split(',')[4]) if len(lines) >= 2 else curr
                chg = (curr - prev) / prev * 100
                return curr, chg
    except:
        pass
    return None, None

def fmt(last, pct):
    """格式化涨跌显示"""
    if last is None:
        return 'N/A', 'N/A'
    # 去掉$符号
    last = str(last).replace('$', '').strip()
    pct_str = str(pct).replace('%', '').strip()
    try:
        pct_val = float(pct_str)
        arrow = '▲' if pct_val >= 0 else '▼'
        return last, f'{arrow}{abs(pct_val):.2f}%'
    except:
        return last, pct_str

def main():
    print("=" * 50)
    print(f"🇺🇸 美国股市 | {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 50)
    
    # ETF/指数
    print("\n📊 三大指数ETF")
    for sym, name in [('SPY','S&P 500'), ('QQQ','Nasdaq100'), ('DIA','Dow30')]:
        last, pct = get_nasdaq_etf(sym)
        l, p = fmt(last, pct)
        print(f"  {name}({sym}): ${l} {p}")
    
    # 科技股
    print("\n💻 科技巨头")
    for sym, name in [('AAPL','苹果'), ('NVDA','英伟达'), ('TSLA','特斯拉'),
                       ('MSFT','微软'), ('GOOGL','谷歌'), ('AMZN','亚马逊'), ('META','Meta')]:
        last, pct = get_nasdaq_stock(sym)
        l, p = fmt(last, pct)
        print(f"  {name}({sym}): ${l} {p}")
    
    # 金融
    print("\n🏦 金融")
    for sym, name in [('JPM','摩根大通'), ('BRK.B','伯克希尔'), ('GS','高盛'), ('BAC','美国银行')]:
        last, pct = get_nasdaq_stock(sym)
        l, p = fmt(last, pct)
        print(f"  {name}({sym}): ${l} {p}")
    
    # 大宗商品ETF
    print("\n🛢️ 大宗商品")
    for sym, name in [('GLD','黄金ETF'), ('USO','原油ETF')]:
        last, pct = get_nasdaq_etf(sym)
        l, p = fmt(last, pct)
        print(f"  {name}({sym}): ${l} {p}")
    
    # 加密货币
    print("\n🪙 加密货币")
    btc, btc_chg = get_btc()
    if btc:
        a = '▲' if btc_chg >= 0 else '▼'
        print(f"  比特币(BTC): ${btc:,.0f} {a}{abs(btc_chg):.2f}%")
    
    # 其他市场
    print("\n🌏 其他主要市场")
    # 欧洲斯托克指数
    for sym, name in [('EWJ','日经225'), ('EWG','德国DAX'), ('EWU','英国FTSE')]:
        last, pct = get_nasdaq_etf(sym)
        l, p = fmt(last, pct)
        print(f"  {name}({sym}): ${l} {p}")
    
    print(f"\n⏰ 数据时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("📡 来源: Nasdaq API + Stooq")
    print("=" * 50)

if __name__ == '__main__':
    main()
