# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://finance.sina.com.cn/",
}

# ============ 指数行情 - 新浪 ============
print("=== 指数行情 ===")
try:
    codes = "sh000001,sz399001,sz399006,sh000688,sh000300"
    url = f"https://hq.sinajs.cn/list={codes}"
    r = requests.get(url, headers=headers, timeout=15)
    r.encoding = 'gbk'
    lines = r.text.strip().split('\n')
    names_map = {
        "sh000001": "上证指数", "sz399001": "深证成指", "sz399006": "创业板指",
        "sh000688": "科创50", "sh000300": "沪深300"
    }
    for line in lines:
        parts = line.split('=')
        if len(parts) < 2:
            continue
        code_part = parts[0].split('_')[-1]
        data_str = parts[1].strip().strip('"')
        if not data_str:
            continue
        fields = data_str.split(',')
        if len(fields) < 10:
            continue
        name = names_map.get(code_part, code_part)
        price = fields[1]
        chg = fields[2]
        pct = fields[3]
        print(f"{name}: {price} ({pct}%)")
except Exception as e:
    print(f"指数: {e}")

# ============ 涨跌停统计 - 新浪 ============
print("\n=== 涨跌统计 ===")
try:
    # 涨停
    url_zt = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
    params_zt = {"page": 1, "num": 5, "sort": "changepercent", "asc": 0, "node": "hs_a", "symbol": "", "_s_r_a": "page"}
    r_zt = requests.get(url_zt, params=params_zt, headers=headers, timeout=15)
    r_zt.encoding = 'utf-8'
    # 总数用东财
    url_em = "http://push2.eastmoney.com/api/qt/clist/get"
    params_em = {
        "pn": 1, "pz": 1, "po": 1, "np": 1,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": 2, "invt": 2, "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23",
        "fields": "f12",
    }
    r_em = requests.get(url_em, params=params_em, headers=headers, timeout=15)
    total = r_em.json().get("data",{}).get("total",0)
    
    params_zt2 = dict(params_em)
    params_zt2["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=9.9"
    r_zt2 = requests.get(url_em, params=params_zt2, headers=headers, timeout=15)
    zt_count = r_zt2.json().get("data",{}).get("total",0)
    
    params_dt2 = dict(params_em)
    params_dt2["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=-9.9"
    r_dt2 = requests.get(url_em, params=params_dt2, headers=headers, timeout=15)
    dt_count = r_dt2.json().get("data",{}).get("total",0)
    
    params_up2 = dict(params_em)
    params_up2["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=0"
    r_up2 = requests.get(url_em, params=params_up2, headers=headers, timeout=15)
    up_count = r_up2.json().get("data",{}).get("total",0)
    
    params_dn2 = dict(params_em)
    params_dn2["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=0"
    r_dn2 = requests.get(url_em, params=params_dn2, headers=headers, timeout=15)
    dn_count = r_dn2.json().get("data",{}).get("total",0)
    
    print(f"上涨: {up_count}  下跌: {dn_count}  涨停: {zt_count}  跌停: {dt_count}  总: {total}")
except Exception as e:
    print(f"涨跌停: {e}")

# ============ 持仓个股 - 新浪 ============
print("\n=== 持仓个股 ===")
stocks = [
    ("浙江龙盛", "sh600352"),
    ("同花顺", "sz300033"),
    ("华工科技", "sz000988"),
    ("中复神鹰", "sh688295"),
    ("亨通光电", "sh600487"),
    ("高澜股份", "sz300499"),
    ("西部矿业", "sh601168"),
    ("航发动力", "sh600893"),
    ("亿能电力", "bj920046"),
    ("东睦股份", "sh600114"),
    ("南网数字", "sz301638"),
]
codes_str = ",".join([s[1] for s in stocks])
try:
    url2 = f"https://hq.sinajs.cn/list={codes_str}"
    r2 = requests.get(url2, headers=headers, timeout=15)
    r2.encoding = 'gbk'
    lines2 = r2.text.strip().split('\n')
    
    for line, (name, code) in zip(lines2, stocks):
        parts = line.split('=')
        if len(parts) < 2:
            print(f"{name}({code}): 数据获取失败")
            continue
        data_str = parts[1].strip().strip('"').strip(';')
        if not data_str:
            print(f"{name}({code}): 无数据")
            continue
        fields = data_str.split(',')
        if len(fields) < 32:
            print(f"{name}({code}): 字段不足 {len(fields)}")
            continue
        
        price = fields[3]    # 当前价
        yest = fields[2]       # 昨收
        open_p = fields[1]    # 开盘
        chg = fields[3]      # 当前价(重算)
        pct = fields[3]       # 涨跌幅
        
        try:
            price_f = float(fields[3])
            yest_f = float(fields[2])
            open_f = float(fields[1])
            vol_f = float(fields[8])    # 成交量(手)
            amount_f = float(fields[9]) # 成交额(元)
            high_f = float(fields[4])   # 最高
            low_f = float(fields[5])    # 最低
            
            pct_f = (price_f - yest_f) / yest_f * 100 if yest_f > 0 else 0
            chg_f = price_f - yest_f
            
            direction = ""
            if open_f > 0 and yest_f > 0:
                diff = open_f - yest_f
                if abs(diff) < 0.01:
                    direction = "平开"
                elif diff > 0:
                    direction = f"高开{abs(diff):.2f}"
                else:
                    direction = f"低开{abs(diff):.2f}"
            
            vol_str = f"{vol_f/10000:.1f}万手" if vol_f >= 10000 else f"{vol_f/100:.0f}百手"
            amount_str = f"{amount_f/1e8:.2f}亿" if amount_f >= 1e8 else f"{amount_f/1e4:.0f}万"
            
            print(f"{name}: 现价{price_f:.2f} ({pct_f:+.2f}%) 开:{open_f:.2f} {direction} 量:{vol_str} 额:{amount_str} 高:{high_f:.2f} 低:{low_f:.2f}")
        except Exception as e2:
            print(f"{name}: 解析失败 {e2}")
except Exception as e:
    print(f"持仓: {e}")

import datetime
print(f"\n采集时间 {datetime.datetime.now().strftime('%H:%M:%S')}")
