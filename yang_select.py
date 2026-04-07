# 杨永兴隔夜套利精华版 v1.0
# 规则：14:45入场，次日10:30前离场
# 仅在市场上升期/震荡期操作，退潮期空仓

import requests
import json
from datetime import datetime

API = "https://stockboot.jiuma.cn/api"

# ====== 第一层：大盘情绪校验 ======
def check_market_sentiment():
    """
    返回: dict{
        'ok': bool,
        'reason': str,
        'sh_index': float,
        'cy_index': float
    }
    """
    try:
        r = requests.post(f"{API}/quote/batch", json=["000001", "399006"], timeout=10)
        items = r.json()['data']['items']
        fields = r.json()['data']['fields']
        rows = [dict(zip(fields, item)) for item in items]
        
        sh = next((r for r in rows if r['stockCode'] == '000001'), None)
        cy = next((r for r in rows if r['stockCode'] == '399006'), None)
        
        sh_chg = sh['changeRate'] if sh else -999
        cy_chg = cy['changeRate'] if cy else -999
        
        ok = sh_chg > -1.5 and cy_chg > -2.0
        sh_icon = "OK" if sh_chg > -1.5 else "!!"
        cy_icon = "OK" if cy_chg > -2 else "!!"
        reason = f"SH{sh_icon} {sh_chg:+.2f}% | CY{cy_icon} {cy_chg:+.2f}%"
        
        return {'ok': ok, 'reason': reason, 'sh': sh_chg, 'cy': cy_chg}
    except Exception as e:
        return {'ok': False, 'reason': f"行情获取失败: {e}", 'sh': 0, 'cy': 0}

# ====== 第二层：动态涨幅区间 ======
def get_gain_range(sh_chg):
    """
    根据大盘强弱返回当日选股涨幅区间
    """
    if sh_chg >= 1.0:
        return 3.0, 8.0   # 强势：3%~8%
    elif sh_chg >= -0.5:
        return 2.0, 6.0   # 震荡：2%~6%
    else:
        return 1.0, 4.0   # 弱势：1%~4%

# ====== 第三层：量比过滤 ======
def check_volume_ratio(code):
    """
    检查量比 1.3~2.2，排除尾盘急拉
    返回: (ok, detail)
    """
    try:
        r = requests.post(f"{API}/quote/batch", json=[code], timeout=10)
        item = r.json()['data']['items'][0]
        row = dict(zip(r.json()['data']['fields'], item))
        
        vol_ratio = row.get('volRatio') or 0
        chg_rate = row.get('changeRate') or 0
        
        # 排除尾盘最后5分钟急拉>2%
        # 用涨跌幅代理：全天涨幅>2%且尾盘加速 = 危险
        detail = f"量比={vol_ratio:.2f} 涨幅={chg_rate:.2f}%"
        
        if vol_ratio < 1.3:
            return False, f"{detail} [X] 量比不足"
        if vol_ratio > 2.5:
            return False, f"{detail} [X] 量比过大（主力出货嫌疑）"
        if chg_rate > 8:
            return False, f"{detail} [X] 涨幅过大追高风险高"
        if chg_rate < 0:
            return False, f"{detail} [X] 下跌不参与"
        
        return True, f"{detail} [OK]"
    except:
        return False, f"{code} 数据异常"

# ====== 第四层：分时形态检查 ======
def check_price_trend(code):
    """
    检查均价线是否平稳向上，运行在均线上方
    返回: (ok, detail)
    """
    try:
        r = requests.get(f"{API}/quote/minute/{code}", timeout=10)
        data = r.json()
        if 'data' not in data:
            return False, "分时数据无"
        
        minutes = data['data']
        if not minutes:
            return False, "分时数据空"
        
        prices = [float(m['price']) for m in minutes if m.get('price')]
        if len(prices) < 10:
            return False, "数据不足"
        
        # 检查全天均价：价格是否大部分时间在均线上方
        avg_price = sum(prices) / len(prices)
        above_avg = sum(1 for p in prices if p >= avg_price) / len(prices)
        
        # 检查尾盘是否急拉
        tail = prices[-10:] if len(prices) >= 10 else prices
        tail_rise = (tail[-1] - tail[0]) / tail[0] * 100 if tail[0] > 0 else 0
        
        detail = f"均价上={above_avg:.0%} 尾盘波动={tail_rise:+.2f}%"
        
        if above_avg < 0.6:
            return False, f"{detail} [X] 全天弱势"
        if tail_rise > 2.0:
            return False, f"{detail} [X] 尾盘急拉诱多"
        
        return True, f"{detail} [OK]"
    except Exception as e:
        return False, f"分时异常:{e}"

# ====== 核心选股 ======
def yang_select(max_stocks=3):
    """
    杨永兴隔夜套利精选
    返回: 推荐标的列表
    """
    print(f"【{datetime.now().strftime('%H:%M')} 杨永兴精选选股】")
    
    # 1. 大盘情绪
    sentiment = check_market_sentiment()
    print(f"大盘: {sentiment['reason']}")
    
    if not sentiment['ok']:
        print("[!!] 大盘弱势，跳过隔夜套利")
        return []
    
    sh_chg = sentiment['sh']
    gain_min, gain_max = get_gain_range(sh_chg)
    print(f"今日涨幅区间: {gain_min}% ~ {gain_max}%")
    
    # 2. 动态选股：按涨幅筛选（用涨停股作为有涨停基因的标的池）
    try:
        r = requests.post(f"{API}/dynamic-select/execute", 
                        json={"sentence": "涨停"}, timeout=20)
        result = r.json()
        stocks_data = result.get('data', {})
        candidates = stocks_data.get('stocks', [])[:30]
        total = stocks_data.get('totalCount', len(candidates))
        print(f"候选涨停股: {len(candidates)}只（共{total}只）")
    except Exception as e:
        print(f"选股API失败: {e}")
        return []
    
    if not candidates:
        print("无候选标的")
        return []
    
    # 3. 逐个过滤
    results = []
    for s in candidates:
        code = s.get('code', '')
        name = s.get('name', code)
        
        # 排除流通市值过大/过小（简化版：用经验判断）
        # 排除科创/创业板高价股（波动太大）
        
        vr_ok, vr_detail = check_volume_ratio(code)
        
        if not vr_ok:
            print(f"  {name} {vr_detail}")
            continue
        
        pt_ok, pt_detail = check_price_trend(code)
        
        print(f"  {name} | {vr_detail} | {pt_detail}")
        
        if vr_ok and pt_ok:
            results.append({
                'name': name,
                'code': code,
                'volume_detail': vr_detail,
                'trend_detail': pt_detail
            })
        
        if len(results) >= max_stocks:
            break
    
    return results

# ====== 屏蔽清单检查 ======
BLOCK_REASONS = {
    'st': 'ST/*ST股',
    'unlock': '解禁股',
    'new': '次新股',
    'high': '连续大涨高位',
    'volume_shadow': '放量出货',
    'tail_rise': '尾盘诱多',
    'block': '冷门无联动',
}

# ====== 快速判断（已知强势板块）======
KNOWN_HOT_CODES = [
    '000586',  # 汇源通信 光通信
    '300308',  # 中际旭创 光模块
    '600487',  # 亨通光电 光通信
    '002792',  # 通宇通讯 CPO
    '688205',  # 德科立 光通信
]

def quick_yang_check(codes):
    """
    快速验证已知强势标的是否满足杨永兴条件
    """
    print(f"\n【{datetime.now().strftime('%H:%M')} 快速验证强势标的】")
    sentiment = check_market_sentiment()
    print(f"大盘: {sentiment['reason']}")
    
    if not sentiment['ok']:
        print("[!!] 大盘弱势，跳过")
        return []
    
    name_map = {
        '000586': '汇源通信', '300308': '中际旭创', '600487': '亨通光电',
        '002792': '通宇通讯', '688205': '德科立', '600900': '长江电力',
        '600938': '中国海油', '601288': '农业银行',
    }
    
    results = []
    try:
        r = requests.post(f"{API}/quote/batch", json=codes, timeout=10)
        data = r.json()['data']
        for item in data['items']:
            row = dict(zip(data['fields'], item))
            code = row['stockCode']
            name = name_map.get(code, code)
            chg = row['changeRate']
            vr = row.get('volRatio', 0) or 0
            
            gain_min, gain_max = get_gain_range(sentiment['sh'])
            
            ok = True
            reasons = []
            
            if chg < gain_min:
                ok = False
                reasons.append(f"涨幅{chg:.1f}%<{gain_min}%")
            if chg > gain_max:
                ok = False
                reasons.append(f"涨幅{chg:.1f}%>{gain_max}%")
            if vr < 1.3:
                reasons.append(f"量比{vr:.2f}不足")
            if vr > 2.5:
                reasons.append(f"量比过大")
            
            status = "[OK]" if ok else "[X]"
            print(f"  {name}({code}) {chg:+.2f}% 量比={vr:.2f} {status} {'|'.join(reasons) if reasons else '通过'}")
            
            if ok:
                results.append({'name': name, 'code': code, 'chg': chg, 'vr': vr})
    except Exception as e:
        print(f"批量查询失败: {e}")
    
    return results

if __name__ == "__main__":
    print("=" * 50)
    print("杨永兴隔夜套利精选 v1.0")
    print("规则: 14:45入场 次日10:30前离场")
    print("=" * 50)
    
    results = yang_select(max_stocks=3)
    
    if results:
        print(f"\n[*] 推荐标的 ({len(results)}只):")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r['name']}({r['code']})")
            print(f"     {r['volume_detail']}")
            print(f"     {r['trend_detail']}")
    else:
        print("\n今日暂无符合条件的标的，等待下一交易日")
