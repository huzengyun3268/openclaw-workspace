# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings('ignore')
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://finance.eastmoney.com/",
    "Accept": "*/*",
}

# ============ 指数行情 ============
print("=== 指数行情 ===")
try:
    url = "http://push2.eastmoney.com/api/qt/ulist.np/get"
    params = {
        "fltt": 2, "invt": 2,
        "fields": "f12,f14,f2,f3,f4",
        "secids": "1.000001,0.399001,0.399006,1.000688,1.000300",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    d = r.json()
    names = {"1.000001":"上证指数","0.399001":"深证成指","0.399006":"创业板指","1.000688":"科创50","1.000300":"沪深300"}
    items = d.get("data",{}).get("diff",{})
    for secid, item in items.items():
        name = names.get(secid, item.get("f14",""))
        price = item.get("f2",0)
        chg = item.get("f3",0)
        print(f"{name}: {price} ({chg:+.2f}%)")
except Exception as e:
    print(f"指数: {e}")

# ============ 涨跌停统计 ============
print("\n=== 涨跌统计 ===")
try:
    # 涨停数
    url_zt = "http://push2.eastmoney.com/api/qt/clist/get"
    params_zt = {
        "pn": 1, "pz": 1,
        "po": 1, "np": 1,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": 2, "invt": 2,
        "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=9.9",
        "fields": "f12",
    }
    r_zt = requests.get(url_zt, params=params_zt, headers=headers, timeout=15)
    zt_count = r_zt.json().get("data",{}).get("total",0)
    
    params_dt = {
        "pn": 1, "pz": 1,
        "po": 1, "np": 1,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "fltt": 2, "invt": 2,
        "fid": "f3",
        "fs": "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=-9.9",
        "fields": "f12",
    }
    r_dt = requests.get(url_dt, params=params_dt, headers=headers, timeout=15)
    dt_count = r_dt.json().get("data",{}).get("total",0)
    
    # 总数
    params_total = dict(params_zt)
    params_total["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23"
    params_total["fid"] = "f3"
    del params_total["fid"]
    r_total = requests.get(url_zt, params=params_total, headers=headers, timeout=15)
    total = r_total.json().get("data",{}).get("total",0)
    
    # 上涨下跌
    params_up = dict(params_zt)
    params_up["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.gt=0"
    r_up = requests.get(url_zt, params=params_up, headers=headers, timeout=15)
    up_count = r_up.json().get("data",{}).get("total",0)
    
    params_dn = dict(params_zt)
    params_dn["fs"] = "m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&f3.lt=0"
    r_dn = requests.get(url_zt, params=params_dn, headers=headers, timeout=15)
    dn_count = r_dn.json().get("data",{}).get("total",0)
    
    print(f"上涨: {up_count}  下跌: {dn_count}  涨停: {zt_count}  跌停: {dt_count}  总: {total}")
except Exception as e:
    print(f"涨跌停统计: {e}")

# ============ 持仓个股 ============
print("\n=== 持仓个股 ===")
stocks = [
    ("浙江龙盛", "600352"),
    ("同花顺", "300033"),
    ("华工科技", "000988"),
    ("中复神鹰", "688295"),
    ("亨通光电", "600487"),
    ("高澜股份", "300499"),
    ("西部矿业", "601168"),
    ("航发动力", "600893"),
    ("亿能电力", "920046"),
    ("东睦股份", "600114"),
    ("南网数字", "301638"),
]
secids_list = []
for name, code in stocks:
    if code.startswith("6"):
        secids_list.append("1."+code)
    else:
        secids_list.append("0."+code)
secids_str = ",".join(secids_list)

try:
    url4 = "http://push2.eastmoney.com/api/qt/ulist.np/get"
    params4 = {
        "fltt": 2, "invt": 2,
        "fields": "f12,f14,f2,f3,f4,f5,f6,f15,f16,f17,f18",
        "secids": secids_str,
        "ut": "b2884a393a59ad64002292a3e90d46a5",
    }
    r4 = requests.get(url4, params=params4, headers=headers, timeout=15)
    d4 = r4.json()
    items = d4.get("data",{}).get("diff",{})
    
    for secid, item in items.items():
        name = item.get("f14","")
        price = item.get("f2",0)
        chg = item.get("f3",0)
        vol = item.get("f5",0)
        amount = item.get("f6",0)
        high = item.get("f15",0)
        low = item.get("f16",0)
        open_p = item.get("f17",0)
        prev_close = item.get("f18",0)
        
        direction = ""
        if open_p > 0 and prev_close > 0:
            diff = open_p - prev_close
            if abs(diff) < 0.01:
                direction = "平开"
            elif diff > 0:
                direction = f"高开{abs(diff):.2f}"
            else:
                direction = f"低开{abs(diff):.2f}"
        
        if vol >= 1e6:
            vol_str = f"{vol/1e6:.1f}万手"
        elif vol >= 1e3:
            vol_str = f"{vol/1e3:.0f}百手"
        else:
            vol_str = f"{vol:.0f}手"
        
        if amount >= 1e8:
            amount_str = f"{amount/1e8:.2f}亿"
        elif amount >= 1e4:
            amount_str = f"{amount/1e4:.0f}万"
        else:
            amount_str = f"{amount:.0f}"
        
        print(f"{name}: 现价{price} ({chg:+.2f}%) 开:{open_p} {direction} 量:{vol_str} 额:{amount_str} 今日高:{high} 低:{low}")
except Exception as e:
    print(f"持仓: {e}")
    import traceback
    traceback.print_exc()

import datetime
print(f"\n采集时间 {datetime.datetime.now().strftime('%H:%M:%S')}")
