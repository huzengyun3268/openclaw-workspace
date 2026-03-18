---
name: technical-analysis
description: 股票技术分析技能。用于分析股票的技术指标、形态、K线组合等。主要功能包括：(1) 常用技术指标计算（MA、MACD、KDJ、RSI、BOLL等）(2) K线形态识别（锤子线、吞没、十字星等）(3) 趋势分析 (4) 支撑位阻力位计算 (5) 量价关系分析。当用户需要技术分析时使用此技能。
---

# 股票技术分析

## 常用技术指标

### 1. 移动平均线 (MA)

```python
import pandas as pd

def calc_ma(df, period):
    return df['close'].rolling(window=period).mean()

# 常用周期
MA5 = calc_ma(df, 5)   # 短期均线
MA10 = calc_ma(df, 10)  # 中期均线
MA20 = calc_ma(df, 20)  # 长期均线
MA60 = calc_ma(df, 60)  # 半年线
```

### 2. MACD

```python
def calc_macd(df, fast=12, slow=26, signal=9):
    ema12 = df['close'].ewm(span=fast).mean()
    ema26 = df['close'].ewm(span=slow).mean()
    diff = ema12 - ema26
    dea = diff.ewm(span=signal).mean()
    macd = (diff - dea) * 2
    return diff, dea, macd
```

### 3. KDJ随机指标

```python
def calc_kdj(df, n=9, m1=3, m2=3):
    low_n = df['low'].rolling(window=n).min()
    high_n = df['high'].rolling(window=n).max()
    
    rsv = (df['close'] - low_n) / (high_n - low_n) * 100
    k = rsv.ewm(com=m1-1).mean()
    d = k.ewm(com=m2-1).mean()
    j = 3 * k - 2 * d
    return k, d, j
```

### 4. RSI相对强弱

```python
def calc_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
```

### 5. 布林带 (BOLL)

```python
def calc_boll(df, period=20, std_dev=2):
    middle = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower
```

## K线形态识别

### 常见反转形态

| 形态 | 信号 | 说明 |
|------|------|------|
| 锤子线 | 买入 | 下影线长，实体小 |
| 上吊线 | 卖出 | 上影线长，实体小 |
| 吞没 | 买入/卖出 | 阴阳包线 |
| 十字星 | 谨慎 | 多空平衡 |
| 早晨之星 | 买入 | 底部三连阳 |
| 黄昏之星 | 卖出 | 顶部三连阴 |

### 形态识别代码

```python
def is_hammer(candle):
    """锤子线"""
    body = abs(candle['close'] - candle['open'])
    lower_shadow = min(candle['open'], candle['close']) - candle['low']
    upper_shadow = candle['high'] - max(candle['open'], candle['close'])
    
    return (lower_shadow > body * 2 and 
            upper_shadow < body * 0.5)

def is_doji(candle):
    """十字星"""
    body = abs(candle['close'] - candle['open'])
    total_range = candle['high'] - candle['low']
    return body < total_range * 0.1
```

## 支撑位与阻力位

```python
def find_support_resistance(prices, window=20):
    """寻找支撑位和阻力位"""
    highs = prices['high'].rolling(window).max()
    lows = prices['low'].rolling(window).min()
    return highs, lows
```

## 量价关系

| 现象 | 信号 |
|------|------|
| 价涨量增 | 强势上涨 |
| 价涨量缩 | 上涨乏力 |
| 价跌量增 | 恐慌抛售 |
| 价跌量缩 | 底部信号 |

## 使用建议

1. **多指标结合** - MACD + KDJ + RSI 综合判断
2. **顺势而为** - 上涨趋势中逢低买入
3. **量价配合** - 放量突破更可靠
4. **设止损位** - 技术分析+止损=风险控制

## 注意事项

- 技术分析仅供参考
- 市场有风险，投资需谨慎
- 不同行情适用不同指标
- 建议结合基本面分析
