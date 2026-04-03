import requests
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

r = requests.get('http://qt.gtimg.cn/q=sh000001', timeout=5)
r.encoding = 'gbk'
raw = r.text.strip()
print('Raw:', repr(raw[:100]))
if '=' in raw:
    data = raw.split('=')[1].strip('"')
    parts = data.split('~')
    print('Total parts:', len(parts))
    print('Name:', repr(parts[1]))
    print('Price:', parts[3])
    print('Prev close:', parts[4])
    chg = (float(parts[3]) - float(parts[4])) / float(parts[4]) * 100
    print('Change:', f'{chg:+.2f}%')
