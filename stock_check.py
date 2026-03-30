import urllib.request

codes = ['sh600352','sh600893','sz300033','sh601168','bj831330','sh600487','sh688295','sz430046','sh600114','sh600089']
names = {
    'sh600352':'浙江龙盛','sh600893':'航发动力','sz300033':'同花顺',
    'sh601168':'西部矿业','bj831330':'普适导航','sh600487':'亨通光电',
    'sh688295':'中复神鹰','sz430046':'圣博润','sh600114':'东睦股份','sh600089':'特变电工'
}
prices = {
    'sh600352':13.2,'sh600893':48.3,'sz300033':301,'sh601168':25.4,
    'bj831330':20.0,'sh600487':53.85,'sh688295':55.0,'sz430046':0.29,
    'sh600114':31.681,'sh600089':24.765
}
stops = {
    'sh600352':12.0,'sh600893':42.0,'sz300033':280.0,'sh601168':22.0,
    'bj831330':18.0,'sh600487':38.0,'sz430046':None,'sh600114':25.0,'sh600089':25.0
}
costs = {
    'sh600352':16.52,'sh600893':49.184,'sz300033':423.488,'sh601168':26.169,
    'bj831330':20.361,'sh600487':45.47,'sh688295':56.85,'sz430046':0.478,
    'sh600114':31.681,'sh600089':24.765
}
amounts = {
    'sh600352':86700,'sh600893':9000,'sz300033':1200,'sh601168':11000,
    'bj831330':7370,'sh600487':4000,'sh688295':3000,'sz430046':10334,
    'sh600114':4900,'sh600089':52300
}

codes_str = ','.join(codes)
url = f'http://qt.gtimg.cn/q={codes_str}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')
lines = data.strip().split('\n')

print("=== 持仓监控 2026-03-30 15:30 ===\n")
for line in lines:
    if '="~' in line:
        continue
    if '=""' in line:
        continue
    try:
        code = line.split('="')[0].replace('v_','')
        if code not in names:
            continue
        parts = line.split('~')
        price = float(parts[3]) if len(parts)>3 else 0
        pct = parts[31] if len(parts)>31 else '0'
        name = names.get(code, code)
        cost = costs.get(code, 0)
        stop = stops.get(code)
        amt = amounts.get(code, 0)
        profit = (price - cost) * amt
        pct_profit = (price/cost - 1)*100 if cost > 0 else 0

        warn = ''
        if stop and price <= stop:
            warn = ' ⚠️ 触及止损！'
        elif stop and price < stop * 1.05:
            warn = ' ⚠️ 接近止损'

        print(f"{name}({code}): {price}元 涨跌额:{parts[31] if len(parts)>31 else '0'} 涨幅:{pct}%")
        print(f"  成本:{cost} | 盈亏:{profit:+.0f}元({pct_profit:+.1f}%) | 止损:{stop}{warn}")
        print()
    except Exception as e:
        pass
