# -*- coding: utf-8 -*-
import requests
import json

# 用新浪财经接口
codes = ['sh600352', 'sz300033', 'sz000988', 'sh688295', 'sh600487', 'sz300499', 'sh601168', 'sh600893', 'bj920046']

def get_stock_data(sina_code):
    url = f"http://hq.sinajs.cn/list={sina_code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://finance.sina.com.cn/'
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        r.encoding = 'gbk'
        text = r.text.strip()
        # 格式: var hq_str_sh600352="名称,今日开盘价,昨日收盘价,当前价格,今日最高价,今日最低价,..."
        content = text.split('"')[1] if '"' in text else ''
        if content:
            parts = content.split(',')
            if len(parts) >= 32:
                name = parts[0]
                open_p = parts[1]  # 今开
                close_p = parts[2]  # 昨收
                price = parts[3]   # 当前
                high = parts[4]    # 最高
                low = parts[5]     # 最低
                vol = parts[8]     # 成交量(手)
                amount = parts[9]  # 成交额(万)
                if price.replace('.','').replace('-','').isdigit():
                    pct = round((float(price) - float(close_p)) / float(close_p) * 100, 2) if float(close_p) != 0 else 0
                    change = round(float(price) - float(close_p), 2)
                    return f"{name}: 现价={price} 今开={open_p} 涨跌={change}({pct}%) 最高={high} 最低={low}"
                else:
                    return f"{sina_code}: 无有效数据"
            else:
                return f"{sina_code}: 数据格式异常"
        else:
            return f"{sina_code}: 无数据"
    except Exception as e:
        return f"{sina_code}: 失败 {e}"

for code in codes:
    print(get_stock_data(code))
