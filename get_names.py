# -*- coding: utf-8 -*-
import urllib.request, json

# 腾讯接口直接获取名称
codes = ['sz002471', 'sh688011', 'sz002491', 'sz002176', 'sz300016', 'sh600216']
for code in codes:
    url = f"https://qt.gtimg.cn/q={code}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            raw = r.read()
            # 尝试gbk
            try:
                text = raw.decode('gbk', errors='replace')
            except:
                text = raw.decode('utf-8', errors='replace')
            parts = text.split('~')
            if len(parts) > 3:
                name = parts[1]
                price = parts[3]
                change = parts[32] if len(parts) > 32 else ''
                print(f"{code} 名称: {name}  现价: {price}  涨跌: {change}%")
    except Exception as e:
        print(f"{code} 失败: {e}")
