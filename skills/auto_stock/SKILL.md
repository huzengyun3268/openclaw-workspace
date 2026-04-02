---
name: auto_stock
description: 龙虾全自动炒股技能 v1.0 - 激进短线交易系统。选股+持仓监控+盘前盘后报告+风控提醒。资金基准80万，单票上限30%，止损4%，止盈8-12-15%。
version: 1.0.0
---

# 龙虾全自动炒股技能 v1.0

## 核心规则

| 规则 | 参数 |
|------|------|
| 资金基准 | 80万 |
| 单票上限 | 30% = 24万 |
| 总仓上限 | 70% = 56万 |
| 止损线 | -4%（触发立即走，不犹豫）|
| 止盈线 | +8%减半 / +12%再减 / +15%全走 |
| 持有期限 | 1-3天（超时不赚强制走）|
| 炸板规则 | 涨停炸板先出一半 |
| 连续止损 | 2次后当天禁止开新仓 |

---

## 快捷命令

### 选股（盘中用）
```
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_trade.py 选股
```

### 持仓分析
```
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_trade.py 持仓
```

### 今日热点
```
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_trade.py 热点
```

### 风控规则
```
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_trade.py 风控
```

### 激进短线专项选股
```
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_term_select.py 强势
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_term_select.py 突破
python C:/Users/Administrator/.openclaw/workspace/skills/auto_stock/scripts/short_term_select.py 尾盘
```

---

## 自动定时任务（已设置）

| 任务 | 时间 | 内容 |
|------|------|------|
| 盘前报告 | 工作日 9:25 | 热点方向+重点关注股+操作提醒 |
| 持仓监控 | 工作日 9-11点 每15分钟 | 持仓状态+预警 |
| 集合竞价 | 工作日 9:15/9:20/9:25 | 竞价异动监控 |
| 持仓监控 | 工作日 13-15点 每15分钟 | 持仓状态+预警 |
| 盘后复盘 | 工作日 15:10 | 持仓分析+明日计划 |

---

## 持仓配置

持仓每次变化后，编辑以下文件更新：
- `short_trade.py` → POSITIONS 列表
- `evening_report.py` → POSITIONS 列表

格式：
```python
{"name":"股票名", "code":"sh600xxx", "shares":数量, "cost":成本价, "buy_date":"2026-04-02", "note":"短线"}
```

---

## 核心交易哲学

> **"不管哪个方向，总有弱时，我们做强时行情"**
> 只做强势，不做弱势。弱转强时跟进，强转弱时离场。

## 选股条件说明

| 模式 | 条件 | 适合场景 |
|------|------|---------|
| 强势 | 涨幅5-10%+换手>5%+市值<300亿 | 主线明确时 |
| 突破 | 涨幅3-8%+换手>8%+突破20日新高 | 突破确认时 |
| 尾盘 | 涨幅2-6%+换手>5%+量比>1.5 | 尾盘套利 |
| 热点 | 涨幅5-15%+换手>10%+非一字板 | 热点追涨 |
| 回踩 | 涨幅1-5%+近5日跌>5%缩量 | 低吸反弹 |

---

## 风险提醒

- 不碰ST/利空/问题股
- 大盘冰点（跌幅>1%）不开新仓
- 高位妖股不追（连续3板以上）
- 止损是命，不情绪化扛单
