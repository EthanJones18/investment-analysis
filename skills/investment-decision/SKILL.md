---
name: investment-decision
description: 综合投资决策分析Skill。整合宏观分析、基本面分析、技术分析、市场信息分析、地缘政治分析、多头分析、空头分析七大维度，对资产标的进行全面深度的投资决策分析，给出最终的具体投资建议。
---

# 投资决策专家 (Investment Decision)

## 概述

本Skill是一个综合投资决策分析框架，整合宏观分析、基本面分析、技术分析、市场信息分析、地缘政治分析、多头分析、空头分析七大维度，对资产标的进行全面深度的投资决策分析，给出最终的具体投资建议。

**核心理念**：
1. **多维度分析**：从宏观到微观，从基本面到技术面，全方位评估
2. **量化评分**：每个维度独立评分，综合加权得出最终建议
3. **风险优先**：优先识别下行风险，再评估上行机会
4. ** actionable**：给出具体可操作的投资建议

## 分析维度

### 1. 宏观分析 (Macro Analysis) - 权重15%
- 全球经济形势
- 货币政策环境
- 利率走势
- 通胀预期

### 2. 基本面分析 (Fundamental Analysis) - 权重25%
- 财务报表分析
- 盈利能力评估
- 成长性分析
- 估值合理性

### 3. 技术分析 (Technical Analysis) - 权重15%
- 趋势判断
- 支撑阻力位
- 技术指标
- 量价关系

### 4. 市场信息分析 (Market Intelligence) - 权重15%
- 市场情绪
- 资金流向
- 新闻事件
- 社交媒体情绪

### 5. 地缘政治分析 (Geopolitical Analysis) - 权重10%
- 地缘政治风险
- 政策风险
- 国际关系
- 区域冲突

### 6. 多头分析 (Bull Case Analysis) - 权重10%
- 增长机会
- 竞争优势
- 创新驱动
- 市场拓展

### 7. 空头分析 (Bear Case Analysis) - 权重10%
- 估值泡沫
- 基本面缺陷
- 行业风险
- 治理风险

## 评分体系

### 各维度评分标准

| 维度 | 权重 | 评分范围 | 数据来源 |
|------|------|---------|---------|
| 宏观分析 | 15% | 0-100 | 宏观经济数据 |
| 基本面分析 | 25% | 0-100 | 财务报表 |
| 技术分析 | 15% | 0-100 | 价格数据 |
| 市场信息 | 15% | 0-100 | 新闻/社交媒体 |
| 地缘政治 | 10% | 0-100 | 事件数据 |
| 多头分析 | 10% | 0-100 | 基本面/行业 |
| 空头分析 | 10% | 0-100 | 风险因素 |

### 综合评分计算

```
综合评分 = Σ(维度评分 × 维度权重)

投资建议生成:
- 90-100: 强烈买入
- 80-89: 买入
- 70-79: 增持
- 60-69: 持有
- 50-59: 减持
- 40-49: 卖出
- <40: 强烈卖出
```

## 投资决策矩阵

| 综合评分 | 建议 | 仓位 | 止损 | 目标收益 |
|---------|------|------|------|---------|
| 90-100 | 强烈买入 | 20-30% | -8% | +30% |
| 80-89 | 买入 | 15-20% | -7% | +25% |
| 70-79 | 增持 | 10-15% | -6% | +20% |
| 60-69 | 持有 | 5-10% | -5% | +15% |
| 50-59 | 减持 | 0-5% | - | - |
| 40-49 | 卖出 | 清仓 | - | - |
| <40 | 强烈卖出 | 做空/对冲 | - | - |

## 使用方法

### 完整投资决策分析

```bash
python scripts/comprehensive_decision.py \
  --symbol BABA \
  --analysis-depth full \
  --output ./output
```

### 快速分析

```bash
python scripts/quick_decision.py \
  --symbol BABA \
  --output ./output
```

### 对比分析

```bash
python scripts/comparative_analysis.py \
  --symbols BABA,TCEHY,JD \
  --output ./output
```

## 分析报告结构

### 1. 执行摘要
- 投资建议
- 综合评分
- 关键结论

### 2. 多维度分析
- 各维度详细分析
- 评分与权重
- 关键发现

### 3. 风险收益评估
- 上行潜力
- 下行风险
- 风险收益比

### 4. 投资建议
- 具体操作建议
- 仓位建议
- 止损止盈
- 时间周期

### 5. 监控指标
- 关键监控指标
- 催化剂事件
- 风险预警

## 参考项目

本Skill参考了以下开源项目和研究：

- [Microsoft Qlib](https://github.com/microsoft/qlib) - AI量化投资平台
- [Deep Research Agent for Finance](https://github.com/The-AI-Alliance/deep-research-agent-for-finance) - AI金融研究
- [FinSight](https://github.com/RUC-NLPIR/FinSight) - 多智能体金融研究系统
- [Equity Research Analysis](https://github.com/aameerk/Equity-Research-Analysis-using-Langchain) - 自动化股票研究

## 高级功能

详细的高级功能说明请参考：

- [多维度分析指南](references/multi_dimension_analysis.md)
- [评分体系说明](references/scoring_system.md)
- [投资决策矩阵](references/decision_matrix.md)
- [风险管理](references/risk_management.md)
