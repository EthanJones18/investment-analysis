# SKILL.md - Conservative Risk Analysis

## 描述

专注于保守风险管理的股市投资分析Skill。用于评估和计算保守型投资策略的风险敞口、仓位管理、资本保护等。

## 触发条件

当用户提及以下关键词时触发：
- 保守风险分析
- 固定分数仓位
- CPPI/TIPP/OBPI
- VaR/CVaR
- 保本策略
- 最大回撤控制

## 核心方法

### 1. Fixed Fractional Position Sizing

每笔交易承担固定比例的账户风险（保守型通常0.5%-1%）。

```python
def fixed_fractional_sizing(account_value, risk_pct, entry_price, stop_price):
    risk_amount = account_value * risk_pct
    risk_per_share = abs(entry_price - stop_price)
    return int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
```

### 2. CPPI (Constant Proportion Portfolio Insurance)

动态调整风险资产和无风险资产比例，保护本金。

```
Cushion = 组合价值 - Floor
风险资产配置 = Cushion × Multiplier
```

### 3. VaR/CVaR

- **VaR**: 给定置信水平下的最大预期损失
- **CVaR**: 超过VaR后的平均损失（更保守）

### 4. 最大回撤控制

设置回撤阈值，达到时自动降仓或停止交易。

## 保守型风险管理原则

1. **单笔风险 ≤ 1%** 账户价值
2. **组合总风险 ≤ 6%** 
3. **最大回撤 ≤ 10-15%**
4. **保本优先于盈利**
5. **频繁再平衡**

## 参考框架

- Pyfolio / Empyrical - 风险分析
- Backtrader - 回测框架
- CPPI算法实现
