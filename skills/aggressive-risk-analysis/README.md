# aggressive-risk-analysis

激进风险分析Skill - 专注于股市投资的激进风险管理

## 功能

- **Kelly Criterion仓位计算**: 最优仓位比例计算，支持分数Kelly策略
- **反马丁格尔(Anti-Martingale)**: 盈利加仓、亏损减仓的动态仓位管理
- **风险平价(Risk Parity)**: 基于风险贡献的资产配置
- **波动率目标(Volatility Targeting)**: 根据市场波动动态调整仓位
- **最大回撤控制**: 自动降仓保护机制
- **综合风险分析**: 整合多种方法的激进风险评估框架

## 使用方法

在对话中提及以下关键词将触发此Skill:
- 激进风险分析
- Kelly Criterion
- 反马丁格尔
- 风险平价
- 波动率目标
- 最大回撤控制
- 仓位管理

## 核心算法

### Kelly Criterion
```python
Kelly % = W - [(1-W)/R]
# W = 胜率, R = 盈亏比
```

### Anti-Martingale
```
盈利后: 仓位 × scale_factor
亏损后: 仓位 / scale_factor (或重置)
```

### Risk Parity
```
目标: 各资产对组合风险的贡献相等
权重优化: 最小化风险贡献方差
```

## 参考

- Pyfolio / Empyrical - 风险分析库
- Backtrader / Zipline - 回测框架
- Quantopian - 量化平台
