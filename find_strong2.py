import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# 成交额前100扫描
url = 'https://push2.eastmoney.com/api/qt/clist/get'
params = {
    'fid': 'f6',
    'po': '0',
    'pz': '100',
    'pn': '1',
    'np': '1',
    'fltt': '2',
    'invt': '2',
    'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23',
    'fields': 'f2,f3,f4,f5,f6,f7,f8,f10,f12,f14,f15,f16,f17,f18',
    '_': '1'
}
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.eastmoney.com/'}
try:
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    text = resp.text
    if text.startswith('jQuery'):
        text = text[7:]
    import json
    data = json.loads(text)
    stocks = data.get('data', {}).get('diff', [])
    print('=== 今日成交额前30强（按成交额排序）===')
    # sort by amount
    sorted_stocks = sorted(stocks, key=lambda x: float(x.get('f6', 0) or 0), reverse=True)
    for i, s in enumerate(sorted_stocks[:30], 1):
        name = s.get('f14', '')
        code = str(s.get('f12', ''))
        price = s.get('f2', '')
        chg = s.get('f3', '')
        amount = s.get('f10', '')  # 万元
        high = s.get('f15', '')
        open_p = s.get('f17', '')
        turnover = s.get('f8', '')  # 换手率%
        print(f'{i:2}. {name}(sh{code}或sz{code}) 现价{price} 涨幅{chg}% 换手{turnover}% 成交额{amount}万 最高{high}')
except Exception as e:
    print('Error:', e)
