# -*- coding: utf-8 -*-
"""
老胡专属持仓监控脚本
只监控他的持仓，多数据源，实时期权预警
"""
import urllib.request
import json
import time
import random
import os
from datetime import datetime

# ============ 老胡持仓配置 ============
HOLDINGS = {
    # 主账户
    'sh600352': {'name': '浙江龙盛',  'cost': 16.948,  'stop': 12.0,  'shares': 76700,  'account': '主账户'},
    'sz300033': {'name': '同花顺',    'cost': 423.488, 'stop': 280.0, 'shares': 1200,   'account': '主账户'},
    'sh600487': {'name': '亨通光电',  'cost': 43.210,  'stop': 38.0,  'shares': 3000,   'account': '主账户'},
    'sh600893': {'name': '航发动力',  'cost': 49.184,  'stop': 42.0,  'shares': 9000,   'account': '主账户'},
    'sh601168': {'name': '西部矿业',  'cost': 26.169,  'stop': 22.0,  'shares': 11000,  'account': '主账户'},
    'sh518880': {'name': '黄金ETF',  'cost': 9.868,   'stop': 0,    'shares': 24000,  'account': '主账户'},
    'bj831330': {'name': '普适导航',  'cost': 20.361,  'stop': 18.0,  'shares': 7370,   'account': '主账户'},
    'sz430046': {'name': '圣博润',    'cost': 0.478,   'stop': 0,    'shares': 10334,  'account': '主账户'},
    # 老婆账户
    'sh600114': {'name': '东睦股份',  'cost': 31.176,  'stop': 25.0,  'shares': 11100,  'account': '老婆账户'},
    # 两融账户
    'sh600089': {'name': '特变电工',  'cost': 24.765,  'stop': 25.0,  'shares': 52300,  'account': '两融账户'},
}

UA_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

def fetch_tencent(codes):
    """腾讯行情接口"""
    url = f'https://qt.gtimg.cn/q={",".join(codes)}'
    req = urllib.request.Request(url, headers={
        'User-Agent': random.choice(UA_LIST),
        'Referer': 'https://gu.qq.com'
    })
    r = urllib.request.urlopen(req, timeout=8)
    txt = r.read().decode('gbk')
    results = {}
    for line in txt.strip().split(';'):
        if 'v_' not in line:
            continue
        key = line.split('=')[0].split('_')[-1].strip()
        p = line.split('"')[1].split('~')
        if len(p) > 35:
            results[key] = {
                'price': float(p[3]) if p[3] else 0,
                'prev_close': float(p[4]) if p[4] else 0,
                'open': float(p[5]) if p[5] else 0,
                'high': float(p[33]) if p[33] else 0,
                'low': float(p[34]) if p[34] else 0,
            }
    return results

def fetch_sina(codes):
    """新浪行情接口"""
    url = f'https://hq.sinajs.cn/list={",".join(codes)}'
    req = urllib.request.Request(url, headers={
        'User-Agent': random.choice(UA_LIST),
        'Referer': 'https://finance.sina.com.cn'
    })
    r = urllib.request.urlopen(req, timeout=8)
    txt = r.read().decode('gb18030')
    results = {}
    for line in txt.strip().split(';'):
        if 'hq_str_' not in line:
            continue
        key = line.split('=')[0].split('_')[-1].strip()
        p = line.split('"')[1].split(',')
        if len(p) > 30 and float(p[3]) > 0:
            results[key] = {
                'price': float(p[3]),
                'prev_close': float(p[2]),
                'open': float(p[1]),
                'high': float(p[4]),
                'low': float(p[5]),
            }
    return results

def get_price(code):
    """获取单个股票价格，尝试腾讯->新浪"""
    c = code[2:]  # 去掉sh/sz/bj前缀
    # 腾讯
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': random.choice(UA_LIST), 'Referer': 'https://gu.qq.com'})
        r = urllib.request.urlopen(req, timeout=6)
        txt = r.read().decode('gbk')
        p = txt.split('"')[1].split('~')
        if len(p) > 35:
            return float(p[3]) if p[3] else None
    except:
        pass
    # 新浪
    try:
        url = f'https://hq.sinajs.cn/list={code}'
        req = urllib.request.Request(url, headers={'User-Agent': random.choice(UA_LIST), 'Referer': 'https://finance.sina.com.cn'})
        r = urllib.request.urlopen(req, timeout=6)
        txt = r.read().decode('gb18030')
        p = txt.split('"')[1].split(',')
        if len(p) > 30:
            return float(p[3]) if p[3] else None
    except:
        pass
    return None

def format_report():
    """生成持仓报告"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = [f"\n{'='*50}"]
    lines.append(f"  老胡持仓报告  {now}")
    lines.append(f"{'='*50}")
    
    total_pnl = 0
    alerts = []
    
    by_account = {'主账户': [], '老婆账户': [], '两融账户': []}
    
    for code, info in HOLDINGS.items():
        price = get_price(code)
        if price is None:
            continue
        
        cost = info['cost']
        shares = info['shares']
        stop = info['stop']
        name = info['name']
        account = info['account']
        
        pnl = (price - cost) * shares
        pnl_pct = (price - cost) / cost * 100
        prev = None  # 用None表示无法获取
        
        change_pct = 0
        try:
            c = code[2:]
            url = f'https://qt.gtimg.cn/q={code}'
            req = urllib.request.Request(url, headers={'User-Agent': random.choice(UA_LIST), 'Referer': 'https://gu.qq.com'})
            r = urllib.request.urlopen(req, timeout=6)
            txt = r.read().decode('gbk')
            p = txt.split('"')[1].split('~')
            if len(p) > 4 and float(p[4]) > 0:
                change_pct = (float(p[3]) - float(p[4])) / float(p[4]) * 100
        except:
            pass
        
        total_pnl += pnl
        
        # 预警检查
        if stop > 0 and price <= stop:
            alerts.append(f"  *** 止损触发 [{name}] 现价{price:.2f} <= 止损{stop}")
        
        sign = '+' if pnl >= 0 else ''
        stop_info = f' 止损{stop}' if stop > 0 else ''
        pnl_str = f"{sign}{pnl:.0f}元 ({sign}{pnl_pct:.1f}%)"
        chg_str = f"{'+' if change_pct >= 0 else ''}{change_pct:.2f}%"
        
        by_account[account].append(
            f"  {name:<8} {price:>7.2f} {chg_str:>7}  成本{cost:>7.2f}  {pnl_str:>15}  {stop_info}"
        )
    
    for account, rows in by_account.items():
        if rows:
            lines.append(f"\n【{account}】")
            lines.append(f"  {'名称':<8} {'现价':>7} {'涨跌':>7}  {'成本':>7}  {'盈亏':>15}  {'备注'}")
            lines.append('  ' + '-'*60)
            lines.extend(rows)
    
    lines.append(f"\n{'='*50}")
    total_sign = '+' if total_pnl >= 0 else ''
    lines.append(f"  浮动盈亏合计: {total_sign}{total_pnl:.0f}元")
    lines.append(f"{'='*50}")
    
    if alerts:
        lines.append("\n  === 预警 ===")
        lines.extend(alerts)
    
    return '\n'.join(lines)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # 单次运行
        print(format_report())
    else:
        # 持续监控
        print("老胡持仓监控已启动 (Ctrl+C停止)")
        while True:
            try:
                print(format_report())
                time.sleep(60)  # 每60秒刷新
            except KeyboardInterrupt:
                print("\n已停止")
                break
            except Exception as e:
                print(f"错误: {e}")
                time.sleep(30)
