import urllib.request
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 用东方财富K线接口查新三板
# 普适导航 bj831330 -> secid=0.831330
# 圣博润 sz430046 -> secid=0.430046
codes = [('普适导航', '0.831330'), ('圣博润', '0.430046')]
for name, secid in codes:
    url = f'http://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f57,f58,f60,f107,f169,f170,f171'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'http://quote.eastmoney.com/'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
            d = data.get('data', {})
            price = d.get('f57')  # 现价
            change = d.get('f169')  # 涨跌额
            pct = d.get('f170')  # 涨跌幅
            print(f'{name} 现价:{price} 涨跌额:{change} 涨跌幅:{pct}%')
    except Exception as e:
        print(f'{name} 失败: {e}')
