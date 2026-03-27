import urllib.request

url = 'https://hq.sinajs.cn/list=sh600352'
req = urllib.request.Request(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://finance.sina.com.cn'
})
r = urllib.request.urlopen(req, timeout=10)
data = r.read().decode('gbk')
print(data)
