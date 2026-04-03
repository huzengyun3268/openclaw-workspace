import urllib.request, random, sys
sys.stdout.reconfigure(encoding='utf-8')

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
codes = {
    'sh600089': '特变电工',
    'sh600352': '浙江龙盛',
    'sz300033': '同花顺',
    'sh600487': '亨通光电',
    'sh600893': '航发动力',
    'sh601168': '西部矿业',
    'sh518880': '黄金ETF',
    'sh600114': '东睦股份',
}
for code, name in codes.items():
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': ua, 'Referer': 'https://gu.qq.com'})
        r = urllib.request.urlopen(req, timeout=6)
        txt = r.read().decode('gbk')
        p = txt.split('"')[1].split('~')
        price = float(p[3])
        prev = float(p[4])
        chg = (price - prev) / prev * 100
        print(f'{name}: {price:.2f} ({chg:+.2f}%)')
    except Exception as e:
        print(f'{name}: 查询失败')
