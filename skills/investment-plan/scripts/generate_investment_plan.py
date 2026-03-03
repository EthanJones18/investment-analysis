#!/usr/bin/env python3
"""
综合投资计划生成脚本
整合投资决策、投资交易、风险决策分析的结果，生成完整的投资计划提案
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class InvestmentThesis:
    """投资主题"""
    core_logic: str
    key_assumptions: List[Dict]
    catalysts_short: List[str]
    catalysts_medium: List[str]
    catalysts_long: List[str]

@dataclass
class TradingStrategy:
    """交易策略"""
    entry_conditions: List[str]
    entry_price_range: Dict[str, float]
    entry_timing: str
    position_sizing_method: str
    initial_position: str
    pyramiding_plan: List[Dict]
    take_profit_strategy: str
    stop_loss_strategy: str

@dataclass
class RiskManagement:
    """风险管理"""
    risk_matrix: List[Dict]
    position_limits: Dict
    stop_loss_levels: Dict
    emergency_plans: List[Dict]

@dataclass
class ExecutionPlan:
    """执行方案"""
    timeline: List[Dict]
    checklists: Dict[str, List[str]]
    responsibilities: Dict[str, str]

@dataclass
class InvestmentPlan:
    """投资计划"""
    symbol: str
    plan_date: str
    version: str
    
    # 分析输入
    decision_analysis: Dict
    trading_analysis: Dict
    risk_analysis: Dict
    
    # 计划内容
    thesis: InvestmentThesis
    strategy: TradingStrategy
    risk_management: RiskManagement
    execution: ExecutionPlan
    
    # 监控调整
    monitoring_metrics: List[str]
    adjustment_triggers: List[Dict]
    review_schedule: Dict
    
    # 综合评估
    plan_quality_score: float
    recommendation: str
    priority: str

class InvestmentPlanGenerator:
    """投资计划生成器"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.plan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def load_analysis_results(self, decision_file: str, trading_file: str, risk_file: str) -> tuple:
        """加载分析结果"""
        try:
            with open(decision_file, 'r', encoding='utf-8') as f:
                decision = json.load(f)
        except:
            decision = self._generate_default_decision()
        
        try:
            with open(trading_file, 'r', encoding='utf-8') as f:
                trading = json.load(f)
        except:
            trading = self._generate_default_trading()
        
        try:
            with open(risk_file, 'r', encoding='utf-8') as f:
                risk = json.load(f)
        except:
            risk = self._generate_default_risk()
        
        return decision, trading, risk
    
    def _generate_default_decision(self) -> Dict:
        """生成默认决策分析"""
        return {
            "symbol": self.symbol,
            "composite_score": 75,
            "recommendation": "增持",
            "risk_level": "中等",
            "analysis_dimensions": {
                "macro": {"score": 70, "outlook": "中性偏多"},
                "fundamental": {"score": 80, "outlook": "积极"},
                "technical": {"score": 75, "outlook": "上升趋势"},
                "market_intelligence": {"score": 72, "outlook": "情绪积极"},
                "geopolitical": {"score": 65, "outlook": "风险可控"},
                "bull_case": {"score": 78, "outlook": "增长机会明确"},
                "bear_case": {"score": 70, "outlook": "风险可控"}
            }
        }
    
    def _generate_default_trading(self) -> Dict:
        """生成默认交易分析"""
        return {
            "symbol": self.symbol,
            "entry_strategy": {
                "price_range": {"min": 150, "ideal": 155, "max": 160},
                "timing": "回调入场",
                "conditions": ["价格回调至支撑位", "成交量萎缩", "技术指标企稳"]
            },
            "position_management": {
                "initial_size": "10%",
                "max_size": "20%",
                "pyramiding": "金字塔加仓"
            },
            "exit_strategy": {
                "take_profit": ["+15%减仓25%", "+25%减仓25%", "+35%清仓"],
                "stop_loss": "-10%"
            }
        }
    
    def _generate_default_risk(self) -> Dict:
        """生成默认风险分析"""
        return {
            "symbol": self.symbol,
            "risk_profiles": {
                "aggressive": {"score": 80, "suitable": True},
                "conservative": {"score": 65, "suitable": False},
                "neutral": {"score": 75, "suitable": True}
            },
            "var_95": -0.12,
            "max_drawdown": -0.18,
            "sharpe_ratio": 1.2,
            "risk_level": "中等"
        }
    
    def generate_thesis(self, decision: Dict, risk: Dict) -> InvestmentThesis:
        """生成投资主题"""
        # 根据分析结果生成核心逻辑
        composite_score = decision.get('composite_score', 75)
        
        if composite_score >= 80:
            core_logic = f"""
            {self.symbol}具备强劲的投资价值。基本面稳健，行业地位领先，
            技术面呈现上升趋势，风险收益比合理。建议积极配置。
            """
        elif composite_score >= 70:
            core_logic = f"""
            {self.symbol}具备较好的投资机会。基本面良好，估值合理，
            存在一定的上涨催化剂，风险可控。建议适度配置。
            """
        else:
            core_logic = f"""
            {self.symbol}投资价值一般。需关注风险因素，
            建议谨慎参与或观望。
            """
        
        return InvestmentThesis(
            core_logic=core_logic.strip(),
            key_assumptions=[
                {"assumption": "宏观经济保持稳定", "verification": "GDP增速、就业数据", "risk": "衰退风险"},
                {"assumption": "行业增长符合预期", "verification": "行业报告、订单数据", "risk": "增长不及预期"},
                {"assumption": "公司竞争力维持", "verification": "市场份额、财报数据", "risk": "竞争加剧"}
            ],
            catalysts_short=[
                "季度财报发布",
                "新产品上市",
                "重大合同签订"
            ],
            catalysts_medium=[
                "产能扩张完成",
                "新市场开拓",
                "行业政策出台"
            ],
            catalysts_long=[
                "技术突破",
                "行业整合",
                "国际化扩张"
            ]
        )
    
    def generate_strategy(self, trading: Dict, risk: Dict) -> TradingStrategy:
        """生成交易策略"""
        entry = trading.get('entry_strategy', {})
        position = trading.get('position_management', {})
        exit_strat = trading.get('exit_strategy', {})
        
        return TradingStrategy(
            entry_conditions=[
                "投资决策综合评分 ≥ 70分",
                "价格进入目标区间",
                "技术形态符合要求",
                "风险收益比 ≥ 1:3",
                "流动性充足"
            ],
            entry_price_range={
                "ideal": entry.get('price_range', {}).get('ideal', 155),
                "min": entry.get('price_range', {}).get('min', 150),
                "max": entry.get('price_range', {}).get('max', 160)
            },
            entry_timing=entry.get('timing', '回调入场'),
            position_sizing_method="风险比例法",
            initial_position=position.get('initial_size', '10%'),
            pyramiding_plan=[
                {"order": 1, "size": "30%", "trigger": "达到入场条件"},
                {"order": 2, "size": "20%", "trigger": "盈利10%后"},
                {"order": 3, "size": "15%", "trigger": "盈利20%后"},
                {"order": 4, "size": "10%", "trigger": "盈利30%后"}
            ],
            take_profit_strategy="分批止盈：+15%减仓25%，+25%减仓25%，+35%清仓",
            stop_loss_strategy=f"固定止损：{exit_strat.get('stop_loss', '-10%')}"
        )
    
    def generate_risk_management(self, risk: Dict) -> RiskManagement:
        """生成风险管理方案"""
        return RiskManagement(
            risk_matrix=[
                {"type": "市场风险", "description": "市场整体下跌", "probability": "中", "impact": "高", "level": "高"},
                {"type": "行业风险", "description": "行业政策变化", "probability": "低", "impact": "高", "level": "中"},
                {"type": "公司风险", "description": "业绩不及预期", "probability": "中", "impact": "高", "level": "高"},
                {"type": "流动性风险", "description": "无法及时成交", "probability": "低", "impact": "中", "level": "低"}
            ],
            position_limits={
                "single_stock_max": "20%",
                "single_industry_max": "40%",
                "risk_per_trade": "2%"
            },
            stop_loss_levels={
                "initial": "-10%",
                "trailing": "盈利20%后上移至成本价",
                "time_based": "60天未达预期评估退出"
            },
            emergency_plans=[
                {"scenario": "闪崩", "action": "暂停交易，评估风险，考虑对冲"},
                {"scenario": "流动性危机", "action": "降低仓位，转向流动性好的标的"},
                {"scenario": "黑天鹅事件", "action": "启动应急止损，全面风险评估"}
            ]
        )
    
    def generate_execution(self) -> ExecutionPlan:
        """生成执行方案"""
        return ExecutionPlan(
            timeline=[
                {"phase": "准备阶段", "time": "T-7天", "task": "完成分析、制定计划", "deliverable": "投资计划书"},
                {"phase": "审批阶段", "time": "T-3天", "task": "计划审批、资金准备", "deliverable": "审批文件"},
                {"phase": "建仓阶段", "time": "T日", "task": "首次建仓", "deliverable": "成交确认"},
                {"phase": "监控阶段", "time": "T+1起", "task": "持续监控、动态调整", "deliverable": "监控报告"}
            ],
            checklists={
                "pre_entry": [
                    "投资计划已审批",
                    "资金已到位",
                    "交易权限已确认",
                    "风险限额已设定",
                    "止损单已准备"
                ],
                "entry": [
                    "价格符合计划区间",
                    "流动性充足",
                    "仓位大小符合计划",
                    "止损单已设置",
                    "交易记录已保存"
                ],
                "holding": [
                    "每日监控价格",
                    "关注新闻事件",
                    "评估风险状况",
                    "检查止损有效性",
                    "记录交易日志"
                ]
            },
            responsibilities={
                "analyst": "完成分析、制定计划",
                "portfolio_manager": "计划审批、资金配置",
                "trader": "执行交易",
                "risk_manager": "风险监控"
            }
        )
    
    def calculate_plan_quality(self, decision: Dict, risk: Dict) -> tuple:
        """计算计划质量评分"""
        composite_score = decision.get('composite_score', 75)
        risk_score = risk.get('risk_profiles', {}).get('neutral', {}).get('score', 75)
        
        # 综合评分
        plan_score = (composite_score + risk_score) / 2
        
        if plan_score >= 85:
            recommendation = "立即执行"
            priority = "高"
        elif plan_score >= 75:
            recommendation = "执行，加强监控"
            priority = "中高"
        elif plan_score >= 65:
            recommendation = "执行，谨慎监控"
            priority = "中"
        else:
            recommendation = "修改完善后执行"
            priority = "低"
        
        return plan_score, recommendation, priority
    
    def generate_plan(self, decision_file: str, trading_file: str, risk_file: str) -> InvestmentPlan:
        """生成完整投资计划"""
        # 加载分析结果
        decision, trading, risk = self.load_analysis_results(decision_file, trading_file, risk_file)
        
        # 生成计划各部分
        thesis = self.generate_thesis(decision, risk)
        strategy = self.generate_strategy(trading, risk)
        risk_mgmt = self.generate_risk_management(risk)
        execution = self.generate_execution()
        
        # 计算质量评分
        plan_score, recommendation, priority = self.calculate_plan_quality(decision, risk)
        
        return InvestmentPlan(
            symbol=self.symbol,
            plan_date=self.plan_date,
            version="1.0",
            decision_analysis=decision,
            trading_analysis=trading,
            risk_analysis=risk,
            thesis=thesis,
            strategy=strategy,
            risk_management=risk_mgmt,
            execution=execution,
            monitoring_metrics=[
                "当前价格 vs 入场价",
                "当前回撤",
                "风险收益比变化",
                "仓位占比",
                "大盘走势"
            ],
            adjustment_triggers=[
                {"condition": "达到止损位", "action": "立即止损", "priority": "紧急"},
                {"condition": "基本面恶化", "action": "减仓或清仓", "priority": "高"},
                {"condition": "达到第一止盈", "action": "减仓25%", "priority": "中"}
            ],
            review_schedule={
                "daily": "检查持仓状态、监控风险指标",
                "weekly": "评估交易表现、分析盈亏原因",
                "monthly": "全面绩效评估、策略优化更新"
            },
            plan_quality_score=plan_score,
            recommendation=recommendation,
            priority=priority
        )
    
    def export_plan(self, plan: InvestmentPlan, output_dir: str):
        """导出投资计划"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # 导出JSON
        json_file = f"{output_dir}/{self.symbol}_investment_plan.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(plan), f, ensure_ascii=False, indent=2)
        
        # 生成Markdown报告
        md_file = f"{output_dir}/{self.symbol}_investment_plan.md"
        self._generate_markdown_report(plan, md_file)
        
        return json_file, md_file
    
    def _generate_markdown_report(self, plan: InvestmentPlan, output_file: str):
        """生成Markdown格式报告"""
        report = f"""# {plan.symbol} 投资计划书

**计划版本**: {plan.version}  
**生成日期**: {plan.plan_date}  
**计划质量评分**: {plan.plan_quality_score:.1f}/100  
**投资建议**: {plan.recommendation}  
**优先级**: {plan.priority}

---

## 1. 投资主题

### 1.1 核心投资逻辑

{plan.thesis.core_logic}

### 1.2 关键假设

| 假设 | 验证方法 | 风险点 |
|------|---------|--------|
"""
        
        for assumption in plan.thesis.key_assumptions:
            report += f"| {assumption['assumption']} | {assumption['verification']} | {assumption['risk']} |\n"
        
        report += f"""
### 1.3 催化剂事件

**短期催化剂 (1-3个月)**:
"""
        for catalyst in plan.thesis.catalysts_short:
            report += f"- {catalyst}\n"
        
        report += "\n**中期催化剂 (3-12个月)**:\n"
        for catalyst in plan.thesis.catalysts_medium:
            report += f"- {catalyst}\n"
        
        report += "\n**长期催化剂 (1-3年)**:\n"
        for catalyst in plan.thesis.catalysts_long:
            report += f"- {catalyst}\n"
        
        report += f"""

---

## 2. 交易策略

### 2.1 入场策略

**入场条件**:
"""
        for condition in plan.strategy.entry_conditions:
            report += f"- [ ] {condition}\n"
        
        report += f"""
**入场价格区间**:
- 理想入场价: {plan.strategy.entry_price_range['ideal']}
- 可接受区间: {plan.strategy.entry_price_range['min']} - {plan.strategy.entry_price_range['max']}

**入场时机**: {plan.strategy.entry_timing}

### 2.2 仓位管理

**初始仓位**: {plan.strategy.initial_position}

**金字塔加仓计划**:

| 次序 | 仓位比例 | 触发条件 |
|------|---------|---------|
"""
        for item in plan.strategy.pyramiding_plan:
            report += f"| 第{item['order']}次 | {item['size']} | {item['trigger']} |\n"
        
        report += f"""
### 2.3 出场策略

**止盈策略**: {plan.strategy.take_profit_strategy}

**止损策略**: {plan.strategy.stop_loss_strategy}

---

## 3. 风险管理

### 3.1 风险矩阵

| 风险类型 | 描述 | 概率 | 影响 | 等级 |
|---------|------|------|------|------|
"""
        for risk in plan.risk_management.risk_matrix:
            report += f"| {risk['type']} | {risk['description']} | {risk['probability']} | {risk['impact']} | {risk['level']} |\n"
        
        report += f"""
### 3.2 仓位限制

- 单标的最大仓位: {plan.risk_management.position_limits['single_stock_max']}
- 单一行业最大仓位: {plan.risk_management.position_limits['single_industry_max']}
- 单笔交易风险: {plan.risk_management.position_limits['risk_per_trade']}

### 3.3 止损设置

- 初始止损: {plan.risk_management.stop_loss_levels['initial']}
- 移动止损: {plan.risk_management.stop_loss_levels['trailing']}
- 时间止损: {plan.risk_management.stop_loss_levels['time_based']}

---

## 4. 执行方案

### 4.1 执行时间表

| 阶段 | 时间 | 任务 | 交付物 |
|------|------|------|--------|
"""
        for item in plan.execution.timeline:
            report += f"| {item['phase']} | {item['time']} | {item['task']} | {item['deliverable']} |\n"
        
        report += "\n### 4.2 执行检查清单\n\n**建仓前检查**:\n"
        for item in plan.execution.checklists['pre_entry']:
            report += f"- [ ] {item}\n"
        
        report += "\n**建仓时检查**:\n"
        for item in plan.execution.checklists['entry']:
            report += f"- [ ] {item}\n"
        
        report += "\n**持仓期检查**:\n"
        for item in plan.execution.checklists['holding']:
            report += f"- [ ] {item}\n"
        
        report += f"""

---

## 5. 监控与调整

### 5.1 关键监控指标

"""
        for metric in plan.monitoring_metrics:
            report += f"- {metric}\n"
        
        report += "\n### 5.2 调整触发条件\n\n| 触发条件 | 调整措施 | 优先级 |\n|---------|---------|--------|\n"
        for trigger in plan.adjustment_triggers:
            report += f"| {trigger['condition']} | {trigger['action']} | {trigger['priority']} |\n"
        
        report += "\n### 5.3 回顾计划\n\n"
        for period, task in plan.review_schedule.items():
            report += f"- **{period}**: {task}\n"
        
        report += """

---

## 6. 风险提示

本投资计划基于当前市场信息和分析框架生成，不构成投资建议。
投资有风险，入市需谨慎。请根据自身风险承受能力做出投资决策。

---

*报告由投资计划生成系统自动生成*
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

def main():
    parser = argparse.ArgumentParser(description='生成综合投资计划')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--decision-file', default='', help='投资决策分析文件')
    parser.add_argument('--trading-file', default='', help='投资交易分析文件')
    parser.add_argument('--risk-file', default='', help='风险决策分析文件')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    print(f"开始生成投资计划: {args.symbol}")
    print(f"计划生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 生成投资计划
    generator = InvestmentPlanGenerator(args.symbol)
    plan = generator.generate_plan(args.decision_file, args.trading_file, args.risk_file)
    
    # 导出计划
    json_file, md_file = generator.export_plan(plan, args.output)
    
    print("\n" + "=" * 50)
    print("投资计划生成完成!")
    print("=" * 50)
    print(f"\n计划质量评分: {plan.plan_quality_score:.1f}/100")
    print(f"投资建议: {plan.recommendation}")
    print(f"执行优先级: {plan.priority}")
    print(f"\n输出文件:")
    print(f"  JSON: {json_file}")
    print(f"  Markdown: {md_file}")
    
    print("\n" + "-" * 50)
    print("投资主题摘要:")
    print(plan.thesis.core_logic[:200] + "..." if len(plan.thesis.core_logic) > 200 else plan.thesis.core_logic)
    
    print("\n交易策略摘要:")
    print(f"  入场时机: {plan.strategy.entry_timing}")
    print(f"  初始仓位: {plan.strategy.initial_position}")
    print(f"  止盈策略: {plan.strategy.take_profit_strategy}")
    print(f"  止损策略: {plan.strategy.stop_loss_strategy}")

if __name__ == "__main__":
    main()
