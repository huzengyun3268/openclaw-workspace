import requests
url = 'https://qt.gtimg.cn/q=sh600089,sh601857,sz000975'
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com/'}
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = 'gbk'
lines = resp.text.strip().split('\n')
for line in lines:
    idx_eq = line.find('=')
    if idx_eq < 0:
        continue
    after_eq = line[idx_eq+1:]
    idx_tilde = after_eq.find('~')
    data_str = after_eq[idx_tilde+1:].rstrip('";')
    fields = data_str.split('~')
    print(f'Total fields: {len(fields)}')
    for i in range(40, min(len(fields), 87)):
        print(f'  f[{i}] = {fields[i]}')
    print()
    break
