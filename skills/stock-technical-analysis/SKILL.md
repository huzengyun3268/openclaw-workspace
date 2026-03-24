---
name: stock-technical-analysis
description: A股持仓技术分析技能。综合MA、RSI、MACD、KDJ、BOLL等指标，给出量化评分和操作建议。当用户要求分析股票、给出操作建议、或需要技术分析报告时使用此技能。支持持仓股票全面技术分析、个股深度技术分析、大盘技术分析。
---

# A股技术分析技能

## 核心脚本

- 批量分析：`C:\tools\stock_analysis\ta_batch.js`（持仓全面分析，12只股票）
- 单股分析：`C:\tools\stock_analysis\ta_batch.js <股票代码>`
- Python引擎：`C:\tools\stock_analysis\stock_ta.py`（技术指标计算）
- Python路径：`C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe`

## 技术指标

- **均线MA**：MA5/MA10/MA20/MA60，多头/空头排列判断
- **RSI**：6日/14日相对强弱指数，超买(>65)超卖(<35)
- **MACD**：DIF/DEA金叉死叉，零轴上下判断
- **KDJ**：K/D/J值，极度超买(>90)极度超卖(<10)
- **BOLL布林带**：价格与上下轨关系
- **综合评分**：-10到+10分量化体系

## 评分体系

| 评分 | 信号 | 颜色 |
|------|------|------|
| ≥4分 | 🟢强烈买入 | 绿色 |
| 2~4分 | 🟡谨慎买入 | 黄色 |
| 0~2分 | 🔵持有观察 | 蓝色 |
| -2~0分 | 🟡谨慎持有 | 黄色 |
| <-2分 | 🔴建议卖出 | 红色 |

## 使用方式

### 持仓全面分析
```bash
node C:\tools\stock_analysis\ta_batch.js
```

### 单股深度分析
```bash
node C:\tools\stock_analysis\ta_batch.js <股票代码>
# 示例
node C:\tools\stock_analysis\ta_batch.js 600352
```

## 注意事项

- 数据来源：Sina Finance API（60日K线）
- 实时价格：EastMoney API
- 技术分析基于60日历史K线，不是当日实时分时数据
- 分析仅供参考，不构成投资建议
