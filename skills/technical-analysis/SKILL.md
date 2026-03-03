---
name: technical-analysis
description: 专注于股票技术分析的Skill。用于通过分析资产价格的历史走势、交易量等技术指标来预测未来价格趋势。支持移动平均线、RSI、MACD、布林带、KDJ等多种技术指标计算，以及支撑阻力、趋势线、图表形态识别。适用于股票、期货、加密货币等资产的技术面分析和交易信号生成。当用户需要进行技术分析、计算技术指标、识别图表形态、生成交易信号或回测交易策略时触发此Skill。
---

# 技术分析专家 (Technical Analysis)

## 概述

本Skill专注于股票技术分析，通过计算各种技术指标、识别图表形态、分析价格走势来预测未来价格趋势，生成交易信号。

## 核心功能

### 1. 技术指标计算
支持30+种常用技术指标：

**趋势指标**
- 移动平均线 (MA, EMA, SMA)
- 指数平滑异同平均线 (MACD)
- 平均趋向指数 (ADX)
- 抛物线转向 (SAR)

**动量指标**
- 相对强弱指数 (RSI)
- 随机指标 (KDJ)
- 威廉指标 (Williams %R)
- 变动率 (ROC)

**波动率指标**
- 布林带 (Bollinger Bands)
- 平均真实波幅 (ATR)

**成交量指标**
- 成交量移动平均线 (VMA)
- 能量潮 (OBV)
- 量价趋势 (VPT)

### 2. 图表形态识别
- 支撑阻力线自动识别
- 趋势线绘制
- K线形态识别（锤子线、十字星、吞没等）
- 经典形态（头肩顶/底、双顶/底、三角形等）

### 3. 交易信号生成
- 多指标共振信号
- 金叉/死叉信号
- 超买/超卖信号
- 突破/跌破信号

### 4. 策略回测
- 基于技术指标的交易策略回测
- 收益率计算
- 风险指标评估（夏普比率、最大回撤等）

## 使用方法

### 快速计算技术指标

```bash
python scripts/technical_indicators.py \
  --symbol AAPL \
  --indicator rsi,macd,bollinger \
  --period 14 \
  --output ./output
```

### 生成交易信号

```bash
python scripts/trading_signals.py \
  --symbol AAPL \
  --strategy multi_indicator \
  --output ./signals.json
```

### 识别图表形态

```bash
python scripts/chart_patterns.py \
  --symbol AAPL \
  --pattern support_resistance,trendline \
  --output ./patterns.png
```

### 策略回测

```bash
python scripts/backtest_strategy.py \
  --symbol AAPL \
  --strategy golden_cross \
  --start 2024-01-01 \
  --end 2024-12-31 \
  --output ./backtest_result.json
```

## 技术指标详解

### 移动平均线 (MA)

**计算公式**
- SMA = (P1 + P2 + ... + Pn) / n
- EMA = P_today * k + EMA_yesterday * (1-k), k=2/(n+1)

**交易信号**
- 价格上穿MA：买入信号
- 价格下穿MA：卖出信号
- 短期MA上穿长期MA（金叉）：买入
- 短期MA下穿长期MA（死叉）：卖出

### RSI (相对强弱指数)

**计算公式**
RSI = 100 - (100 / (1 + RS))
RS = 平均上涨幅度 / 平均下跌幅度

**交易信号**
- RSI > 70：超买，考虑卖出
- RSI < 30：超卖，考虑买入
- RSI背离：价格新高但RSI未新高，可能反转

### MACD

**计算公式**
- DIF = EMA(12) - EMA(26)
- DEA = EMA(DIF, 9)
- MACD柱 = (DIF - DEA) * 2

**交易信号**
- DIF上穿DEA（金叉）：买入
- DIF下穿DEA（死叉）：卖出
- MACD柱由负转正：买入信号增强

### 布林带

**计算公式**
- 中轨 = MA(20)
- 上轨 = MA(20) + 2 * STD(20)
- 下轨 = MA(20) - 2 * STD(20)

**交易信号**
- 价格触及下轨后反弹：买入
- 价格触及上轨后回落：卖出
- 带宽收窄后扩张：大行情即将开始

## 多指标共振策略

结合多个指标提高信号准确性：

| 指标组合 | 买入条件 | 卖出条件 |
|---------|---------|---------|
| MA + RSI | 价格上穿MA且RSI<70 | 价格下穿MA且RSI>30 |
| MACD + 布林带 | MACD金叉且价格触及下轨 | MACD死叉且价格触及上轨 |
| KDJ + 成交量 | KDJ金叉且成交量放大 | KDJ死叉且成交量萎缩 |

## 注意事项

1. **技术分析的局限性**
   - 历史数据不代表未来表现
   - 在震荡市中容易产生假信号
   - 需要结合基本面分析使用

2. **参数优化**
   - 不同市场、不同品种需要调整参数
   - 避免过度优化（过拟合）

3. **风险管理**
   - 设置止损位
   - 控制单笔交易仓位
   - 分散投资

## 参考项目

本Skill参考了以下开源项目：

- [ta](https://github.com/bukosabino/ta) - Python技术分析库
- [TA-Lib](https://github.com/TA-Lib/ta-lib-python) - 专业技术分析库
- [backtrader](https://github.com/mementum/backtrader) - Python回测框架
- [MyTT](https://github.com/mpquant/MyTT) - 通达信指标移植
- [STIP](https://github.com/cn-vhql/STIP) - 交互式技术指标回测平台

## 高级功能

详细的高级功能说明请参考：

- [技术指标详解](references/indicators_reference.md)
- [策略回测指南](references/backtesting_guide.md)
- [图表形态识别](references/pattern_recognition.md)
