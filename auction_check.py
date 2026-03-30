import requests
stocks = ['sh600352','sh600893','sz300033','sh601168','bj920046','sz430046','sh600487','sh688295','bj831330']
def get_rt(code):
    try:
        r = requests.get('https://qt.gtimg.cn/q=' + code, timeout=5)
        fields = r.text.split('=')[1].strip('"; \n')
        f = fields.split('~')
        return {'name': f[1], 'price': float(f[3]), 'pct': float(f[32]), 'vol': f[36]}
    except Exception as e:
        return None
for s in stocks:
    d = get_rt(s)
    if d:
        print(f"{d['name']}({s[2:]}): {d['price']}  {'%.2f' % d['pct']}% 竞价量={d['vol']}")
    else:
        print(f"{s} 获取失败")
