# SKILL.md - Neutral Risk Analysis

## 描述

专注于风险中性管理的股市投资分析Skill。用于评估和计算市场中性策略的风险敞口、对冲比率、配对交易等。支持Beta中性、美元中性、统计套利、协整配对交易、多因子中性等风险中性方法。

## 触发条件

当用户需要进行以下分析时触发此Skill：
- 风险中性分析
- 市场中性策略 (Market Neutral)
- Beta中性对冲
- 美元中性配置
- 配对交易 (Pairs Trading)
- 统计套利
- 协整分析
- 多因子中性
- 长短仓组合优化

## 核心模块

### 1. Beta中性对冲

**理论基础**
Beta中性是指组合的市场Beta值为0，即组合收益与市场收益无关。通过调整多空仓位比例，使得多头Beta等于空头Beta。

**核心公式**
```
组合Beta = w_long × β_long - w_short × β_short = 0

对冲比率 = β_long / β_short
空头仓位 = 多头仓位 × 对冲比率

其中:
- w_long, w_short: 多空权重
- β_long, β_short: 多空资产的Beta值
```

**Python实现**
```python
import numpy as np
import pandas as pd
from scipy import stats

class BetaNeutralHedge:
    """
    Beta中性对冲计算器
    """
    def __init__(self, market_data):
        """
        参数:
            market_data: 市场基准收益率序列 (如SPY)
        """
        self.market_data = market_data
    
    def calculate_beta(self, returns, window=252):
        """
        计算Beta值
        
        参数:
            returns: 资产收益率序列
            window: 计算窗口
        
        返回:
            beta: Beta值
            alpha: Alpha值
            r_squared: 拟合优度
        """
        if len(returns) < window:
            window = len(returns)
        
        asset_returns = returns[-window:]
        market_returns = self.market_data[-window:]
        
        # 线性回归计算Beta
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            market_returns, asset_returns
        )
        
        return {
            'beta': slope,
            'alpha': intercept,
            'r_squared': r_value ** 2,
            'p_value': p_value
        }
    
    def calculate_hedge_ratio(self, long_beta, short_beta):
        """
        计算对冲比率
        
        参数:
            long_beta: 多头资产Beta
            short_beta: 空头资产Beta
        
        返回:
            hedge_ratio: 对冲比率
        """
        if short_beta == 0:
            return 0
        return long_beta / short_beta
    
    def get_neutral_position(self, long_value, long_beta, short_beta):
        """
        获取Beta中性仓位
        
        参数:
            long_value: 多头仓位金额
            long_beta: 多头Beta
            short_beta: 空头Beta
        
        返回:
            short_value: 空头仓位金额
            hedge_ratio: 对冲比率
        """
        hedge_ratio = self.calculate_hedge_ratio(long_beta, short_beta)
        short_value = long_value * hedge_ratio
        
        return {
            'long_value': long_value,
            'short_value': short_value,
            'hedge_ratio': hedge_ratio,
            'net_beta': long_beta - (short_beta * hedge_ratio)
        }


# 快速计算Beta
def calculate_beta_simple(stock_returns, market_returns):
    """
    简化版Beta计算
    
    参数:
        stock_returns: 股票收益率
        market_returns: 市场收益率
    
    返回:
        Beta值
    """
    covariance = np.cov(stock_returns, market_returns)[0][1]
    market_variance = np.var(market_returns)
    
    if market_variance == 0:
        return 0
    
    return covariance / market_variance
```

**使用示例**
```python
# 模拟数据
np.random.seed(42)
market_returns = np.random.normal(0.001, 0.02, 252)
stock_a_returns = market_returns * 1.2 + np.random.normal(0, 0.01, 252)  # Beta ≈ 1.2
stock_b_returns = market_returns * 0.8 + np.random.normal(0, 0.01, 252)  # Beta ≈ 0.8

# 初始化Beta中性计算器
hedge = BetaNeutralHedge(market_returns)

# 计算Beta
beta_a = hedge.calculate_beta(stock_a_returns)
beta_b = hedge.calculate_beta(stock_b_returns)

print(f"股票A - Beta: {beta_a['beta']:.2f}, R²: {beta_a['r_squared']:.2f}")
print(f"股票B - Beta: {beta_b['beta']:.2f}, R²: {beta_b['r_squared']:.2f}")

# 计算Beta中性仓位
long_value = 100000  # 多头10万
neutral_pos = hedge.get_neutral_position(
    long_value, 
    beta_a['beta'], 
    beta_b['beta']
)

print(f"\nBeta中性配置:")
print(f"多头: ${neutral_pos['long_value']:,.2f}")
print(f"空头: ${neutral_pos['short_value']:,.2f}")
print(f"对冲比率: {neutral_pos['hedge_ratio']:.2f}")
```

---

### 2. 美元中性 (Dollar Neutral)

**理论基础**
美元中性是指组合中多头和空头的名义金额相等。这是最简单的中性策略，但不一定是Beta中性。

**Python实现**
```python
class DollarNeutralPortfolio:
    """
    美元中性组合管理
    """
    def __init__(self, total_capital):
        """
        参数:
            total_capital: 总资本
        """
        self.total_capital = total_capital
        self.long_positions = {}
        self.short_positions = {}
    
    def add_long_position(self, symbol, value):
        """添加多头仓位"""
        self.long_positions[symbol] = value
    
    def add_short_position(self, symbol, value):
        """添加空头仓位"""
        self.short_positions[symbol] = value
    
    def get_portfolio_status(self):
        """获取组合状态"""
        total_long = sum(self.long_positions.values())
        total_short = sum(self.short_positions.values())
        
        return {
            'total_long': total_long,
            'total_short': total_short,
            'net_exposure': total_long - total_short,
            'gross_exposure': total_long + total_short,
            'is_dollar_neutral': abs(total_long - total_short) < 0.01 * self.total_capital
        }
    
    def rebalance_to_neutral(self):
        """重新平衡至美元中性"""
        status = self.get_portfolio_status()
        total_long = status['total_long']
        total_short = status['total_short']
        
        # 调整至相等
        target = (total_long + total_short) / 2
        
        return {
            'target_per_side': target,
            'long_adjustment': target - total_long,
            'short_adjustment': target - total_short
        }
```

---

### 3. 配对交易 (Pairs Trading)

**理论基础**
配对交易是一种市场中性策略，通过交易两个高度相关的资产，做多相对低估的，做空相对高估的，等待价格回归。

**核心概念**
- **相关性 (Correlation)**: 衡量两个资产价格的线性关系
- **协整 (Cointegration)**: 衡量两个资产价格的长期均衡关系
- **Z-Score**: 衡量价差偏离均值的程度

**Python实现**
```python
from statsmodels.tsa.stattools import coint, adfuller
import numpy as np

class PairsTrading:
    """
    配对交易策略
    """
    def __init__(self, stock_a_prices, stock_b_prices):
        """
        参数:
            stock_a_prices: 股票A价格序列
            stock_b_prices: 股票B价格序列
        """
        self.stock_a = stock_a_prices
        self.stock_b = stock_b_prices
        self.spread = None
        self.zscore = None
    
    def calculate_correlation(self):
        """计算相关系数"""
        return np.corrcoef(self.stock_a, self.stock_b)[0, 1]
    
    def test_cointegration(self):
        """
        协整检验 (Engle-Granger两步法)
        
        返回:
            coint_t: 检验统计量
            p_value: p值
            critical_values: 临界值
        """
        coint_t, p_value, critical_values = coint(self.stock_a, self.stock_b)
        
        return {
            'coint_t': coint_t,
            'p_value': p_value,
            'critical_values': critical_values,
            'is_cointegrated': p_value < 0.05
        }
    
    def calculate_spread(self, method='log'):
        """
        计算价差
        
        参数:
            method: 'log'(对数价差) 或 'price'(价格价差)
        """
        if method == 'log':
            self.spread = np.log(self.stock_a) - np.log(self.stock_b)
        else:
            # 线性回归计算对冲比率
            beta = np.polyfit(self.stock_b, self.stock_a, 1)[0]
            self.spread = self.stock_a - beta * self.stock_b
        
        return self.spread
    
    def calculate_zscore(self, lookback=20):
        """
        计算Z-Score
        
        参数:
            lookback: 回看窗口
        """
        if self.spread is None:
            self.calculate_spread()
        
        rolling_mean = pd.Series(self.spread).rolling(window=lookback).mean()
        rolling_std = pd.Series(self.spread).rolling(window=lookback).std()
        
        self.zscore = (self.spread - rolling_mean) / rolling_std
        
        return self.zscore
    
    def generate_signals(self, entry_threshold=2.0, exit_threshold=0.5):
        """
        生成交易信号
        
        参数:
            entry_threshold: 入场阈值 (Z-Score绝对值)
            exit_threshold: 出场阈值
        
        返回:
            signals: 交易信号序列
        """
        if self.zscore is None:
            self.calculate_zscore()
        
        signals = pd.Series(index=range(len(self.zscore)), dtype='object')
        
        # 信号逻辑
        signals[self.zscore < -entry_threshold] = 'LONG_A_SHORT_B'  # A低估，B高估
        signals[self.zscore > entry_threshold] = 'SHORT_A_LONG_B'   # A高估，B低估
        signals[abs(self.zscore) < exit_threshold] = 'EXIT'
        
        return signals.fillna('HOLD')


# 配对筛选器
class PairsSelector:
    """
    配对筛选器 - 从多只股票中找出最佳配对
    """
    def __init__(self, price_data_df):
        """
        参数:
            price_data_df: 价格数据DataFrame (列为股票)
        """
        self.price_data = price_data_df
        self.pairs = []
    
    def find_cointegrated_pairs(self, p_value_threshold=0.05):
        """
        找出协整配对
        
        参数:
            p_value_threshold: p值阈值
        
        返回:
            协整配对列表
        """
        n = len(self.price_data.columns)
        stocks = self.price_data.columns
        
        cointegrated_pairs = []
        
        for i in range(n):
            for j in range(i+1, n):
                stock_a = stocks[i]
                stock_b = stocks[j]
                
                # 协整检验
                _, p_value, _ = coint(
                    self.price_data[stock_a], 
                    self.price_data[stock_b]
                )
                
                if p_value < p_value_threshold:
                    correlation = np.corrcoef(
                        self.price_data[stock_a], 
                        self.price_data[stock_b]
                    )[0, 1]
                    
                    cointegrated_pairs.append({
                        'pair': (stock_a, stock_b),
                        'p_value': p_value,
                        'correlation': correlation
                    })
        
        # 按p值排序
        cointegrated_pairs.sort(key=lambda x: x['p_value'])
        
        return cointegrated_pairs
```

**使用示例**
```python
# 生成模拟配对数据
np.random.seed(42)
dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')

# 股票A和B高度相关
stock_a = 100 + np.cumsum(np.random.normal(0.001, 0.02, len(dates)))
stock_b = stock_a * 0.5 + np.random.normal(0, 2, len(dates))  # 协整关系

# 初始化配对交易
pairs = PairsTrading(stock_a, stock_b)

# 检验协整
coint_result = pairs.test_cointegration()
print(f"协整检验 - p值: {coint_result['p_value']:.4f}")
print(f"是否协整: {coint_result['is_cointegrated']}")

# 计算相关系数
corr = pairs.calculate_correlation()
print(f"相关系数: {corr:.4f}")

# 生成信号
signals = pairs.generate_signals(entry_threshold=2.0, exit_threshold=0.5)
print(f"\n最新信号: {signals.iloc[-1]}")
print(f"当前Z-Score: {pairs.zscore.iloc[-1]:.2f}")
```

---

### 4. 多因子中性 (Multi-Factor Neutral)

**理论基础**
除了市场Beta，组合还可能暴露于其他风险因子（如价值、动量、规模等）。多因子中性旨在消除对这些因子的暴露。

**Python实现**
```python
class MultiFactorNeutral:
    """
    多因子中性组合构建
    """
    def __init__(self, factor_exposures_df):
        """
        参数:
            factor_exposures_df: 因子暴露矩阵 (股票 × 因子)
        """
        self.factor_exposures = factor_exposures_df
        self.factors = factor_exposures_df.columns
    
    def calculate_portfolio_factor_exposure(self, weights):
        """
        计算组合因子暴露
        
        参数:
            weights: 组合权重
        
        返回:
            各因子暴露
        """
        return self.factor_exposures.T @ weights
    
    def optimize_factor_neutral(self, expected_returns, 
                                target_factors=None,
                                constraints=None):
        """
        构建因子中性组合
        
        参数:
            expected_returns: 预期收益
            target_factors: 需要中性的因子列表 (None表示全部)
            constraints: 其他约束
        
        返回:
            最优权重
        """
        from scipy.optimize import minimize
        
        n_assets = len(expected_returns)
        
        if target_factors is None:
            target_factors = self.factors
        
        # 目标函数: 最大化收益
        def objective(w):
            return -np.dot(w, expected_returns)
        
        # 约束条件
        cons = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 0},  # 美元中性
        ]
        
        # 因子中性约束
        for factor in target_factors:
            factor_exposure = self.factor_exposures[factor].values
            cons.append({
                'type': 'eq', 
                'fun': lambda w, f=factor_exposure: np.dot(w, f)
            })
        
        # 初始权重
        w0 = np.zeros(n_assets)
        
        # 优化
        result = minimize(objective, w0, method='SLSQP', constraints=cons)
        
        return result.x
```

---

### 5. 统计套利综合框架

**Python实现**
```python
class StatisticalArbitrage:
    """
    统计套利综合框架
    """
    def __init__(self, returns_data, market_returns):
        """
        参数:
            returns_data: 资产收益率DataFrame
            market_returns: 市场收益率序列
        """
        self.returns = returns_data
        self.market = market_returns
        self.hedge = BetaNeutralHedge(market_returns)
    
    def analyze_pair(self, stock_a, stock_b):
        """
        分析配对
        
        参数:
            stock_a, stock_b: 两只股票代码
        
        返回:
            综合分析结果
        """
        returns_a = self.returns[stock_a]
        returns_b = self.returns[stock_b]
        
        # Beta分析
        beta_a = self.hedge.calculate_beta(returns_a)
        beta_b = self.hedge.calculate_beta(returns_b)
        
        # 配对交易分析
        prices_a = (1 + returns_a).cumprod()
        prices_b = (1 + returns_b).cumprod()
        
        pairs = PairsTrading(prices_a, prices_b)
        coint_result = pairs.test_cointegration()
        correlation = pairs.calculate_correlation()
        
        # Beta中性仓位
        neutral_pos = self.hedge.get_neutral_position(
            100000, beta_a['beta'], beta_b['beta']
        )
        
        return {
            'stock_a': stock_a,
            'stock_b': stock_b,
            'beta_a': beta_a,
            'beta_b': beta_b,
            'cointegration': coint_result,
            'correlation': correlation,
            'neutral_position': neutral_pos,
            'recommendation': self._generate_recommendation(
                coint_result, correlation, beta_a, beta_b
            )
        }
    
    def _generate_recommendation(self, coint, corr, beta_a, beta_b):
        """生成交易建议"""
        if coint['is_cointegrated'] and corr > 0.8:
            return "STRONG_BUY" if beta_a['beta'] < beta_b['beta'] else "STRONG_SELL"
        elif coint['is_cointegrated']:
            return "BUY" if beta_a['beta'] < beta_b['beta'] else "SELL"
        else:
            return "NEUTRAL"


# 综合风险中性分析器
class NeutralRiskAnalyzer:
    """
    综合风险中性分析器
    """
    def __init__(self, price_data, market_data):
        self.price_data = price_data
        self.returns = price_data.pct_change().dropna()
        self.market_returns = market_data.pct_change().dropna()
        self.stat_arb = StatisticalArbitrage(self.returns, self.market_returns)
    
    def full_analysis(self, stock_a, stock_b):
        """完整分析"""
        analysis = self.stat_arb.analyze_pair(stock_a, stock_b)
        
        report = f"""
风险中性分析报告: {stock_a} vs {stock_b}
{'='*50}

1. Beta分析
   {stock_a}: Beta = {analysis['beta_a']['beta']:.3f}
   {stock_b}: Beta = {analysis['beta_b']['beta']:.3f}

2. 相关性分析
   相关系数: {analysis['correlation']:.3f}

3. 协整检验
   p值: {analysis['cointegration']['p_value']:.4f}
   是否协整: {'是' if analysis['cointegration']['is_cointegrated'] else '否'}

4. Beta中性配置
   多头(${stock_a}): ${analysis['neutral_position']['long_value']:,.2f}
   空头(${stock_b}): ${analysis['neutral_position']['short_value']:,.2f}
   对冲比率: {analysis['neutral_position']['hedge_ratio']:.3f}

5. 交易建议: {analysis['recommendation']}
"""
        return report
```

---

## 使用示例

### 完整分析流程
```python
# 准备数据
price_data = pd.DataFrame({
    'AAPL': aapl_prices,
    'MSFT': msft_prices,
    'GOOGL': googl_prices,
    'SPY': spy_prices
})

# 初始化分析器
analyzer = NeutralRiskAnalyzer(price_data[['AAPL', 'MSFT', 'GOOGL']], 
                                price_data['SPY'])

# 分析配对
result = analyzer.full_analysis('AAPL', 'MSFT')
print(result)

# 寻找最佳配对
selector = PairsSelector(price_data[['AAPL', 'MSFT', 'GOOGL']])
pairs = selector.find_cointegrated_pairs()
print("最佳配对:", pairs[:3])
```

---

## 关键指标解释

### 中性指标
| 指标 | 说明 | 中性标准 |
|------|------|----------|
| Beta | 市场敏感度 | ≈ 0 |
| 净敞口 | 多空差额 | ≈ 0 |
| 总敞口 | 多空总和 | 根据策略 |
| 相关系数 | 价格相关性 | > 0.8 |
| p值 | 协整显著性 | < 0.05 |

### 风险管理原则
1. **Beta中性** - 组合Beta接近0
2. **美元中性** - 多空金额相等
3. **分散化** - 多对配对分散风险
4. **止损** - 价差持续扩大时止损
5. **再平衡** - 定期调整维持中性

---

## 参考资源

### 开源框架
- **PyPortfolioOpt**: 投资组合优化
- **Riskfolio-Lib**: 风险分析和资产配置
- **Statsmodels**: 协整检验和时间序列分析
- **Scipy**: 统计计算

### 理论基础
- Pairs Trading: Vidyamurthy (2004)
- Market Neutral: 对冲基金策略
- Cointegration: Engle-Granger (1987)
- Factor Models: Fama-French

---

## 注意事项

1. **协整不等于相关** - 需要分别检验
2. **Beta是动态的** - 需要定期重新计算
3. **交易成本** - 频繁再平衡会增加成本
4. **极端市场** - 中性策略在极端市场可能失效
5. **杠杆风险** - 多空策略通常涉及杠杆
