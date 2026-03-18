---
name: stock-monitor
description: 股票实时监控技能。用于实时监控股票价格、涨跌幅、成交量、资金流向等动态数据。主要功能包括：(1) 实时价格监控 (2) 涨跌幅预警 (3) 成交量异动监控 (4) 资金流向监控 (5) 自选股监控。当用户需要监控股票动态时使用此技能。
---

# 股票实时监控

## 功能

1. **价格监控** - 实时获取股票现价
2. **涨跌幅监控** - 监控涨跌停、异动
3. **成交量监控** - 监控放量缩量
4. **资金流向** - 监控大单进出
5. **自选股监控** - 同时监控多只股票

## 数据来源

使用东方财富API：
```
https://push2.eastmoney.com/api/qt/stock/get?secid=0.300033&fields=f43,f44,f45,f46,f47,f48,f57,f58,f169,f170
```

字段说明：
- f43: 最新价
- f44: 最高价
- f45: 最低价
- f46: 开盘价
- f47: 成交量(手)
- f48: 成交额(元)
- f169: 涨跌额
- f170: 涨跌幅
- f57: 股票代码
- f58: 股票名称

## 使用方式

```python
import requests

def get_stock_price(code):
    # 沪市: 0.6xxxxx, 深市: 0.0xxxxx, 创业板: 0.3xxxxx
    if code.startswith('6'):
        secid = f"0.{code}"
    elif code.startswith('0') or code.startswith('3'):
        if code.startswith('3'):
            secid = f"0.{code}"
        else:
            secid = f"1.{code}"
    else:
        secid = f"0.{code}"
    
    url = f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f169,f170"
    resp = requests.get(url)
    data = resp.json()['data']
    return {
        'name': data['f58'],
        'price': data['f43'] / 1000,  # 价格需要除以1000
        'change': data['f169'] / 1000,
        'change_pct': data['f170'] / 1000,
        'volume': data['f47']
    }
```

## 监控示例

| 股票 | 代码 | 实时价格 | 涨跌幅 |
|------|------|----------|--------|
| 同花顺 | 300033 | 32.91元 | -2.46% |
| 贵州茅台 | 600519 | - | - |
| 宁德时代 | 300750 | - | - |

## 注意事项

- 东方财富API更新频率约5-10秒
- 仅供个人学习使用，勿过度频繁请求
- 投资有风险，决策需谨慎
