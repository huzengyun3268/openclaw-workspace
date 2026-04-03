import urllib.request

url = 'https://qt.gtimg.cn/q=sh600352'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as r:
    raw = r.read()

print('RAW bytes:', raw[:100])
html = raw.decode('gbk', 'ignore')
print('Decoded:', repr(html[:200]))
