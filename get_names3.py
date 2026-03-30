# -*- coding: utf-8 -*-
import urllib.request, json

# 用腾讯接口获取
codes = ['sz002471', 'sh688011', 'sz002491']
for code in codes:
    url = f"https://qt.gtimg.cn/q={code}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            raw = r.read()
            # 强制用latin1读字节，再手动decode gbk
            raw_bytes = raw
            text = raw_bytes.decode('gbk', errors='replace')
            parts = text.split('~')
            if len(parts) > 4:
                print(f"{code}: name={parts[1]}, price={parts[3]}, change={parts[32]}")
    except Exception as e:
        print(f"{code} ERROR: {e}")
