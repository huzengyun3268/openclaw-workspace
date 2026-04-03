import requests

codes = ['sh600352','sz300033','sh600487','sh600893','sh601168','sh518880','bj831330','sz430046','sh600114','sh600089']
names = {'sh600352':'ZJLS','sz300033':'THS','sh600487':'HTGD','sh600893':'HFDFL','sh601168':'XBKY','sh518880':'GoldETF','bj831330':'PSBS','sz430046':'SBR','sh600114':'DMGF','sh600089':'TBDG'}

for code in codes:
    url = 'https://qt.gtimg.cn/q=' + code
    try:
        r = requests.get(url, timeout=5)
        parts = r.text.split('~')
        if len(parts) > 4:
            price = float(parts[3])
            chg_pct = parts[32] if len(parts) > 32 else '0'
            print(code + ' ' + names[code] + ': ' + str(price) + ' (' + chg_pct + '%)')
        else:
            print(code + ': parse error')
    except Exception as e:
        print(code + ': error - ' + str(e))
