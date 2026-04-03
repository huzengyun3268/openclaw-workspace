# -*- coding: utf-8 -*-
"""
A股量化选股助手 - 2026年4月1日关注股票筛选
评分 = 技术面x35 + 资金面x25 + 消息面x20 + 基本面x20
"""

import requests
import json
import time
import sys

# 强制UTF-8输出
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 股票池（名称, 代码）  去重
STOCK_POOL_ORIG = [
    # 能源
    ("特变电工", "sh600089"),
    ("中国石油", "sh601857"),
    ("中国石化", "sh600028"),
    ("中国海油", "sh600938"),
    ("广汇能源", "sh600256"),
    # 军工
    ("航发动力", "sh600893"),
    ("中航沈飞", "sh600760"),
    ("中航西飞", "sh000768"),
    ("航亚科技", "sh688510"),
    ("北方导航", "sh600435"),
    # 黄金
    ("山金国际", "sz000975"),
    ("中金黄金", "sh600489"),
    ("赤峰黄金", "sh600988"),
    ("银泰黄金", "sz000975"),
    ("湖南黄金", "sz002155"),
    # 科技/AI
    ("浪潮信息", "sz000977"),
    ("中科曙光", "sh603019"),
    ("寒武纪", "sh688256"),
    ("海光信息", "sh688041"),
    # 电网/电力
    ("国电南瑞", "sh600406"),
    ("许继电气", "sz000400"),
    ("平高电气", "sh600312"),
    ("思源电气", "sz002028"),
    # 大盘权重
    ("贵州茅台", "sh600519"),
    ("宁德时代", "sz300750"),
    ("比亚迪", "sz002594"),
    ("中国平安", "sh601318"),
    # 化工
    ("浙江龙盛", "sh600352"),
    ("万华化学", "sh600309"),
    ("华鲁恒升", "sh600426"),
    # 矿业
    ("紫金矿业", "sh601899"),
    ("洛阳钼业", "sh603993"),
    ("西部矿业", "sh601168"),
    # 光模块/通信
    ("通鼎互联", "sz002491"),
    ("中天科技", "sh600522"),
    ("亨通光电", "sh600487"),
    ("烽火通信", "sh600498"),
    # 消费/医疗
    ("迈瑞医疗", "sz300760"),
    ("药明康德", "sh603259"),
    ("爱尔眼科", "sz300015"),
    # 补充
    ("同花顺", "sz300033"),
    ("中复神鹰", "sh688295"),
]

# 去重
seen = set()
STOCK_POOL = []
for name, code in STOCK_POOL_ORIG:
    if code not in seen:
        seen.add(code)
        STOCK_POOL.append((name, code))

print(f"股票池共 {len(STOCK_POOL)} 只\n")


def fetch_tencent_realtime(codes_list):
    """获取实时行情 - codes_list是纯代码字符串列表"""
    url = f"https://qt.gtimg.cn/q={','.join(codes_list)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.qq.com/"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        resp.encoding = 'gbk'
        text = resp.text.strip()
        results = {}
        for line in text.split('\n'):
            idx_eq = line.find('=')
            if idx_eq < 0:
                continue
            after_eq = line[idx_eq+1:]
            idx_tilde = after_eq.find('~')
            if idx_tilde < 0:
                continue
            data_str = after_eq[idx_tilde+1:].rstrip('";')
            fields = data_str.split('~')
            # 提取代码
            key_part = line[:idx_eq]  # 如 v_sh600089
            if key_part.startswith('v_'):
                code = key_part[2:]
            else:
                code = key_part
            results[code] = fields
        return results
    except Exception as e:
        print(f"[API错误] {e}")
        return {}


def fetch_history_kline(code, count=35):
    """获取日K线数据"""
    if code.startswith('sh') or code.startswith('sz') or code.startswith('bj'):
        sym = code[2:]
        stype = code[:2]
    else:
        sym = code
        stype = 'sh'
    
    url = "https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
    params = {"symbol": f"{stype}{sym}", "scale": "240", "ma": "no", "datalen": str(count)}
    
    try:
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        return data if isinstance(data, list) else []
    except:
        return []


def safe_float(val, default=0.0):
    try:
        return float(val)
    except:
        return default


def calc_ma(prices):
    if len(prices) < 20:
        return None, None, None
    ma5 = sum(prices[-5:]) / 5
    ma10 = sum(prices[-10:]) / 10
    ma20 = sum(prices[-20:]) / 20
    return ma5, ma10, ma20


def calc_rsi(prices, period=14):
    if len(prices) < period + 2:
        return None
    gains, losses = [], []
    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))


def calc_macd_diff(prices, fast=12, slow=26):
    if len(prices) < slow + 1:
        return None
    def ema(data, period):
        k = 2 / (period + 1)
        ema_val = data[0]
        for d in data[1:]:
            ema_val = d * k + ema_val * (1 - k)
        return ema_val
    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    return ema_fast - ema_slow


def calc_boll_mid(prices, period=20):
    if len(prices) < period:
        return None
    recent = prices[-period:]
    return sum(recent) / period


def calc_scores(name, code, fields):
    """计算四个维度得分
    
    腾讯字段映射（0-indexed）:
    f[0]=股票名  f[1]=代码  f[2]=现价  f[3]=昨收  f[4]=今开
    f[5]=成交量(手)  f[6]=成交额(元)  f[7]=外盘成交量
    f[8]=最低  f[30]=涨跌额  f[31]=涨跌幅(%)  f[32]=最高
    f[35]=成交量  f[36]=成交额(万元)  f[37]=换手率(%)
    f[38]=市盈率(PE)  f[43]=总市值(亿元)  f[44]=流通市值(亿元)
    f[45]=市净率(PB)
    """
    scores = {"技术面": 0, "资金面": 0, "消息面": 0, "基本面": 0}
    
    if not fields or len(fields) < 45:
        return scores, {}
    
    try:
        price = safe_float(fields[2])      # 现价
        prev_close = safe_float(fields[3])  # 昨收
        turnover = safe_float(fields[37])  # 换手率(%)
        pe = safe_float(fields[38])        # PE
        pb = safe_float(fields[45])        # PB
        flow_cap = safe_float(fields[44]) # 流通市值（亿元）
        total_cap = safe_float(fields[43]) # 总市值（亿元）
        change_pct = safe_float(fields[31]) # 涨跌幅（%）
        high = safe_float(fields[32])      # 最高
        low = safe_float(fields[8])        # 最低
        outer_vol = safe_float(fields[7])  # 外盘成交量
        
        # 内盘估算：成交量-外盘
        total_vol = safe_float(fields[5])
        inner_vol = max(total_vol - outer_vol, 0)
        
        info = {
            "price": price, "prev_close": prev_close,
            "turnover": turnover, "pe": pe, "pb": pb,
            "flow_cap": flow_cap, "total_cap": total_cap,
            "change_pct": change_pct, "high": high, "low": low,
            "outer_vol": outer_vol, "inner_vol": inner_vol,
            "total_vol": total_vol,
        }
    except Exception as e:
        return scores, {}
    
    if price <= 0:
        return scores, {}
    
    # ====== 技术面（满分35分）======
    kline = fetch_history_kline(code, 35)
    prices = []
    for k in kline:
        try:
            prices.append(float(k.get('close', 0)))
        except:
            pass
    
    if len(prices) >= 20:
        ma5, ma10, ma20 = calc_ma(prices)
        rsi = calc_rsi(prices)
        diff = calc_macd_diff(prices)
        boll_mid = calc_boll_mid(prices)
        
        if ma5 and ma10 and ma20:
            if ma5 > ma10 > ma20:
                scores["技术面"] += 10
        
        if rsi is not None:
            if 40 <= rsi <= 70:
                scores["技术面"] += 8
            elif rsi > 70:
                scores["技术面"] += 3
            elif rsi < 30:
                scores["技术面"] += 5
        
        if diff is not None:
            # DIFF > 0 表示在零轴上方，强势
            if diff > 0:
                scores["技术面"] += 8
        
        if boll_mid and price > boll_mid:
            scores["技术面"] += 5
        
        if 1.0 <= abs(change_pct) <= 8.0 and change_pct > 0:
            scores["技术面"] += 4
        elif change_pct > 8.0:
            scores["技术面"] += 2
    
    # ====== 资金面（满分25分）======
    # 量比估算：用换手率相对判断
    vol_ratio_est = turnover / 2.0  # 粗估（实际量比需要前5日均值）
    if vol_ratio_est > 1.5:
        scores["资金面"] += 8
    
    if 3.0 <= turnover <= 15.0:
        scores["资金面"] += 8
    elif turnover > 15.0:
        scores["资金面"] += 3
    elif turnover > 0.5:
        scores["资金面"] += 4
    
    # 外盘 > 内盘（主动买盘强）
    if outer_vol > inner_vol and inner_vol > 0:
        ratio = outer_vol / inner_vol
        if ratio > 1.2:
            scores["资金面"] += 6
        elif ratio > 1.0:
            scores["资金面"] += 3
    
    # 主力净流入（粗估）
    if outer_vol > inner_vol * 1.1:
        scores["资金面"] += 3
    
    # ====== 消息面（满分20分）======
    energy_stocks = ["特变电工", "中国石油", "中国石化", "中国海油", "广汇能源"]
    gold_stocks = ["山金国际", "中金黄金", "赤峰黄金", "银泰黄金", "湖南黄金"]
    military_stocks = ["航发动力", "中航沈飞", "中航西飞", "航亚科技", "北方导航"]
    ai_stocks = ["浪潮信息", "中科曙光", "寒武纪", "海光信息"]
    power_stocks = ["国电南瑞", "许继电气", "平高电气", "思源电气", 
                    "通鼎互联", "中天科技", "亨通光电", "烽火通信"]
    
    if name in energy_stocks:
        scores["消息面"] += 5
    if name in gold_stocks:
        scores["消息面"] += 5
    if name in military_stocks:
        scores["消息面"] += 5
    
    # 电力/电网（宽松政策受益）
    if name in power_stocks:
        scores["消息面"] += 5
    
    # AI/科技主线
    if name in ai_stocks:
        scores["消息面"] += 5
    
    # 季报预期（PE合理）
    if 5 < pe < 50 and pe > 0:
        scores["消息面"] += 3
    
    # 科创/创业板创新属性
    if code.startswith('sh688') or code.startswith('sz300') or code.startswith('bj'):
        scores["消息面"] += 2
    
    # ====== 基本面（满分20分）======
    if 10 <= pe <= 40:
        scores["基本面"] += 8
    elif 0 < pe < 10:
        scores["基本面"] += 5
    elif pe > 40:
        scores["基本面"] += 2
    
    if 50 <= flow_cap <= 500:
        scores["基本面"] += 6
    elif 20 <= flow_cap < 50:
        scores["基本面"] += 4
    elif 500 < flow_cap <= 2000:
        scores["基本面"] += 3
    
    if 0 < pb < 5:
        scores["基本面"] += 4
    elif pb == 0:
        scores["基本面"] += 1
    
    if pe > 0 and pe < 60:
        scores["基本面"] += 2
    
    return scores, info


def get_suggestion(total):
    if total >= 75:
        return "强烈关注"
    elif total >= 60:
        return "适当关注"
    elif total >= 45:
        return "谨慎关注"
    else:
        return "暂不关注"


# ========== 主程序 ==========
print("=" * 80)
print("开始扫描股票池...")
print("=" * 80)

BATCH_SIZE = 20
all_results = []

for i in range(0, len(STOCK_POOL), BATCH_SIZE):
    batch = STOCK_POOL[i:i+BATCH_SIZE]
    codes = [c for _, c in batch]
    
    raw_data = fetch_tencent_realtime(codes)
    time.sleep(0.4)
    
    for name, code in batch:
        fields = raw_data.get(code, [])
        scores, info = calc_scores(name, code, fields)
        total = sum(scores.values())
        
        if info.get("price", 0) > 0:
            all_results.append({
                "name": name, "code": code,
                "price": info.get("price", 0),
                "change_pct": info.get("change_pct", 0),
                "pe": info.get("pe", 0),
                "turnover": info.get("turnover", 0),
                "flow_cap": info.get("flow_cap", 0),
                "scores": scores, "total": total, "info": info
            })
        else:
            # 打印无法获取数据的股票
            print(f"  [无数据] {name}({code})")
    
    print(f"  已处理 {min(i+BATCH_SIZE, len(STOCK_POOL))}/{len(STOCK_POOL)} 只...")

all_results.sort(key=lambda x: x["total"], reverse=True)

# ========== 输出TOP10 ==========
print("\n" + "=" * 90)
print("【2026年4月1日 A股量化选股 TOP10】")
print("评分公式：技术面x35 + 资金面x25 + 消息面x20 + 基本面x20")
print("=" * 90)

print(f"\n{'排名':<4} {'股票':<8} {'代码':<10} {'现价':>8} {'涨幅':>8} {'技术':>4} {'资金':>4} {'消息':>4} {'基本':>4} {'总分':>5}  建议")
print("-" * 90)

for i, r in enumerate(all_results[:10], 1):
    s = r["scores"]
    total = r["total"]
    cp = r["change_pct"]
    change_str = f"{cp:+.2f}%"
    price_str = f"¥{r['price']:.2f}"
    suggest = get_suggestion(total)
    
    print(f"{i:<4} {r['name']:<8} {r['code']:<10} {price_str:>8} {change_str:>8} "
          f"{s['技术面']:>4} {s['资金面']:>4} {s['消息面']:>4} {s['基本面']:>4} {total:>5}  {suggest}")

print("-" * 90)

# ========== 最终推荐 ==========
print("\n" + "=" * 60)
print("【最终推荐 - 明天最值得关注的3只】")
print("=" * 60)

top3 = all_results[:3]
for i, r in enumerate(top3, 1):
    s = r["scores"]
    info = r["info"]
    price = info.get('price', 0)
    stop_loss = price * 0.95
    
    print(f"\n第{i}名：{r['name']}（{r['code']}）")
    print(f"   现价：¥{price:.2f}  今日涨幅：{r['change_pct']:+.2f}%")
    print(f"   综合总分：{r['total']}分")
    print(f"   各维度：技术面{s['技术面']}/35 | 资金面{s['资金面']}/25 | 消息面{s['消息面']}/20 | 基本面{s['基本面']}/20")
    print(f"   PE：{r['pe']:.1f}  换手率：{r['turnover']:.2f}%  流通市值：{r['flow_cap']:.1f}亿")
    
    if r['change_pct'] > 5:
        timing = "今日涨幅较大，建议尾盘观察"
        stop = price * 0.93
    elif r['change_pct'] > 0:
        timing = "温和上涨，明日开盘竞价量价配合好可介入"
        stop = price * 0.95
    else:
        timing = "小幅调整，明日低开企稳可考虑"
        stop = price * 0.94
    
    print(f"   操作：{timing}")
    print(f"   止损位：¥{stop:.2f}（约-5%）")

print("\n" + "=" * 60)
print("【操作注意事项】")
print("  A股T+1制度：当天买的股票第二天才能卖出！")
print("  以上仅为量化模型筛选结果，不构成投资建议")
print("  请结合大盘环境、市场情绪综合判断")
print("=" * 60)

# ========== 完整明细 ==========
print("\n\n【完整候选池得分明细】")
print(f"{'股票':<8} {'代码':<10} {'现价':>8} {'涨幅':>8} {'技术':>4} {'资金':>4} {'消息':>4} {'基本':>4} {'总分':>5}")
print("-" * 70)
for r in all_results:
    s = r["scores"]
    print(f"{r['name']:<8} {r['code']:<10} ¥{r['price']:>6.2f} {r['change_pct']:>+6.2f}% "
          f"{s['技术面']:>4} {s['资金面']:>4} {s['消息面']:>4} {s['基本面']:>4} {r['total']:>5}")

# 保存
with open("stock_scan_results.txt", "w", encoding="utf-8") as f:
    f.write("A股量化选股扫描结果 - 眼镜\n")
    f.write("扫描时间: 2026-03-31 下午\n\n")
    for i, r in enumerate(all_results[:10], 1):
        s = r["scores"]
        f.write(f"{i}. {r['name']}({r['code']}) 总分:{r['total']} 技术:{s['技术面']} 资金:{s['资金面']} 消息:{s['消息面']} 基本:{s['基本面']}\n")

print("\n结果已保存至 stock_scan_results.txt")
