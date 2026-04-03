import requests

url = 'https://qt.gtimg.cn/q=sh600089,sh601857,sz000975'
headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.qq.com/'}
resp = requests.get(url, headers=headers, timeout=10)
resp.encoding = 'gbk'
text = resp.text.strip()
lines = text.split('\n')
print(f"Total lines: {len(lines)}")
for line in lines:
    if len(line) < 20:
        continue
    # Find the ~ after the quote
    # Format: v_sh600089="1~field~...
    idx_eq = line.find('=')
    if idx_eq < 0:
        continue
    after_eq = line[idx_eq+1:]  # starts with "
    # Find the ~ after the opening quote
    idx_tilde = after_eq.find('~')
    if idx_tilde < 0:
        print(f"No tilde found in: {line[:50]}")
        continue
    # Data starts after the ~
    data_str = after_eq[idx_tilde+1:].rstrip('";')
    fields = data_str.split('~')
    print(f"Fields: {len(fields)}")
    for i, f in enumerate(fields[:50]):
        print(f"  f[{i}] = {f}")
    break
