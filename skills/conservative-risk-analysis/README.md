# conservative-risk-analysis

保守风险分析Skill - 专注于股市投资的保守风险管理

## 功能

- **固定分数仓位管理**: 每笔交易固定比例风险（0.5%-1%）
- **CPPI投资组合保险**: 动态资产配置保护本金
- **VaR/CVaR风险价值**: 量化尾部风险
- **最大回撤控制**: 自动降仓保护机制
- **保本策略**: 资本保护优先

## 使用方法

在对话中提及以下关键词将触发此Skill:
- 保守风险分析
- 固定分数仓位
- CPPI/TIPP/OBPI
- VaR/CVaR
- 保本策略
- 最大回撤控制

## 核心算法

### Fixed Fractional
```python
仓位 = (账户价值 × 风险比例) / 每股风险
```

### CPPI
```python
缓冲 = 组合价值 - 底线
风险配置 = 缓冲 × 乘数
```

### VaR/CVaR
```python
VaR = 收益率分布的分位数
CVaR = 超过VaR的平均损失
```

## 保守原则

1. 单笔风险 ≤ 1%
2. 组合总风险 ≤ 6%
3. 最大回撤 ≤ 10-15%
4. 保本优先

## 参考

- Pyfolio / Empyrical
- Backtrader
- CPPI算法
