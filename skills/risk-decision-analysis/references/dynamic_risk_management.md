# 动态风险管理

## 概述

动态风险管理是一种根据市场环境和投资组合表现持续调整风险敞口的管理方法。与静态风险管理不同，动态风险管理强调灵活性和适应性。

## 动态风险预算

### 风险预算调整框架

#### 基于市场状态的调整
```
牛市: 风险预算 +20%
震荡市: 风险预算 不变
熊市: 风险预算 -30%
```

#### 基于波动率的调整
```
波动率 < 10%: 风险预算 +10%
波动率 10-20%: 风险预算 不变
波动率 20-30%: 风险预算 -15%
波动率 > 30%: 风险预算 -30%
```

#### 基于回撤的调整
```
回撤 < 5%: 正常运作
回撤 5-10%: 风险预算 -10%
回撤 10-15%: 风险预算 -25%
回撤 > 15%: 暂停新增风险
```

### Python实现
```python
class DynamicRiskBudget:
    def __init__(self, base_budget):
        self.base_budget = base_budget
        self.current_budget = base_budget
    
    def adjust_for_market_regime(self, regime):
        """基于市场状态调整"""
        adjustments = {
            'bull': 1.2,
            'sideways': 1.0,
            'bear': 0.7
        }
        self.current_budget = self.base_budget * adjustments.get(regime, 1.0)
        return self.current_budget
    
    def adjust_for_volatility(self, current_vol, target_vol=0.20):
        """基于波动率调整"""
        vol_ratio = target_vol / current_vol
        self.current_budget = self.base_budget * min(vol_ratio, 1.5)
        return self.current_budget
    
    def adjust_for_drawdown(self, current_dd):
        """基于回撤调整"""
        if current_dd < 0.05:
            multiplier = 1.0
        elif current_dd < 0.10:
            multiplier = 0.9
        elif current_dd < 0.15:
            multiplier = 0.75
        else:
            multiplier = 0.5
        
        self.current_budget = self.base_budget * multiplier
        return self.current_budget
```

## 动态仓位管理

### 波动率目标法
```
目标仓位 = 目标波动率 / 预期波动率

例如:
目标波动率 = 15%
预期波动率 = 25%
目标仓位 = 15% / 25% = 60%
```

### 风险平价调整
```python
def dynamic_risk_parity(returns, lookback=60):
    """
    动态风险平价
    """
    # 计算滚动波动率
    rolling_vol = returns.rolling(lookback).std() * np.sqrt(252)
    
    # 风险平价权重
    inv_vol = 1 / rolling_vol
    weights = inv_vol.div(inv_vol.sum(axis=1), axis=0)
    
    return weights
```

### 趋势跟踪调整
```python
def trend_based_sizing(prices, fast=50, slow=200):
    """
    基于趋势的仓位调整
    """
    fast_ma = prices.rolling(fast).mean()
    slow_ma = prices.rolling(slow).mean()
    
    # 趋势强度
    trend = (fast_ma - slow_ma) / slow_ma
    
    # 仓位调整
    base_size = 0.5
    adjustment = np.clip(trend * 5, -0.5, 0.5)  # 限制调整范围
    
    return base_size + adjustment
```

## 动态止损策略

### 波动率止损
```python
def volatility_stop(entry_price, atr, multiplier=2):
    """
    ATR波动率止损
    """
    return entry_price - multiplier * atr
```

### 时间衰减止损
```python
def time_decay_stop(entry_date, max_days=30, decay_rate=0.02):
    """
    时间衰减止损
    随着时间推移，逐步收紧止损
    """
    days_held = (datetime.now() - entry_date).days
    
    # 初始止损
    initial_stop = 0.10
    
    # 时间衰减
    time_decay = min(days_held * decay_rate, 0.05)
    
    return initial_stop - time_decay
```

### 波动率自适应止损
```python
def adaptive_stop_loss(returns, base_stop=0.10, lookback=20):
    """
    自适应止损
    根据近期波动率调整止损距离
    """
    current_vol = returns.tail(lookback).std() * np.sqrt(252)
    
    # 基准波动率
    base_vol = 0.20
    
    # 调整系数
    adjustment = current_vol / base_vol
    
    return base_stop * adjustment
```

## 动态对冲

### 基于相关性的对冲
```python
def correlation_based_hedge(portfolio_returns, hedge_asset_returns, threshold=0.7):
    """
    基于相关性的动态对冲
    """
    # 计算滚动相关性
    correlation = portfolio_returns.rolling(60).corr(hedge_asset_returns)
    
    # 当相关性超过阈值时增加对冲
    hedge_ratio = np.where(correlation > threshold, 0.3, 0.1)
    
    return hedge_ratio
```

### 基于波动率的期权对冲
```python
def volatility_based_hedge(current_vol, target_vol=0.15):
    """
    基于波动率的期权对冲
    """
    if current_vol > target_vol * 1.5:
        # 高波动率，增加保护
        return {'put_spread': 0.3, 'collar': 0.2}
    elif current_vol < target_vol * 0.5:
    # 低波动率，减少保护
        return {'put_spread': 0.1, 'collar': 0.0}
    else:
        # 正常波动率
        return {'put_spread': 0.2, 'collar': 0.1}
```

## 动态再平衡

### 阈值再平衡
```python
class ThresholdRebalancer:
    def __init__(self, target_weights, threshold=0.05):
        self.target_weights = target_weights
        self.threshold = threshold
    
    def check_rebalance(self, current_weights):
        """检查是否需要再平衡"""
        deviation = abs(current_weights - self.target_weights)
        return deviation.max() > self.threshold
    
    def rebalance(self, current_weights):
        """执行再平衡"""
        if self.check_rebalance(current_weights):
            return self.target_weights
        return current_weights
```

### 波动率定时再平衡
```python
def volatility_timing_rebalance(volatility, base_frequency='quarterly'):
    """
    基于波动率的再平衡时机选择
    高波动率时减少再平衡频率，降低交易成本
    """
    if volatility > 0.30:
        return 'yearly'
    elif volatility > 0.20:
        return 'semi-annually'
    else:
        return base_frequency
```

## 风险监控仪表盘

### 关键指标监控
```python
class RiskDashboard:
    def __init__(self, portfolio):
        self.portfolio = portfolio
    
    def get_metrics(self):
        """获取风险指标"""
        returns = self.portfolio.returns
        
        return {
            'var_95': self.calculate_var(returns, 0.95),
            'var_99': self.calculate_var(returns, 0.99),
            'cvar_95': self.calculate_cvar(returns, 0.95),
            'max_drawdown': self.calculate_max_drawdown(returns),
            'volatility': returns.std() * np.sqrt(252),
            'sharpe_ratio': self.calculate_sharpe(returns),
            'beta': self.calculate_beta(returns),
            'tail_risk': self.calculate_tail_risk(returns)
        }
    
    def generate_alerts(self, metrics, thresholds):
        """生成风险预警"""
        alerts = []
        
        if metrics['var_95'] < thresholds['var_95']:
            alerts.append('VaR超过阈值')
        
        if metrics['max_drawdown'] < thresholds['max_drawdown']:
            alerts.append('回撤超过阈值')
        
        if metrics['volatility'] > thresholds['volatility']:
            alerts.append('波动率过高')
        
        return alerts
```

## 应急预案

### 风险事件响应
```python
class RiskEventHandler:
    def __init__(self):
        self.response_plans = {
            'flash_crash': self.handle_flash_crash,
            'liquidity_crisis': self.handle_liquidity_crisis,
            'correlation_spike': self.handle_correlation_spike
        }
    
    def handle_flash_crash(self, portfolio):
        """应对闪崩"""
        return {
            'action': '暂停交易',
            'reduce_position': 0.5,
            'increase_cash': 0.3,
            'activate_hedge': True
        }
    
    def handle_liquidity_crisis(self, portfolio):
        """应对流动性危机"""
        return {
            'action': '降低仓位',
            'focus_on_liquid_assets': True,
            'reduce_position': 0.3,
            'avoid_illiquid_assets': True
        }
```

## 实施建议

### 1. 建立风险预算框架
- 确定总体风险预算
- 设定调整规则和阈值
- 明确各资产风险贡献目标

### 2. 实施动态监控
- 实时监控关键风险指标
- 设置预警阈值
- 建立应急响应机制

### 3. 定期回顾优化
- 定期评估风险管理效果
- 分析风险事件响应
- 持续优化模型参数

### 4. 技术系统支持
- 自动化风险计算
- 实时监控系统
- 预警通知机制
