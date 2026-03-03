# 开源宏观分析工具参考

本文档汇总GitHub上优秀的宏观分析相关开源项目，为宏观分析提供工具和方法参考。

---

## 数据获取类工具

### 1. AKShare - 中国金融数据接口库

**GitHub**: https://github.com/akfamily/akshare

**功能特点**:
- 提供全面的中国宏观数据接口
- 涵盖GDP、CPI、PPI、PMI、LPR、货币供应量等核心指标
- 支持财经新闻数据获取（财联社、新闻联播等）
- 免费开源，Python接口简洁

**宏观数据覆盖**:
- 国民经济核算（GDP、工业增加值）
- 价格指数（CPI、PPI、企业商品价格指数）
- 货币金融（LPR、货币供应量、社会融资规模）
- 就业与工资（城镇调查失业率）
- 对外贸易（进出口、外商直接投资）

**参考价值**: 中国宏观分析的首选数据源

---

### 2. FRED API - 美联储经济数据

**GitHub**: https://github.com/alihanucar/fredapi

**功能特点**:
- 访问美联储80万+经济时间序列数据
- 覆盖美国及全球主要经济体宏观数据
- 支持多种数据格式导出
- 提供Python、Go等多种语言客户端

**数据覆盖**:
- 就业数据（非农就业、失业率、工资增长）
- 通胀数据（CPI、PCE、核心通胀）
- 经济增长（GDP、零售销售、工业产出）
- 货币政策（联邦基金利率、资产负债表）
- 房地产市场（房价指数、新屋开工）

**参考价值**: 美国及全球宏观分析的标准数据源

---

### 3. qstock - 个人量化投研分析库

**GitHub**: https://github.com/tkfy920/qstock

**功能特点**:
- 数据获取、可视化、选股、回测一体化
- 宏观指标模块提供GDP、CPI、PPI、PMI等数据
- 财经新闻文本数据支持
- 交互式可视化图表

**宏观相关功能**:
- `macro_data()`: 获取GDP、CPI、PPI、PMI、货币供应量、LPR
- `ib_rate()`: 获取全球同业拆借利率（SHIBOR、LIBOR等）
- `news_data()`: 获取财联社、金十数据、新闻联播等
- `north_money()`: 北向资金流向分析

**参考价值**: 适合中国市场的快速宏观数据获取

---

## 分析框架类工具

### 4. OpenBB Terminal - 开源投资研究终端

**GitHub**: https://github.com/OpenBB-finance/OpenBB

**功能特点**:
- 专业级开源投资研究平台
- 集成宏观分析模块（Economy菜单）
- 支持多数据源接入
- 提供Python SDK和API接口

**宏观分析功能**:
- 经济指标查询（GDP、CPI、失业率等）
- 央行政策追踪
- 收益率曲线分析
- 汇率与大宗商品监控
- 经济日历与事件追踪

**参考价值**: 机构级宏观分析工具的开源替代方案

---

### 5. QuantsPlaybook - 券商金工研报复现

**GitHub**: https://github.com/hugo2046/QuantsPlaybook

**功能特点**:
- 复现100+个量化投资策略
- 涵盖择时、因子构建、组合优化四大领域
- 基于A股市场真实数据验证
- 提供详细研报和代码

**宏观相关策略**:
- **择时策略25+**: RSRS、QRS、HHT模型、扩散指标等
- **因子构建22+**: 筹码分布、凸显性因子(STR)、球队硬币因子等
- **组合优化**: DE进化算法、多任务学习等

**核心方法论**:
- RSRS（阻力支撑相对强度）择时
- HHT（希尔伯特-黄变换）趋势识别
- 行为金融因子（处置效应、凸显性等）
- 市场微观结构分析

**参考价值**: 量化宏观分析与择时的成熟方法论

---

### 6. Claude Code Stock Deep Research Agent

**GitHub**: https://github.com/liangdabiao/Claude-Code-Stock-Deep-Research-Agent

**功能特点**:
- 基于Claude Code的多Agent研究系统
- 8阶段股票投资尽调框架
- 28个并行研究智能体
- 多空平衡、明确风险、数据验证

**研究框架**:
1. 公司概况与业务模式
2. 财务分析
3. 行业分析
4. 竞争格局
5. 估值分析
6. 风险评估
7. 管理层分析
8. 投资建议

**参考价值**: AI驱动的深度研究方法论

---

## 技术实现参考

### 数据获取最佳实践

```python
# AKShare 获取中国宏观数据示例
import akshare as ak

# GDP数据
gdp_df = ak.macro_china_gdp()

# CPI数据
cpi_df = ak.macro_china_cpi()

# PMI数据
pmi_df = ak.macro_china_pmi()

# LPR利率
lpr_df = ak.macro_china_lpr()
```

```python
# qstock 获取宏观数据示例
import qstock as qs

# 各类宏观数据
gdp = qs.macro_data('gdp')
cpi = qs.macro_data('cpi')
ppi = qs.macro_data('ppi')
pmi = qs.macro_data('pmi')
money_supply = qs.macro_data('ms')
lpr = qs.macro_data('lpr')

# 财经新闻
news = qs.news_data()  # 财联社电报
cctv_news = qs.news_data('cctv')  # 新闻联播
```

### 分析框架实现参考

```python
# RSRS择时指标简化实现思路
import numpy as np
import pandas as pd

def calculate_rsrs(high, low, n=18):
    """
    阻力支撑相对强度(RSRS)指标
    参考：光大证券《择时系列报告之一》
    """
    # 计算N日最高价和最低价的线性回归斜率
    # 斜率代表支撑阻力的相对强度
    # 具体实现需结合研报细节
    pass

def calculate_hht_signal(price_series):
    """
    HHT模型信号生成
    参考：招商证券《技术择时系列研究》
    """
    # 使用希尔伯特-黄变换进行模态分解
    # 识别趋势和周期成分
    # 结合分类算法生成交易信号
    pass
```

---

## 数据源对比

| 工具 | 数据覆盖 | 更新频率 | 费用 | 适用场景 |
|------|---------|---------|------|---------|
| AKShare | 中国宏观+市场 | 实时/日 | 免费 | 中国宏观分析 |
| FRED API | 美国+全球宏观 | 日/周/月 | 免费 | 美国宏观分析 |
| qstock | 中国宏观+市场 | 实时 | 免费 | 快速数据获取 |
| OpenBB | 全球多资产 | 实时 | 免费 | 综合研究平台 |
| QuantsPlaybook | 策略方法论 | - | 免费 | 量化策略研究 |

---

## 推荐阅读

### 券商研报系列
- 光大证券《择时系列报告》（RSRS、QRS）
- 招商证券《技术择时系列研究》（HHT模型）
- 华泰证券《人工智能系列》（因子模型）
- 广发证券《多因子Alpha系列》（筹码分布）
- 方正证券《多因子选股系列》（球队硬币因子）

### 经典书籍
- 《主动投资组合管理》(Grinold & Kahn)
- 《量化投资策略》(Edward Qian)
- 《构建量化动量选股系统的实用指南》
