---
name: market-intelligence
description: 专注于市场信息分析的Skill。从情绪和消息面的维度对资产进行分析，收集和解读最新的市场新闻、社交媒体情绪、另类数据等信息，评估这些因素对资产价格的潜在影响。支持新闻情绪分析、社交媒体监控、事件研究、舆情追踪等功能。当用户需要进行市场情绪分析、消息面解读、舆情监控、事件驱动分析或另类数据研究时触发此Skill。
---

# 市场信息分析专家 (Market Intelligence)

## 概述

本Skill专注于从情绪和消息面维度分析资产，通过收集和解读市场新闻、社交媒体情绪、另类数据等信息，评估其对资产价格的潜在影响。

**核心原则**：每次执行市场信息分析时，必须同时执行以下两个深度检索：
1. **社交媒体监控**：Twitter/X、Reddit、雪球、股吧等平台
2. **权威资讯爬取**：Bloomberg、Reuters、WSJ、财新、第一财经等权威媒体

## 核心功能

### 1. 新闻情绪分析
- 实时新闻采集与情绪打分
- 财经新闻情感倾向分析
- 重大事件识别与影响评估
- 新闻热度追踪

### 2. 社交媒体监控（必须执行）
- Twitter/X、Reddit等平台情绪监控
- 股吧、雪球等中文社区舆情分析
- 社交媒体热点追踪
- 意见领袖(KOL)观点汇总

### 3. 权威资讯爬取（必须执行）
- Bloomberg、Reuters、WSJ等国际权威媒体
- 财新、第一财经、财经等国内权威媒体
- 新闻源权重评估
- 关键事件提取

### 4. 深度解读分析（新增）
- **重点资讯深度解读**：单条新闻影响分析、分类别洞察、市场主线识别
- **社交媒体情绪解读**：平台差异分析、情绪变化解读、散户vs机构对比
- **逆向投资信号**：基于情绪极值的买卖信号、策略建议、风险管理
- **行动建议**：可执行的投资行动清单

### 5. 事件研究
- 财报季事件分析
- 政策公告影响评估
- 突发事件市场反应
- 历史事件回测

### 6. 情绪指标构建
- 综合情绪指数
- 恐慌/贪婪指数
- 多空情绪比
- 情绪动量指标

## 使用方法

### 完整市场信息分析（推荐）

执行完整的市场信息分析，自动包含社交媒体监控和权威资讯爬取：

```bash
python scripts/comprehensive_analysis.py \
  --symbol AAPL \
  --days 7 \
  --output ./output
```

### 单独模块分析

#### 新闻情绪分析

```bash
python scripts/news_sentiment.py \
  --symbol AAPL \
  --sources bloomberg,reuters,seekingalpha \
  --days 7 \
  --output ./output
```

#### 社交媒体监控

```bash
python scripts/social_media_monitor.py \
  --symbol AAPL \
  --platform twitter,reddit,xueqiu,guba \
  --hours 24 \
  --output ./output
```

#### 权威资讯爬取

```bash
python scripts/authority_news_crawler.py \
  --symbol AAPL \
  --sources bloomberg,reuters,cnbc,seekingalpha,caixin \
  --days 7 \
  --output ./output
```

#### 事件研究

```bash
python scripts/event_study.py \
  --symbol AAPL \
  --event earnings \
  --date 2025-01-30 \
  --window 30 \
  --output ./output
```

#### 情绪指数构建

```bash
python scripts/sentiment_index.py \
  --symbol AAPL \
  --components news,social,options \
  --output ./output
```

#### 深度解读分析

```bash
python scripts/market_intelligence_analysis.py \
  --symbol AAPL \
  --data-file ./output/AAPL_comprehensive_analysis.json \
  --report-type comprehensive \
  --output ./output
```

**深度解读分析包含**：
- 重点资讯深度解读（单条新闻影响、分类别洞察、市场主线）
- 社交媒体情绪解读（平台差异、情绪变化、散户vs机构对比）
- 逆向投资信号生成
- 可执行的行动建议

## 情绪分析模型

### VADER模型
- 专为社交媒体设计
- 支持表情符号、俚语
- 无需训练数据
- 适合实时分析

### FinBERT模型
- 金融领域专用BERT
- 针对财经文本训练
- 情绪分类更精准
- 适合新闻分析

### TextBlob模型
- 简单易用
- 基于词典方法
- 适合快速原型
- 支持多语言

## 情绪评分标准

| 分数范围 | 情绪 | 投资建议 |
|---------|------|---------|
| 0.5 ~ 1.0 | 极度乐观 | 警惕过热 |
| 0.2 ~ 0.5 | 乐观 | 偏多 |
| -0.2 ~ 0.2 | 中性 | 观望 |
| -0.5 ~ -0.2 | 悲观 | 偏空 |
| -1.0 ~ -0.5 | 极度悲观 | 警惕恐慌 |

## 事件类型分析

### 财报事件
- 业绩超预期/低于预期
- 指引上调/下调
- 管理层表态
- 分析师反应

### 政策事件
- 监管政策变化
- 货币政策调整
- 行业政策出台
- 贸易政策变动

### 公司事件
- 并购重组
- 高管变动
- 产品发布
- 法律诉讼

### 宏观事件
- 经济数据发布
- 地缘政治事件
- 自然灾害
- 疫情发展

## 另类数据来源

### 卫星数据
- 停车场车辆数（零售）
- 工厂开工率（制造业）
- 油轮追踪（能源）
- 农作物长势（农业）

### 消费数据
- 信用卡交易
- 电商销售
- 机票酒店预订
- 餐厅预订

### 网络数据
- 搜索趋势
- 网站流量
- APP下载量
- 社交媒体活跃度

## 情绪指标应用

### 逆向投资信号
- 极度悲观时买入
- 极度乐观时卖出
- 情绪拐点捕捉

### 趋势确认
- 情绪与价格共振
- 情绪领先价格
- 情绪背离预警

### 风险管理
- 情绪极端值预警
- 波动率预测
- 仓位调整依据

## 分析流程

### 标准分析流程

1. **数据收集**
   - 新闻源采集
   - 社交媒体抓取
   - 另类数据获取

2. **情绪计算**
   - 文本预处理
   - 情绪模型打分
   - 情绪聚合

3. **事件识别**
   - 重大事件检测
   - 事件分类
   - 影响评估

4. **指标构建**
   - 情绪指数计算
   - 历史分位数
   - 趋势判断

5. **投资决策**
   - 信号生成
   - 风险提示
   - 策略建议

## 参考项目

本Skill参考了以下开源项目：

- [Stock_Market_Sentiment_Analysis](https://github.com/algosenses/Stock_Market_Sentiment_Analysis) - 股市情感分析
- [A_Share_investment_Agent](https://github.com/24mlight/A_Share_investment_Agent) - 情感分析智能体
- [Earnings_Call_Analyzed_By_NLP](https://github.com/nilijing/Earnings_Call_Analyzed_By_NLP) - 财报电话会议NLP分析
- [NLP-Sentiment-Analysis-of-Earnings-Call](https://github.com/amberwalker-ds/NLP-Sentiment-Analysis-of-Earnings-Call-Transcripts) - 财报情绪分析

## 高级功能

详细的高级功能说明请参考：

- [情绪分析模型指南](references/sentiment_models.md)
- [另类数据手册](references/alternative_data.md)
- [事件研究方法](references/event_study.md)
