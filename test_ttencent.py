import urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
url = 'https://qt.gtimg.cn/q=sh600249'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://gu.qq.com'})
r = urllib.request.urlopen(req, timeout=6)
txt = r.read().decode('gbk')
p = txt.split('"')[1].split('~')
print('Total fields:', len(p))
for i, v in enumerate(p[:60]):
    if v and v != '0' and v != '':
        print(f'p[{i}] = {v}')
