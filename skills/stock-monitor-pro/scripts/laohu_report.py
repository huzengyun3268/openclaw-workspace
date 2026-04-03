# -*- coding: utf-8 -*-
"""持仓监控脚本 - 输出到文件供定时任务读取"""
import urllib.request
import json
import time
import random
from datetime import datetime

HOLDINGS = {
    'sh600352': {'name': '浙江龙盛',  'cost': 16.948,  'stop': 12.0,  'shares': 76700,  'account': '主账户'},
    'sz300033': {'name': '同花顺',    'cost': 423.488, 'stop': 280.0, 'shares': 1200,   'account': '主账户'},
    'sh600487': {'name': '亨通光电',  'cost': 43.210,  'stop': 38.0,  'shares': 3000,   'account': '主账户'},
    'sh600893': {'name': '航发动力',  'cost': 49.184,  'stop': 42.0,  'shares': 9000,   'account': '主账户'},
    'sh601168': {'name': '西部矿业',  'cost': 26.169,  'stop': 22.0,  'shares': 11000,  'account': '主账户'},
    'sh518880': {'name': '黄金ETF',  'cost': 9.868,   'stop': 0,    'shares': 24000,  'account': '主账户'},
    'sh600114': {'name': '东睦股份',  'cost': 31.176,  'stop': 25.0,  'shares': 11100,  'account': '老婆账户'},
    'sh600089': {'name': '特变电工',  'cost': 24.765,  'stop': 25.0,  'shares': 52300,  'account': '两融账户'},
}

UA_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

def get_price(code):
    for src in ['qt.gtimg.cn', 'hq.sinajs.cn']:
        try:
            if src == 'qt.gtimg.cn':
                url = f'https://{src}/q={code}'
                req = urllib.request.Request(url, headers={'User-Agent': random.choice(UA_LIST), 'Referer': 'https://gu.qq.com'})
                r = urllib.request.urlopen(req, timeout=6)
                txt = r.read().decode('gbk')
                p = txt.split('"')[1].split('~')
                if len(p) > 35:
                    return float(p[3]) if p[3] else None, float(p[4]) if p[4] else None
            else:
                url = f'https://{src}/list={code}'
                req = urllib.request.Request(url, headers={'User-Agent': random.choice(UA_LIST), 'Referer': 'https://finance.sina.com.cn'})
                r = urllib.request.urlopen(req, timeout=6)
                txt = r.read().decode('gb18030')
                p = txt.split('"')[1].split(',')
                if len(p) > 30:
                    return float(p[3]) if p[3] else None, float(p[2]) if p[2] else None
        except:
            continue
    return None, None

def build_report():
    now = datetime.now().strftime('%m-%d %H:%M')
    lines = [f"**持仓实况 {now}**"]
    
    total_pnl = 0
    alerts = []
    by_account = {'主账户': [], '老婆账户': [], '两融账户': []}
    
    for code, info in HOLDINGS.items():
        price, prev = get_price(code)
        if price is None:
            continue
        
        cost = info['cost']
        shares = info['shares']
        stop = info['stop']
        name = info['name']
        account = info['account']
        
        pnl = (price - cost) * shares
        pnl_pct = (price - cost) / cost * 100
        pnl_sign = '+' if pnl >= 0 else ''
        
        change_pct = 0
        if prev and prev > 0:
            change_pct = (price - prev) / prev * 100
        chg_sign = '+' if change_pct >= 0 else ''
        
        total_pnl += pnl
        
        if stop > 0 and price <= stop:
            alerts.append(f"*** 止损 [{name}] {price:.2f} <= {stop}")
        
        stop_info = f' 止损{stop}' if stop > 0 else ''
        line = f"{name} {price:.2f} ({chg_sign}{change_pct:.2f}%) | {pnl_sign}{pnl:.0f}元{stop_info}"
        by_account[account].append(line)
    
    total_sign = '+' if total_pnl >= 0 else ''
    lines.append(f"合计 {total_sign}{total_pnl:.0f}元\n")
    
    for account, rows in by_account.items():
        if rows:
            lines.append(f"【{account}】")
            lines.extend(rows)
            lines.append("")
    
    if alerts:
        lines.append("**预警：**")
        lines.extend(alerts)
    
    return '\n'.join(lines)

if __name__ == '__main__':
    # 开盘时间检查（北京时间）
    now = datetime.now()
    weekday = now.weekday()
    hour, minute = now.hour, now.minute
    time_val = hour * 100 + minute
    
    market_open = (weekday < 5) and ((930 <= time_val <= 1130) or (1300 <= time_val <= 1500))
    
    report = build_report()
    
    # 输出到文件
    out_file = r'C:\Users\Administrator\.openclaw\workspace\laohu_report.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
