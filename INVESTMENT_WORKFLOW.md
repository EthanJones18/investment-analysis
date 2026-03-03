# 投资分析 Workflow

## 概述

本文档定义了标准的投资分析 workflow，用于系统化地对投资标的进行全面分析和决策。

## Workflow 结构

```
基础分析 → 多空分析 → 综合决策/交易员 → 风险评估 → 投资计划
    ↓          ↓              ↓              ↓            ↓
macro/     bull/bear    investment/     risk-       investment
fundamental/   case      decision/      decision        plan
technical/            trading
market-
intelligence
geopolitical-
analysis
```

## 各层详细说明

### 第一层：基础分析（5个 Skills）

| Skill | 功能 | 输出 |
|-------|------|------|
| **macro-analyst** | 宏观经济分析 | 宏观环境评估报告 |
| **fundamental-analysis** | 基本面分析 | 财务分析、估值报告 |
| **technical-analysis** | 技术分析 | 技术形态、趋势判断 |
| **market-intelligence** | 市场信息分析 | 情绪、资金流向分析 |
| **geopolitical-analysis** | 地缘政治分析 | 地缘风险影响评估 |

### 第二层：多空分析（2个 Skills）

| Skill | 功能 | 输出 |
|-------|------|------|
| **bull-case-analysis** | 多头分析 | 上行机会、增长潜力 |
| **bear-case-analysis** | 空头分析 | 下行风险、估值泡沫 |

### 第三层：综合决策 + 交易员（2个 Skills）

| Skill | 功能 | 输出 |
|-------|------|------|
| **investment-decision** | 投资决策分析 | 综合评分、投资建议 |
| **investment-trading** | 交易员执行 | 交易计划、仓位管理、入场出场策略 |

### 第四层：风险评估（4个 Skills）

| Skill | 功能 | 输出 |
|-------|------|------|
| **risk-decision-analysis** | 综合风险决策分析 | 三维风险评分、博弈论推演 |
| **aggressive-risk-analysis** | 激进型风险分析 | 高风险视角评估（高风险高收益） |
| **conservative-risk-analysis** | 保守型风险分析 | 低风险视角评估（本金安全优先） |
| **neutral-risk-analysis** | 中性型风险分析 | 平衡视角评估（风险收益平衡） |

### 第五层：投资计划（1个 Skill）

| Skill | 功能 | 输出 |
|-------|------|------|
| **investment-plan** | 投资计划生成 | 完整投资计划书 |

## Workflow 执行顺序

```
Step 1: 基础分析（可并行执行）
  ├── macro-analyst
  ├── fundamental-analysis
  ├── technical-analysis
  ├── market-intelligence
  └── geopolitical-analysis

Step 2: 多空分析（可并行执行）
  ├── bull-case-analysis
  └── bear-case-analysis

Step 3: 综合决策 + 交易员执行
  ├── investment-decision
  │   （整合 Step 1 和 Step 2 的结果，生成综合评分和投资建议）
  └── investment-trading
      （基于决策制定交易计划：入场、仓位、出场策略）

Step 4: 风险评估
  └── risk-decision-analysis
      （激进/保守/中性三维分析 + 博弈论推演）

Step 5: 投资计划
  └── investment-plan
      （整合所有分析结果，生成最终投资计划书）
```

## 使用规范

### 标准分析流程

1. **确定标的**：明确分析的股票代码
2. **选择深度**：quick（快速）或 full（完整）
3. **设定风险偏好**：aggressive / conservative / neutral
4. **按序执行**：按 workflow 顺序依次调用各 skill
5. **整合输出**：最终生成投资计划书

### 输出格式

- JSON：结构化数据，用于程序处理
- Markdown：可读报告，用于人工阅读

### 质量检查

- 各 skill 输出是否完整
- 数据是否一致
- 逻辑是否通顺
- 建议是否可执行

### 报告内容要求（强制）

**每个 Skill 的报告必须包含：**

1. **推理过程（Process）**
   - 分析框架和方法论
   - 数据收集和处理步骤
   - 逻辑推导链条
   - 关键假设和前提条件

2. **决策依据（Rationale）**
   - 评分标准和权重分配
   - 关键指标的计算过程
   - 多空因素的权衡分析
   - 置信度评估

3. **结果内容（Results）**
   - 具体评分（0-100分）
   - 关键数据指标
   - 明确的结论和建议
   - 风险提示

4. **模块间推理逻辑（Module Linkage）**
   - 本模块输入数据的来源和依据
   - 本模块输出结果如何影响下一模块
   - 模块间的数据流转和逻辑衔接
   - 关键结论的传递路径

   **示例：**
   ```markdown
   ### 模块间推理逻辑
   
   **输入来源：**
   - 接收自基础分析层的宏观评分（70.5分）
   - 接收自基本面分析的现金储备数据（$3,730亿）
   
   **本模块处理：**
   - 基于宏观评分判断利率环境对浮存金的影响
   - 结合现金储备评估安全边际
   
   **输出传递：**
   - 向投资决策层输出：宏观环境利好浮存金收益
   - 向风险评估层输出：现金储备提供下行保护
   ```

5. **数据时效性要求（Data Freshness）**
   - **必须使用当天最新市场数据**
   - 股价、市值等实时数据：分析当日的收盘价/实时价
   - 财务数据：最新季度/年度财报
   - 宏观数据：最新发布的经济指标
   - 新闻事件：分析当日及前一日的重要公告
   
   **数据检查清单：**
   - [ ] 股价数据是否为当日最新？
   - [ ] 财务数据是否为最新季度？
   - [ ] 宏观指标是否为最新发布？
   - [ ] 是否有当日重大新闻/公告？
   - [ ] 分析师评级是否为最新？

**示例结构：**
```markdown
## Skill名称分析

### 推理过程
Step 1: ...
Step 2: ...
Step 3: ...

### 决策依据
- 评分标准: ...
- 权重分配: ...
- 关键计算: ...

### 结果内容
- 评分: XX/100
- 关键指标: ...
- 结论: ...
- 风险: ...

### 模块间推理逻辑
**输入来源：** ...
**本模块处理：** ...
**输出传递：** ...

### 数据时效性声明
- 分析日期: YYYY-MM-DD
- 股价数据: $XX.XX (当日收盘价)
- 财务数据: 20XX年QX财报
- 数据来源: [具体来源]
```

## 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-03-03 | 1.0 | 初始版本，定义标准 investment workflow |
