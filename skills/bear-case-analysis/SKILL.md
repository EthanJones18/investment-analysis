---
name: bear-case-analysis
description: 专注于挖掘下跌机会和风险点的空头研究分析Skill。深入分析上市公司基本面缺陷、行业衰退信号、估值泡沫等负面因素。通过严谨的逻辑推演识别做空机会，为风险规避和反向投资策略提供依据。
---

# 空头研究分析专家 (Bear Case Analysis)

## 概述

本Skill专注于从空头角度分析资产，挖掘下跌机会和风险点。通过深入分析公司的基本面缺陷、行业衰退信号、估值泡沫等负面因素，识别做空机会，为风险规避和反向投资策略提供严谨的逻辑支撑。

**核心理念**：
1. **风险导向**：优先识别下行风险而非上行机会
2. **证据驱动**：基于财务数据、行业趋势、管理质量的严谨分析
3. **逆向思维**：挑战市场共识，寻找被忽视的负面因素
4. **安全边际**：为做空决策提供充分的逻辑支撑

## 核心功能

### 1. 基本面缺陷分析（必须执行）
- 财务报表异常检测
- 会计红旗识别
- 盈利质量评估
- 现金流分析

### 2. 估值泡沫识别（必须执行）
- 相对估值过高
- 历史估值比较
- 增长预期不切实际
- 估值与基本面脱节

### 3. 行业衰退信号（必须执行）
- 行业周期判断
- 技术替代风险
- 监管政策变化
- 竞争格局恶化

### 4. 管理层风险
- 管理层诚信问题
- 内部人交易异常
- 公司治理缺陷
- 战略决策失误

### 5. 做空机会识别
- 做空目标筛选
- 做空时机判断
- 风险收益评估
- 退出策略设计

## 空头分析框架

### 做空候选筛选标准

| 维度 | 红旗信号 | 权重 |
|------|---------|------|
| **估值** | P/E > 行业均值2倍 | 20% |
| **增长** | 收入增长放缓+库存增加 | 20% |
| **盈利** | 非经常性收益占比高 | 15% |
| **现金流** | 经营现金流持续为负 | 20% |
| **杠杆** | 负债率 > 70% | 15% |
| **治理** | 审计意见非标/管理层变动 | 10% |

### 会计红旗清单

**1. 收入确认问题**
- 应收账款增长快于收入增长
- 收入集中在季度末
- 关联交易收入占比高
- 提前确认收入

**2. 成本费用操纵**
- 资本化费用异常增加
- 折旧摊销政策变更
- 存货计价方法变更
- 费用递延处理

**3. 现金流异常**
- 利润与经营现金流严重背离
- 自由现金流持续为负
- 筹资活动现金流依赖
- 现金及等价物异常波动

**4. 资产负债表风险**
- 商誉占总资产比例过高
- 无形资产异常增加
- 表外负债
- 关联方往来款

### 估值泡沫指标

| 指标 | 泡沫阈值 | 检测方法 |
|------|---------|---------|
| P/E Ratio | > 50 | 与历史均值/行业比较 |
| P/S Ratio | > 10 | 与历史均值/行业比较 |
| PEG Ratio | > 2 | 增长预期合理性 |
| EV/EBITDA | > 20 | 与行业比较 |
| Price/Book | > 5 | 与历史均值比较 |
| Market Cap/GDP | > 200% | 市场整体估值 |

## 数据来源

### 财务数据
- SEC EDGAR数据库
- 公司年报/季报
- 审计报告
- 内部人交易数据

### 市场数据
- 做空比例数据
- 期权市场数据
- 融券数据
- 机构持仓变化

### 另类数据
- 卫星图像
- 供应链数据
- 社交媒体情绪
- 法律诉讼信息

## 使用方法

### 完整空头分析（推荐）

```bash
python scripts/comprehensive_analysis.py \
  --symbol XYZ \
  --analysis-depth full \
  --output ./output
```

### 单独模块分析

#### 基本面缺陷分析

```bash
python scripts/fundamental_red_flags.py \
  --symbol XYZ \
  --years 5 \
  --output ./output
```

#### 估值泡沫检测

```bash
python scripts/valuation_bubble.py \
  --symbol XYZ \
  --industry technology \
  --output ./output
```

#### 行业衰退分析

```bash
python scripts/industry_decline.py \
  --symbol XYZ \
  --sector retail \
  --output ./output
```

#### 做空机会筛选

```bash
python scripts/short_screener.py \
  --market US \
  --min-short-interest 0.10 \
  --output ./output
```

## 空头案例构建

### 案例结构

```
1. 做空主题 (Short Thesis)
   - 核心做空逻辑
   - 关键风险因素
   - 催化剂事件

2. 基本面缺陷 (Fundamental Flaws)
   - 财务异常
   - 会计操纵嫌疑
   - 商业模式问题

3. 估值过高 (Overvaluation)
   - 估值指标分析
   - 历史比较
   - 增长预期不切实际

4. 行业风险 (Industry Risks)
   - 行业周期
   - 技术替代
   - 监管压力

5. 管理层风险 (Management Risks)
   - 诚信问题
   - 能力质疑
   - 内部人交易

6. 做空策略 (Short Strategy)
   - 入场时机
   - 目标价格
   - 止损设置
   - 风险收益比
```

## 评分标准

### 综合空头评分

| 分数 | 评级 | 做空建议 |
|------|------|---------|
| 90-100 | 强烈推荐做空 | 重仓做空 |
| 80-89 | 推荐做空 | 积极做空 |
| 70-79 | 中性偏空 | 适度做空 |
| 60-69 | 中性 | 观望 |
| <60 | 回避 | 不建议做空 |

### 分项评分权重

| 维度 | 权重 | 说明 |
|------|------|------|
| 估值泡沫 | 25% | 估值过高程度 |
| 基本面缺陷 | 25% | 财务质量问题 |
| 行业风险 | 20% | 行业衰退信号 |
| 管理层风险 | 15% | 治理问题 |
| 做空条件 | 15% | 做空可行性 |

## 分析流程

### 标准分析流程

1. **初步筛选**
   - 估值指标筛选
   - 做空比例检查
   - 价格动量分析

2. **深度分析**
   - 财务报表细读
   - 会计政策分析
   - 同业比较

3. **风险识别**
   - 基本面缺陷
   - 估值泡沫
   - 行业风险
   - 管理层风险

4. **做空评估**
   - 做空可行性
   - 风险收益比
   - 催化剂识别
   - 退出策略

5. **报告生成**
   - 空头案例构建
   - 目标价设定
   - 风险警示
   - 做空建议

## 参考项目

本Skill参考了以下开源项目和研究：

- [shortsqueeze](https://github.com/samgozman/shortsqueeze) - 做空数据获取
- [FraudDetection](https://github.com/JarFraud/FraudDetection) - 会计欺诈检测
- [Short-Squeeze-Predictor](https://github.com/mandarl/Short-Squeeze-Predictor) - 轧空预测
- [Accounting-Fraud-Detection](https://github.com/rebeccazhang199/Accounting-Fraud-Detection) - 会计欺诈检测
- [financial-fraud-detection](https://github.com/NVIDIA-AI-Blueprints/financial-fraud-detection) - 金融欺诈检测

## 高级功能

详细的高级功能说明请参考：

- [会计红旗识别](references/accounting_red_flags.md)
- [估值泡沫检测](references/valuation_bubble.md)
- [行业衰退分析](references/industry_decline.md)
- [做空策略设计](references/short_strategy.md)
