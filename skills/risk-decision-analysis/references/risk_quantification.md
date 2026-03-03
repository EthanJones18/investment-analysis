# 风险量化模型

## 概述

风险量化模型用于将投资风险转化为可度量的指标，帮助投资者客观评估风险水平，制定风险管理策略。

## 风险价值 (VaR)

### 定义
VaR (Value at Risk) 表示在给定置信水平和时间周期下，投资组合可能遭受的最大损失。

### 计算方法

#### 1. 历史模拟法
```
VaR = 历史收益率分布的分位数

步骤:
1. 收集历史收益率数据
2. 排序收益率
3. 取对应置信水平的分位数
```

#### 2. 方差-协方差法
```
VaR = μ - z × σ

其中:
μ = 预期收益率
z = 标准正态分布的分位数 (95%: 1.645, 99%: 2.326)
σ = 收益率标准差
```

#### 3. 蒙特卡洛模拟法
```
步骤:
1. 建立收益率模型
2. 随机生成大量情景
3. 计算每个情景的损失
4. 取对应置信水平的分位数
```

### Python实现
```python
import numpy as np
import pandas as pd

def calculate_var(returns, confidence=0.95, method='historical'):
    """
    计算VaR
    """
    if method == 'historical':
        return np.percentile(returns, (1 - confidence) * 100)
    
    elif method == 'parametric':
        mean = returns.mean()
        std = returns.std()
        z_score = {0.95: 1.645, 0.99: 2.326}[confidence]
        return mean - z_score * std
    
    elif method == 'monte_carlo':
        # 蒙特卡洛模拟
        simulations = 10000
        mean = returns.mean()
        std = returns.std()
        simulated_returns = np.random.normal(mean, std, simulations)
        return np.percentile(simulated_returns, (1 - confidence) * 100)
```

## 条件风险价值 (CVaR/ES)

### 定义
CVaR (Conditional Value at Risk) 或 ES (Expected Shortfall) 表示在超过VaR阈值的情况下，损失的期望值。

### 计算公式
```
CVaR_α = E[X | X ≤ VaR_α]

即: 所有小于VaR的收益率的平均值
```

### Python实现
```python
def calculate_cvar(returns, confidence=0.95):
    """
    计算CVaR
    """
    var = calculate_var(returns, confidence)
    return returns[returns <= var].mean()
```

## 风险调整收益指标

### 夏普比率 (Sharpe Ratio)
```
Sharpe Ratio = (Rp - Rf) / σp

其中:
Rp = 投资组合收益率
Rf = 无风险利率
σp = 投资组合标准差
```

### 索提诺比率 (Sortino Ratio)
```
Sortino Ratio = (Rp - Rf) / σd

其中:
σd = 下行标准差 (只考虑负收益)
```

### 卡玛比率 (Calmar Ratio)
```
Calmar Ratio = (Rp - Rf) / Max Drawdown
```

### 特雷诺比率 (Treynor Ratio)
```
Treynor Ratio = (Rp - Rf) / β

其中:
β = 投资组合的Beta值
```

### Python实现
```python
def risk_adjusted_returns(returns, risk_free_rate=0.02):
    """
    计算风险调整收益指标
    """
    excess_returns = returns - risk_free_rate / 252  # 日度化
    
    # 夏普比率
    sharpe = excess_returns.mean() / returns.std() * np.sqrt(252)
    
    # 索提诺比率
    downside_returns = returns[returns < 0]
    sortino = excess_returns.mean() / downside_returns.std() * np.sqrt(252)
    
    # 最大回撤
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # 卡玛比率
    calmar = excess_returns.mean() * 252 / abs(max_drawdown)
    
    return {
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'max_drawdown': max_drawdown,
        'calmar_ratio': calmar
    }
```

## 风险贡献分析

### 边际风险贡献
```
MRCi = ∂σp / ∂wi

其中:
wi = 资产i的权重
σp = 组合标准差
```

### 风险贡献
```
RCi = wi × MRCi
```

### 风险贡献百分比
```
%RCi = RCi / σp
```

### Python实现
```python
def risk_contribution(weights, cov_matrix):
    """
    计算风险贡献
    """
    portfolio_vol = np.sqrt(weights @ cov_matrix @ weights)
    
    # 边际风险贡献
    mrc = (cov_matrix @ weights) / portfolio_vol
    
    # 风险贡献
    rc = weights * mrc
    
    # 风险贡献百分比
    rc_pct = rc / portfolio_vol
    
    return {
        'marginal_rc': mrc,
        'risk_contribution': rc,
        'risk_contribution_pct': rc_pct
    }
```

## 压力测试

### 情景设计

#### 历史情景
- 2008年金融危机
- 2020年新冠疫情
- 2015年股灾

#### 假设情景
- 利率上升200bp
- 股市下跌30%
- 信用利差扩大
- 汇率波动

### Python实现
```python
def stress_test(portfolio, scenarios):
    """
    压力测试
    """
    results = {}
    
    for scenario_name, shocks in scenarios.items():
        # 应用冲击
        stressed_values = portfolio['value'] * (1 + shocks)
        
        # 计算损失
        loss = portfolio['value'].sum() - stressed_values.sum()
        loss_pct = loss / portfolio['value'].sum()
        
        results[scenario_name] = {
            'absolute_loss': loss,
            'percentage_loss': loss_pct
        }
    
    return results

# 示例情景
scenarios = {
    '2008_crisis': {'stocks': -0.40, 'bonds': 0.05, 'commodities': -0.30},
    'covid_crash': {'stocks': -0.35, 'bonds': 0.02, 'commodities': -0.25},
    'rate_shock': {'stocks': -0.15, 'bonds': -0.10, 'commodities': 0.05}
}
```

## 尾部风险分析

### 偏度 (Skewness)
```
负偏度: 左尾风险大
正偏度: 右尾机会大
```

### 峰度 (Kurtosis)
```
高峰度: 极端事件发生概率高
低峰度: 收益率分布更接近正态
```

### Python实现
```python
def tail_risk_analysis(returns):
    """
    尾部风险分析
    """
    from scipy import stats
    
    skewness = stats.skew(returns)
    kurtosis = stats.kurtosis(returns)
    
    # 极值分析
    var_99 = np.percentile(returns, 1)
    cvar_99 = returns[returns <= var_99].mean()
    
    return {
        'skewness': skewness,
        'kurtosis': kurtosis,
        'var_99': var_99,
        'cvar_99': cvar_99
    }
```

## 风险预算

### 风险预算分配
```python
def risk_budget_allocation(target_risk_contribution, cov_matrix):
    """
    风险预算配置
    找到使风险贡献等于目标风险贡献的权重
    """
    from scipy.optimize import minimize
    
    n = len(target_risk_contribution)
    
    def objective(w):
        rc = risk_contribution(w, cov_matrix)['risk_contribution_pct']
        return np.sum((rc - target_risk_contribution) ** 2)
    
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = [(0, 1) for _ in range(n)]
    
    result = minimize(objective, np.ones(n) / n, 
                     method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x
```

## 参考资源

- **书籍**: 《风险管理与金融机构》、《量化风险管理》
- **Python库**: PyPortfolioOpt, Riskfolio-Lib, empyrical
- **论文**: "RiskMetrics Technical Document"
