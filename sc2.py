import urllib.request
r=urllib.request.Request('https://qt.gtimg.cn/q=sh600352',headers={'User-Agent':'Mozilla/5.0','Referer':'http://gu.qq.com'})
d=urllib.request.urlopen(r,timeout=5).read().decode('gbk')
print(d[:300])
