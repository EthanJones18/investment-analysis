# neutral-risk-analysis

风险中性分析Skill - 专注于股市投资的风险中性策略

## 功能

- **Beta中性对冲**: 计算对冲比率，构建Beta中性组合
- **美元中性配置**: 多空金额相等的中性策略
- **配对交易**: 统计套利和协整配对
- **多因子中性**: 消除多因子暴露
- **统计套利**: 综合市场中性策略框架

## 使用方法

在对话中提及以下关键词将触发此Skill:
- 风险中性分析
- 市场中性策略
- Beta中性
- 美元中性
- 配对交易
- 统计套利
- 协整分析

## 核心算法

### Beta中性
```python
对冲比率 = β_long / β_short
组合Beta = w_long × β_long - w_short × β_short = 0
```

### 配对交易
```python
价差 = Price_A - β × Price_B
Z-Score = (价差 - 均值) / 标准差
入场: |Z-Score| > 2
出场: |Z-Score| < 0.5
```

### 协整检验
- Engle-Granger两步法
- ADF检验
- p值 < 0.05表示协整

## 中性标准

| 指标 | 目标值 |
|------|--------|
| 组合Beta | ≈ 0 |
| 净敞口 | ≈ 0 |
| 相关系数 | > 0.8 |
| 协整p值 | < 0.05 |

## 参考

- PyPortfolioOpt
- Riskfolio-Lib
- Statsmodels
- Pairs Trading (Vidyamurthy)
