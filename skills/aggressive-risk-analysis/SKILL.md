# SKILL.md - Aggressive Risk Analysis

## 描述

专注于激进风险管理的股市投资分析Skill。用于评估和计算激进型投资策略的风险敞口、仓位管理、回撤控制等。支持Kelly Criterion、反马丁格尔(Anti-Martingale)、风险平价(Risk Parity)、波动率目标(Volatility Targeting)等激进风险管理方法。

## 触发条件

当用户需要进行以下分析时触发此Skill：
- 激进型仓位管理策略
- Kelly Criterion仓位计算
- 反马丁格尔(Anti-Martingale)策略
- 风险平价(Risk Parity)配置
- 波动率目标(Volatility Targeting)
- 最大回撤控制
- 激进风险敞口评估
- 高风险投资组合优化

## 核心模块

### 1. Kelly Criterion 仓位计算

**理论基础**
Kelly Criterion由John Kelly于1956年提出，用于计算最优仓位比例以最大化长期资本增长。

**公式**
```
Kelly % = W - [(1-W)/R]

其中：
- W = 胜率 (Winning probability)
- R = 盈亏比 (Win/Loss ratio) = 平均盈利/平均亏损
- Kelly % = 建议投入资本比例
```

**Python实现**
```python
def kelly_criterion(win_rate, avg_win, avg_loss):
    """
    计算Kelly Criterion最优仓位比例
    
    参数:
        win_rate: 胜率 (0-1)
        avg_win: 平均盈利金额
        avg_loss: 平均亏损金额
    
    返回:
        kelly_pct: Kelly百分比 (建议仓位比例)
    """
    if avg_loss == 0:
        return 0
    
    R = avg_win / avg_loss  # 盈亏比
    kelly_pct = win_rate - ((1 - win_rate) / R)
    
    return max(0, min(kelly_pct, 1))  # 限制在0-1范围内


def fractional_kelly(win_rate, avg_win, avg_loss, fraction=0.25):
    """
    分数Kelly策略 - 更保守的仓位管理
    
    参数:
        fraction: Kelly分数 (0.25=1/4 Kelly, 0.5=Half Kelly)
    """
    full_kelly = kelly_criterion(win_rate, avg_win, avg_loss)
    return full_kelly * fraction
```

**使用示例**
```python
# 假设历史交易数据
win_rate = 0.6  # 60%胜率
avg_win = 4532   # 平均盈利
avg_loss = 3274  # 平均亏损

# 计算Full Kelly
kelly = kelly_criterion(win_rate, avg_win, avg_loss)
print(f"Full Kelly: {kelly:.2%}")  # 输出: 31%

# 计算Fractional Kelly (推荐)
half_kelly = fractional_kelly(win_rate, avg_win, avg_loss, 0.5)
quarter_kelly = fractional_kelly(win_rate, avg_win, avg_loss, 0.25)
print(f"Half Kelly: {half_kelly:.2%}")      # 15.5%
print(f"Quarter Kelly: {quarter_kelly:.2%}") # 7.75%
```

**注意事项**
- Full Kelly波动极大，实战中建议使用Fractional Kelly (1/4到1/2)
- 需要足够的历史数据(至少30-50笔交易)才能准确估计胜率
- 市场条件变化时，Kelly值会动态变化，需要定期重新计算

---

### 2. 反马丁格尔 (Anti-Martingale) 策略

**理论基础**
与马丁格尔策略相反，Anti-Martingale在盈利后增加仓位，亏损后减少仓位。核心理念："让利润奔跑，截断亏损"。

**策略规则**
```
初始仓位: 基准仓位 (如账户的2%)
盈利后: 仓位翻倍 (或按固定比例增加)
亏损后: 仓位减半 (或回到基准仓位)
最大仓位: 设置上限防止过度暴露
```

**Python实现**
```python
class AntiMartingale:
    """
    反马丁格尔仓位管理系统
    """
    def __init__(self, base_risk_pct=0.02, max_risk_pct=0.10, 
                 scale_factor=2.0, reset_on_loss=True):
        """
        参数:
            base_risk_pct: 基础风险比例 (默认2%)
            max_risk_pct: 最大风险比例 (默认10%)
            scale_factor: 盈利后仓位放大倍数 (默认2倍)
            reset_on_loss: 亏损后是否重置到基础仓位
        """
        self.base_risk_pct = base_risk_pct
        self.max_risk_pct = max_risk_pct
        self.scale_factor = scale_factor
        self.reset_on_loss = reset_on_loss
        
        self.current_risk_pct = base_risk_pct
        self.consecutive_wins = 0
        self.consecutive_losses = 0
    
    def calculate_position_size(self, account_value, entry_price, stop_price):
        """
        计算当前仓位大小
        
        参数:
            account_value: 账户总价值
            entry_price: 入场价格
            stop_price: 止损价格
        
        返回:
            position_size: 建议仓位数量
            risk_amount: 风险金额
        """
        risk_amount = account_value * self.current_risk_pct
        risk_per_share = abs(entry_price - stop_price)
        
        if risk_per_share == 0:
            return 0, 0
        
        position_size = risk_amount / risk_per_share
        return position_size, risk_amount
    
    def update_after_trade(self, is_win):
        """
        交易后更新仓位比例
        
        参数:
            is_win: 是否盈利
        """
        if is_win:
            self.consecutive_wins += 1
            self.consecutive_losses = 0
            # 盈利后增加仓位
            self.current_risk_pct = min(
                self.current_risk_pct * self.scale_factor,
                self.max_risk_pct
            )
        else:
            self.consecutive_losses += 1
            self.consecutive_wins = 0
            # 亏损后重置或降低仓位
            if self.reset_on_loss:
                self.current_risk_pct = self.base_risk_pct
            else:
                self.current_risk_pct = max(
                    self.current_risk_pct / self.scale_factor,
                    self.base_risk_pct
                )
    
    def get_status(self):
        """获取当前状态"""
        return {
            'current_risk_pct': self.current_risk_pct,
            'consecutive_wins': self.consecutive_wins,
            'consecutive_losses': self.consecutive_losses,
            'base_risk_pct': self.base_risk_pct,
            'max_risk_pct': self.max_risk_pct
        }
```

**使用示例**
```python
# 初始化Anti-Martingale管理器
amm = AntiMartingale(
    base_risk_pct=0.02,    # 基础2%风险
    max_risk_pct=0.10,     # 最大10%风险
    scale_factor=2.0,      # 盈利后翻倍
    reset_on_loss=True     # 亏损后重置
)

# 模拟交易序列
trades = [True, True, False, True, True, True]  # True=盈利, False=亏损
account_value = 100000

for i, is_win in enumerate(trades):
    position_size, risk_amount = amm.calculate_position_size(
        account_value, entry_price=100, stop_price=95
    )
    status = amm.get_status()
    print(f"交易{i+1}: 仓位风险={status['current_risk_pct']:.1%}, "
          f"连续盈利={status['consecutive_wins']}")
    amm.update_after_trade(is_win)
```

---

### 3. 风险平价 (Risk Parity) 配置

**理论基础**
风险平价策略通过使每个资产对组合总风险的贡献相等来实现风险分散，而不是按资金比例分配。

**核心公式**
```
资产i的风险贡献 = w_i * (Σw)_i / σ_p

其中:
- w_i = 资产i的权重
- Σ = 协方差矩阵
- σ_p = 组合波动率

目标: 使所有资产的风险贡献相等
```

**Python实现**
```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize

class RiskParity:
    """
    风险平价资产配置
    """
    def __init__(self, risk_target=None):
        """
        参数:
            risk_target: 目标波动率 (如0.15表示15%年化波动率)
        """
        self.risk_target = risk_target
        self.weights = None
    
    def _calculate_portfolio_volatility(self, weights, cov_matrix):
        """计算组合波动率"""
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    def _calculate_risk_contribution(self, weights, cov_matrix):
        """计算各资产的风险贡献"""
        port_vol = self._calculate_portfolio_volatility(weights, cov_matrix)
        marginal_risk = np.dot(cov_matrix, weights) / port_vol
        risk_contrib = weights * marginal_risk
        return risk_contrib
    
    def _risk_parity_objective(self, weights, cov_matrix):
        """
        风险平价目标函数 - 最小化风险贡献差异
        """
        risk_contrib = self._calculate_risk_contribution(weights, cov_matrix)
        target_risk = np.mean(risk_contrib)
        # 最小化风险贡献的方差
        return np.sum((risk_contrib - target_risk) ** 2)
    
    def optimize(self, returns_df, long_only=True):
        """
        优化风险平价权重
        
        参数:
            returns_df: 资产收益率DataFrame
            long_only: 是否只允许做多
        
        返回:
            weights: 最优权重
        """
        # 计算协方差矩阵
        cov_matrix = returns_df.cov().values
        n_assets = len(returns_df.columns)
        
        # 初始权重: 等权重
        init_weights = np.array([1/n_assets] * n_assets)
        
        # 约束条件
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        
        if long_only:
            bounds = tuple((0, 1) for _ in range(n_assets))
        else:
            bounds = tuple((-1, 1) for _ in range(n_assets))
        
        # 优化
        result = minimize(
            self._risk_parity_objective,
            init_weights,
            args=(cov_matrix,),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        self.weights = result.x
        
        # 如果设置了目标波动率，进行杠杆调整
        if self.risk_target is not None:
            current_vol = self._calculate_portfolio_volatility(
                self.weights, cov_matrix
            ) * np.sqrt(252)  # 年化
            leverage = self.risk_target / current_vol
            self.weights = self.weights * leverage
        
        return dict(zip(returns_df.columns, self.weights))
    
    def get_risk_contributions(self, returns_df):
        """获取各资产的风险贡献"""
        if self.weights is None:
            raise ValueError("请先调用optimize()方法")
        
        cov_matrix = returns_df.cov().values
        risk_contrib = self._calculate_risk_contribution(self.weights, cov_matrix)
        
        return dict(zip(returns_df.columns, risk_contrib))


# 简化版风险平价 (使用逆波动率加权)
def inverse_volatility_weights(returns_df):
    """
    逆波动率加权 - 风险平价的简化实现
    
    参数:
        returns_df: 资产收益率DataFrame
    
    返回:
        weights: 权重字典
    """
    vols = returns_df.std() * np.sqrt(252)  # 年化波动率
    inv_vols = 1 / vols
    weights = inv_vols / inv_vols.sum()
    return weights.to_dict()
```

**使用示例**
```python
# 生成模拟数据
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
assets = ['股票', '债券', '商品', '黄金']

# 模拟不同波动率的资产收益
returns_data = {
    '股票': np.random.normal(0.0008, 0.02, len(dates)),   # 高波动
    '债券': np.random.normal(0.0003, 0.005, len(dates)),  # 低波动
    '商品': np.random.normal(0.0005, 0.015, len(dates)),  # 中波动
    '黄金': np.random.normal(0.0004, 0.012, len(dates))   # 中低波动
}
returns_df = pd.DataFrame(returns_data, index=dates)

# 方法1: 逆波动率加权 (简单)
simple_weights = inverse_volatility_weights(returns_df)
print("逆波动率权重:", simple_weights)

# 方法2: 优化风险平价 (精确)
rp = RiskParity(risk_target=0.10)  # 目标10%年化波动率
optimal_weights = rp.optimize(returns_df)
print("风险平价权重:", optimal_weights)

# 查看风险贡献
risk_contribs = rp.get_risk_contributions(returns_df)
print("风险贡献:", risk_contribs)
```

---

### 4. 波动率目标 (Volatility Targeting)

**理论基础**
根据市场波动率动态调整仓位，在高波动时期降低暴露，低波动时期增加暴露，以维持恒定的目标波动率。

**Python实现**
```python
class VolatilityTargeting:
    """
    波动率目标仓位管理
    """
    def __init__(self, target_vol=0.15, lookback=60, max_leverage=2.0):
        """
        参数:
            target_vol: 目标年化波动率 (默认15%)
            lookback: 计算历史波动率的回看周期 (默认60天)
            max_leverage: 最大杠杆倍数 (默认2倍)
        """
        self.target_vol = target_vol
        self.lookback = lookback
        self.max_leverage = max_leverage
    
    def calculate_position_scalar(self, returns_series):
        """
        计算仓位调整系数
        
        参数:
            returns_series: 资产收益率序列
        
        返回:
            scalar: 仓位调整系数 (0到max_leverage之间)
        """
        if len(returns_series) < self.lookback:
            return 1.0
        
        # 计算历史波动率 (年化)
        recent_returns = returns_series[-self.lookback:]
        current_vol = recent_returns.std() * np.sqrt(252)
        
        if current_vol == 0:
            return 1.0
        
        # 计算调整系数
        scalar = self.target_vol / current_vol
        
        # 限制杠杆
        return min(scalar, self.max_leverage)
    
    def get_position_size(self, base_position, returns_series):
        """
        获取调整后的仓位大小
        
        参数:
            base_position: 基础仓位
            returns_series: 资产收益率序列
        
        返回:
            adjusted_position: 调整后的仓位
            scalar: 调整系数
        """
        scalar = self.calculate_position_scalar(returns_series)
        adjusted_position = base_position * scalar
        return adjusted_position, scalar


class DynamicVolatilityScaling:
    """
    动态波动率缩放 - 多资产组合版本
    """
    def __init__(self, target_vol=0.15, lookback=60, 
                 vol_cap=0.25, vol_floor=0.05):
        """
        参数:
            vol_cap: 波动率上限 (超过此值大幅降低仓位)
            vol_floor: 波动率下限 (低于此值允许增加仓位)
        """
        self.target_vol = target_vol
        self.lookback = lookback
        self.vol_cap = vol_cap
        self.vol_floor = vol_floor
    
    def calculate_scaling_factor(self, returns_series):
        """
        计算缩放因子 (带上下限保护)
        """
        if len(returns_series) < self.lookback:
            return 1.0
        
        current_vol = returns_series[-self.lookback:].std() * np.sqrt(252)
        
        # 波动率过高时，使用更激进的降仓
        if current_vol > self.vol_cap:
            # 超过上限后，仓位呈指数下降
            excess = (current_vol - self.vol_cap) / self.vol_cap
            scalar = (self.target_vol / current_vol) * np.exp(-excess)
        # 波动率过低时，限制加仓幅度
        elif current_vol < self.vol_floor:
            scalar = min(self.target_vol / current_vol, 2.0)
        else:
            scalar = self.target_vol / current_vol
        
        return max(0.1, min(scalar, 3.0))  # 限制在10%-300%
```

---

### 5. 最大回撤控制

**理论基础**
通过监控账户回撤水平，在达到特定阈值时自动降低仓位，保护资本。

**Python实现**
```python
class DrawdownController:
    """
    最大回撤控制系统
    """
    def __init__(self, 
                 max_drawdown_limit=0.20,  # 最大允许回撤20%
                 warning_threshold=0.10,    # 警告阈值10%
                 reduction_steps=None):
        """
        参数:
            max_drawdown_limit: 最大允许回撤
            warning_threshold: 警告阈值
            reduction_steps: 降仓阶梯 [(回撤阈值, 仓位比例), ...]
        """
        self.max_drawdown_limit = max_drawdown_limit
        self.warning_threshold = warning_threshold
        
        # 默认降仓阶梯
        if reduction_steps is None:
            self.reduction_steps = [
                (0.05, 0.75),   # 回撤5%，仓位降至75%
                (0.10, 0.50),   # 回撤10%，仓位降至50%
                (0.15, 0.25),   # 回撤15%，仓位降至25%
                (0.20, 0.00),   # 回撤20%，停止交易
            ]
        else:
            self.reduction_steps = reduction_steps
        
        self.peak_value = 0
        self.current_drawdown = 0
        self.position_scalar = 1.0
        self.trading_halted = False
    
    def update(self, current_value):
        """
        更新回撤状态
        
        参数:
            current_value: 当前账户价值
        
        返回:
            status: 当前状态字典
        """
        # 更新峰值
        if current_value > self.peak_value:
            self.peak_value = current_value
            self.current_drawdown = 0
            self.position_scalar = 1.0
            self.trading_halted = False
        else:
            # 计算回撤
            self.current_drawdown = (self.peak_value - current_value) / self.peak_value
            
            # 根据回撤调整仓位
            for threshold, scalar in self.reduction_steps:
                if self.current_drawdown >= threshold:
                    self.position_scalar = scalar
                    if scalar == 0:
                        self.trading_halted = True
        
        return {
            'peak_value': self.peak_value,
            'current_value': current_value,
            'drawdown': self.current_drawdown,
            'position_scalar': self.position_scalar,
            'trading_halted': self.trading_halted
        }
    
    def can_trade(self):
        """检查是否可以交易"""
        return not self.trading_halted
    
    def get_position_size(self, base_size):
        """获取调整后的仓位大小"""
        return base_size * self.position_scalar


class AdvancedDrawdownControl:
    """
    高级回撤控制 - 包含恢复机制
    """
    def __init__(self,
                 max_dd=0.20,
                 recovery_trigger=0.75,  # 回撤恢复75%后重新加仓
                 aggressive_recovery=False):
        self.max_dd = max_dd
        self.recovery_trigger = recovery_trigger
        self.aggressive_recovery = aggressive_recovery
        
        self.peak = 0
        self.valley = 0
        self.max_drawdown_reached = 0
        self.current_scalar = 1.0
        self.recovery_mode = False
    
    def update(self, current_value):
        """更新并返回仓位调整系数"""
        # 更新峰值和谷值
        if current_value > self.peak:
            self.peak = current_value
            self.valley = current_value
            self.max_drawdown_reached = 0
            self.current_scalar = 1.0
            self.recovery_mode = False
        elif current_value < self.valley:
            self.valley = current_value
            self.max_drawdown_reached = (self.peak - self.valley) / self.peak
            
            # 计算降仓比例
            if self.max_drawdown_reached >= self.max_dd:
                self.current_scalar = 0
            else:
                # 线性降仓
                self.current_scalar = 1 - (self.max_drawdown_reached / self.max_dd)
        else:
            # 在恢复中
            if self.max_drawdown_reached > 0:
                recovery_pct = (current_value - self.valley) / (self.peak - self.valley)
                
                if recovery_pct >= self.recovery_trigger:
                    # 恢复足够，可以重新加仓
                    if self.aggressive_recovery:
                        self.current_scalar = min(1.0, self.current_scalar + 0.25)
                    else:
                        self.current_scalar = 1.0
                    self.recovery_mode = True
        
        return self.current_scalar
```

---

### 6. 激进风险综合评估框架

**Python实现**
```python
class AggressiveRiskAnalyzer:
    """
    激进风险综合分析器
    整合多种风险管理方法
    """
    def __init__(self, 
                 account_value=100000,
                 kelly_fraction=0.25,
                 target_vol=0.15,
                 max_dd=0.20,
                 base_risk_pct=0.02):
        
        self.account_value = account_value
        self.kelly_fraction = kelly_fraction
        
        # 初始化各模块
        self.amm = AntiMartingale(base_risk_pct=base_risk_pct, max_risk_pct=0.10)
        self.vol_target = VolatilityTargeting(target_vol=target_vol)
        self.dd_control = DrawdownController(max_drawdown_limit=max_dd)
        
        self.history = []
    
    def analyze_trade(self, 
                      symbol,
                      win_rate, 
                      avg_win, 
                      avg_loss,
                      recent_returns,
                      entry_price,
                      stop_price):
        """
        综合分析并给出仓位建议
        
        参数:
            symbol: 交易标的
            win_rate: 胜率
            avg_win: 平均盈利
            avg_loss: 平均亏损
            recent_returns: 近期收益率序列
            entry_price: 入场价
            stop_price: 止损价
        
        返回:
            recommendation: 综合建议
        """
        results = {
            'symbol': symbol,
            'account_value': self.account_value,
            'timestamp': pd.Timestamp.now()
        }
        
        # 1. Kelly Criterion计算
        kelly_pct = kelly_criterion(win_rate, avg_win, avg_loss)
        fractional_kelly = kelly_pct * self.kelly_fraction
        results['kelly'] = {
            'full_kelly': kelly_pct,
            'fractional_kelly': fractional_kelly,
            'suggested_risk': fractional_kelly * self.account_value
        }
        
        # 2. Anti-Martingale建议
        amm_position, amm_risk = self.amm.calculate_position_size(
            self.account_value, entry_price, stop_price
        )
        results['anti_martingale'] = {
            'current_risk_pct': self.amm.current_risk_pct,
            'position_size': amm_position,
            'risk_amount': amm_risk,
            'consecutive_wins': self.amm.consecutive_wins
        }
        
        # 3. 波动率目标调整
        vol_scalar = self.vol_target.calculate_position_scalar(recent_returns)
        results['volatility_targeting'] = {
            'current_vol': recent_returns.std() * np.sqrt(252),
            'target_vol': self.vol_target.target_vol,
            'scalar': vol_scalar
        }
        
        # 4. 回撤控制检查
        dd_status = self.dd_control.update(self.account_value)
        results['drawdown_control'] = dd_status
        
        # 5. 综合建议
        if not self.dd_control.can_trade():
            results['recommendation'] = {
                'action': 'HALT',
                'reason': 'Maximum drawdown reached',
                'position_size': 0
            }
        else:
            # 综合各因素的最小值 (最保守)
            suggested_risk = min(
                fractional_kelly * self.account_value * 0.5,  # Kelly建议的一半
                amm_risk,
                self.account_value * 0.05  # 单笔最大5%
            )
            
            # 应用波动率调整和回撤控制
            risk_per_share = abs(entry_price - stop_price)
            if risk_per_share > 0:
                base_position = suggested_risk / risk_per_share
                final_position = base_position * vol_scalar * dd_status['position_scalar']
            else:
                final_position = 0
            
            results['recommendation'] = {
                'action': 'TRADE',
                'position_size': int(final_position),
                'risk_amount': suggested_risk * vol_scalar * dd_status['position_scalar'],
                'risk_pct': (suggested_risk * vol_scalar * dd_status['position_scalar']) / self.account_value
            }
        
        self.history.append(results)
        return results
    
    def update_after_trade(self, pnl):
        """交易后更新状态"""
        self.account_value += pnl
        is_win = pnl > 0
        self.amm.update_after_trade(is_win)
    
    def get_summary(self):
        """获取分析摘要"""
        if not self.history:
            return "No trades analyzed yet"
        
        recent = self.history[-1]
        return f"""
激进风险分析摘要:
================
账户价值: ${self.account_value:,.2f}
当前回撤: {recent['drawdown_control']['drawdown']:.2%}
连续盈利: {recent['anti_martingale']['consecutive_wins']}

风险指标:
- Kelly建议: {recent['kelly']['fractional_kelly']:.2%} (分数Kelly)
- 当前AM风险: {recent['anti_martingale']['current_risk_pct']:.2%}
- 波动率调整: {recent['volatility_targeting']['scalar']:.2f}x
- 回撤系数: {recent['drawdown_control']['position_scalar']:.2f}x

交易状态: {'正常' if self.dd_control.can_trade() else '暂停'}
"""
```

---

## 使用示例

### 完整分析流程
```python
# 初始化分析器
analyzer = AggressiveRiskAnalyzer(
    account_value=100000,
    kelly_fraction=0.25,  # 使用1/4 Kelly
    target_vol=0.15,      # 目标15%波动率
    max_dd=0.20,          # 最大20%回撤
    base_risk_pct=0.02    # 基础2%风险
)

# 模拟交易分析
trade_data = {
    'symbol': 'AAPL',
    'win_rate': 0.55,
    'avg_win': 500,
    'avg_loss': 300,
    'recent_returns': pd.Series(np.random.normal(0.001, 0.02, 60)),
    'entry_price': 150,
    'stop_price': 145
}

# 获取分析结果
result = analyzer.analyze_trade(**trade_data)
print(analyzer.get_summary())

# 模拟交易执行
pnl = 450  # 盈利
analyzer.update_after_trade(pnl)
```

---

## 关键指标解释

### 风险指标
| 指标 | 说明 | 激进阈值 |
|------|------|----------|
| Kelly % | 最优仓位比例 | 通常使用1/4到1/2 |
| 最大回撤 | 峰值到谷底最大亏损 | < 20% |
| 波动率 | 收益波动程度 | 目标10-20% |
| 风险贡献 | 单资产对组合风险贡献 | 尽量均衡 |

### 仓位管理原则
1. **永远不要使用Full Kelly** - 波动太大，建议使用Fractional Kelly
2. **盈利加仓，亏损减仓** - Anti-Martingale核心原则
3. **波动率高时降仓** - Volatility Targeting
4. **回撤达到阈值必须降仓** - Drawdown Control
5. **单笔风险不超过5%** - 绝对上限

---

## 参考资源

### 开源框架
- **Pyfolio**: Quantopian开发的投资组合风险分析库
- **Empyrical**: 风险指标计算库 (Pyfolio底层)
- **Backtrader**: 支持Pyfolio集成的回测框架
- **Zipline**: Quantopian的开源回测引擎

### 理论基础
- Kelly Criterion: John Kelly (1956)
- Risk Parity: Ray Dalio, Bridgewater
- Volatility Targeting: 现代组合理论延伸
- Anti-Martingale: 专业交易实践

---

## 注意事项

1. **历史数据不代表未来** - 所有计算基于历史统计，市场会变化
2. **参数需要定期调整** - 根据市场环境和个人风险偏好
3. **心理承受能力** - 激进策略需要强大的心理素质
4. **资金管理优先** - 永远把保护本金放在第一位
5. **回测验证** - 任何策略上线前必须充分回测
