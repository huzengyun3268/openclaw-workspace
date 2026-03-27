---
name: stock-monitor-pro
description: 专业级智能股票监控预警系统 V2.1。支持收盘日报自动生成、反爬虫优化(Session级UA、多数据源冗余)、成本百分比预警、均线金叉死叉、RSI超买超卖、成交量异动监控、智能错误提醒。符合中国投资者习惯（红涨绿跌）。Use when user needs stock market monitoring, price alerts, daily reports, or automated trading notifications for A-shares and ETFs.
version: 2.1.0
author: EaveLuo
---

# Stock Monitor Pro V2 - 全功能智能投顾系统

## 核心特色

### 1. 七大预警规则

| 规则 | 触发条件 | 权重 |
|------|----------|------|
| **成本百分比** | 盈利+15% / 亏损-12% | ⭐⭐⭐ |
| **日内涨跌幅** | 个股±4% / ETF±2% / 黄金±2.5% | ⭐⭐ |
| **成交量异动** | 放量>2倍均量 / 缩量<0.5倍 | ⭐⭐ |
| **均线金叉/死叉** | MA5上穿/下穿MA10 | ⭐⭐⭐ |
| **RSI超买超卖** | RSI>70超买 / RSI<30超卖 | ⭐⭐ |
| **跳空缺口** | 向上/向下跳空>1% | ⭐⭐ |
| **动态止盈** | 盈利10%+后回撤5%/10% | ⭐⭐⭐ |

### 2. 分级预警系统
- **紧急级**: 多条件共振
- **警告级**: 2个条件触发
- **提醒级**: 单一条件触发

### 3. 中国习惯：红色=上涨 / 绿色=下跌

## 运行方式

### 后台常驻进程
```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\stock-monitor-pro\scripts
python monitor_v2.py    # 启动监控
```

## 数据源
使用 akshare + 腾讯/东方财富 多数据源冗余

## 适用场景
- A股持仓监控
- 北交所/新三板监控
- ETF监控
- 黄金/商品监控
