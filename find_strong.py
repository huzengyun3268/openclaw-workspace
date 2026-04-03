import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# 今日强势股扫描：从东方财富获取涨幅榜
url = 'https://push2.eastmoney.com/api/qt/clist/get'
params = {
    'cb': 'jQuery',
    'fid': 'f3',
    'po': '1',
    'pz': '50',
    'pn': '1',
    'np': '1',
    'fltt': '2',
    'invt': '2',
    'fid': 'f3',
    'fs': 'm:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23',
    'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152',
    '_': '1'
}
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.eastmoney.com/'}
try:
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    text = resp.text
    # 去掉jQuery包装
    if text.startswith('jQuery'):
        text = text[7:]
    import json
    data = json.loads(text)
    stocks = data.get('data', {}).get('diff', [])
    print('=== 今日涨幅榜前30（沪市主板+科创板）===')
    for i, s in enumerate(stocks[:30], 1):
        name = s.get('f14', '')
        code = s.get('f12', '')
        price = s.get('f2', '')
        change = s.get('f3', '')
        vol = s.get('f6', '')
        amount = s.get('f10', '')  # 万元
        high = s.get('f15', '')
        open_p = s.get('f17', '')
        print(f'{i:2}. {name}({code}) 现价{price} 涨幅{change}% 今开{open_p} 最高{high} 成交额{amount}万')
except Exception as e:
    print('Error:', e)
    # fallback: 手动查询几只
    codes = 'sh600487,sh601168,sh600893,sh600256,sh600522,sz002491,sh600519,sh601288'
    r = requests.get('https://qt.gtimg.cn/q=' + codes, headers={'User-Agent':'Mozilla/5.0'})
    r.encoding = 'gbk'
    for line in r.text.strip().split('\n'):
        eq = line.find('=')
        if eq < 0: continue
        raw = line[eq+1:]
        t = raw.find('~')
        if t < 0: continue
        data = raw[t+1:].strip('"').strip(';')
        f = data.split('~')
        if len(f) < 32: continue
        code = f[1]
        price = f[2]
        prev = f[3]
        chg = f[31]
        high = f[32] if len(f) > 32 else '?'
        vol = f[5]
        print(f'{code}: 现价{price} 涨跌幅{chg}% 最高{high} 成交量{vol}')
