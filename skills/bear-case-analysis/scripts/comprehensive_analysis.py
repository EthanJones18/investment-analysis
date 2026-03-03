#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
空头综合分析脚本
挖掘下跌机会和风险点，识别做空机会

使用方法:
    python comprehensive_analysis.py --symbol XYZ --analysis-depth full
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ValuationMetrics:
    """估值泡沫指标"""
    pe_ratio: float
    ps_ratio: float
    peg_ratio: float
    ev_ebitda: float
    price_book: float
    vs_historical: str  # 相对于历史均值
    vs_industry: str    # 相对于行业
    bubble_score: float  # 0-10


@dataclass
class FundamentalRedFlags:
    """基本面红旗"""
    revenue_quality: float  # 收入质量 0-10
    cash_flow_quality: float  # 现金流质量 0-10
    balance_sheet_risk: float  # 资产负债表风险 0-10
    accounting_concerns: List[str]  # 会计关注点
    overall_risk: str  # High/Medium/Low
    score: float  # 0-10，越高风险越大


@dataclass
class IndustryRisks:
    """行业风险"""
    cycle_phase: str  # 周期阶段
    disruption_risk: float  # 技术替代风险 0-10
    regulatory_risk: float  # 监管风险 0-10
    competition_intensity: float  # 竞争强度 0-10
    growth_outlook: str  # 增长前景
    score: float  # 0-10


@dataclass
class ManagementRisks:
    """管理层风险"""
    insider_selling: bool
    auditor_changes: bool
    related_party_transactions: float  # 关联交易占比
    guidance_accuracy: str  # 业绩指引准确性
    score: float  # 0-10


@dataclass
class BearCaseReport:
    """空头案例报告"""
    symbol: str
    analysis_date: str
    overall_score: float
    rating: str
    short_thesis: str
    valuation_metrics: ValuationMetrics
    fundamental_flags: FundamentalRedFlags
    industry_risks: IndustryRisks
    management_risks: ManagementRisks
    key_risks: List[str]
    catalysts: List[str]
    target_price: Optional[float]
    downside_potential: Optional[float]
    short_recommendation: str


class BearCaseAnalyzer:
    """空头案例分析器"""
    
    def __init__(self, symbol: str, output_dir: str = "./output"):
        self.symbol = symbol
        self.output_dir = output_dir
        
        # 模拟数据存储
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self) -> dict:
        """加载模拟数据"""
        return {
            "GME": {
                "name": "GameStop Corp.",
                "sector": "Consumer Cyclical",
                "valuation": {
                    "pe_ratio": -15.0,  # 亏损
                    "ps_ratio": 1.8,
                    "peg_ratio": -1.0,
                    "ev_ebitda": 45.0,
                    "price_book": 8.5,
                    "vs_historical": "+150%",
                    "vs_industry": "+200%"
                },
                "fundamental": {
                    "revenue_decline_3y": -0.25,
                    "negative_cash_flow": True,
                    "inventory_turnover_decline": True,
                    "goodwill_impairment": True,
                    "debt_to_equity": 0.85,
                    "accounting_issues": ["收入确认激进", "存货跌价准备不足"]
                },
                "industry": {
                    "cycle_phase": "衰退期",
                    "disruption_risk": 9.0,  # 数字化冲击
                    "regulatory_risk": 3.0,
                    "competition_intensity": 8.5,
                    "growth_outlook": "负增长"
                },
                "management": {
                    "insider_selling": True,
                    "auditor_changes": True,
                    "related_party_pct": 0.15,
                    "guidance_accuracy": "差"
                }
            },
            "AMC": {
                "name": "AMC Entertainment",
                "sector": "Communication Services",
                "valuation": {
                    "pe_ratio": -8.0,
                    "ps_ratio": 2.5,
                    "peg_ratio": -1.0,
                    "ev_ebitda": 35.0,
                    "price_book": 12.0,
                    "vs_historical": "+300%",
                    "vs_industry": "+250%"
                },
                "fundamental": {
                    "revenue_decline_3y": -0.60,
                    "negative_cash_flow": True,
                    "inventory_turnover_decline": False,
                    "goodwill_impairment": True,
                    "debt_to_equity": 2.5,
                    "accounting_issues": ["债务重组频繁", "持续经营能力存疑"]
                },
                "industry": {
                    "cycle_phase": "衰退期",
                    "disruption_risk": 9.5,  # 流媒体冲击
                    "regulatory_risk": 4.0,
                    "competition_intensity": 7.0,
                    "growth_outlook": "负增长"
                },
                "management": {
                    "insider_selling": True,
                    "auditor_changes": False,
                    "related_party_pct": 0.08,
                    "guidance_accuracy": "差"
                }
            },
            "PLTR": {
                "name": "Palantir Technologies",
                "sector": "Technology",
                "valuation": {
                    "pe_ratio": 150.0,
                    "ps_ratio": 25.0,
                    "peg_ratio": 5.0,
                    "ev_ebitda": 80.0,
                    "price_book": 15.0,
                    "vs_historical": "+100%",
                    "vs_industry": "+400%"
                },
                "fundamental": {
                    "revenue_decline_3y": 0.25,  # 正增长但放缓
                    "negative_cash_flow": False,
                    "inventory_turnover_decline": False,
                    "goodwill_impairment": False,
                    "debt_to_equity": 0.15,
                    "accounting_issues": ["收入集中度高", "客户集中度风险"]
                },
                "industry": {
                    "cycle_phase": "成熟期",
                    "disruption_risk": 6.0,
                    "regulatory_risk": 7.0,  # 数据隐私监管
                    "competition_intensity": 7.5,
                    "growth_outlook": "放缓"
                },
                "management": {
                    "insider_selling": True,
                    "auditor_changes": False,
                    "related_party_pct": 0.05,
                    "guidance_accuracy": "中等"
                }
            }
        }
    
    def analyze(self, analysis_depth: str = "full") -> BearCaseReport:
        """执行空头分析"""
        print(f"\n开始空头分析 - {self.symbol}")
        print("=" * 70)
        
        # 获取数据
        data = self.mock_data.get(self.symbol, self.mock_data["GME"])
        
        # 1. 估值泡沫分析
        print("\n【步骤 1/4】估值泡沫分析...")
        valuation = self._analyze_valuation(data["valuation"])
        print(f"  估值泡沫评分: {valuation.bubble_score:.1f}/10")
        print(f"  相对于历史: {valuation.vs_historical}")
        print(f"  相对于行业: {valuation.vs_industry}")
        
        # 2. 基本面红旗分析
        print("\n【步骤 2/4】基本面红旗分析...")
        fundamental = self._analyze_fundamental(data["fundamental"])
        print(f"  基本面风险评分: {fundamental.score:.1f}/10")
        print(f"  风险级别: {fundamental.overall_risk}")
        
        # 3. 行业风险分析
        print("\n【步骤 3/4】行业风险分析...")
        industry = self._analyze_industry(data["industry"])
        print(f"  行业风险评分: {industry.score:.1f}/10")
        print(f"  行业周期: {industry.cycle_phase}")
        
        # 4. 管理层风险分析
        print("\n【步骤 4/4】管理层风险分析...")
        management = self._analyze_management(data["management"])
        print(f"  管理层风险评分: {management.score:.1f}/10")
        
        # 计算综合评分
        overall_score = self._calculate_overall_score(
            valuation.bubble_score,
            fundamental.score,
            industry.score,
            management.score
        )
        
        # 确定评级
        rating = self._get_rating(overall_score)
        
        # 生成做空主题
        short_thesis = self._generate_thesis(data, overall_score)
        
        # 识别关键风险
        key_risks = self._identify_risks(data, valuation, fundamental, industry)
        
        # 识别催化剂
        catalysts = self._identify_catalysts(data, industry)
        
        # 做空建议
        short_recommendation = self._generate_short_recommendation(overall_score)
        
        # 构建报告
        report = BearCaseReport(
            symbol=self.symbol,
            analysis_date=datetime.now().isoformat(),
            overall_score=overall_score,
            rating=rating,
            short_thesis=short_thesis,
            valuation_metrics=valuation,
            fundamental_flags=fundamental,
            industry_risks=industry,
            management_risks=management,
            key_risks=key_risks,
            catalysts=catalysts,
            target_price=None,
            downside_potential=None,
            short_recommendation=short_recommendation
        )
        
        return report
    
    def _analyze_valuation(self, data: dict) -> ValuationMetrics:
        """分析估值泡沫"""
        score = 0
        
        # P/E分析
        pe = data["pe_ratio"]
        if pe < 0:
            score += 3  # 亏损公司估值风险
        elif pe > 100:
            score += 2.5
        elif pe > 50:
            score += 1.5
        
        # P/S分析
        ps = data["ps_ratio"]
        if ps > 20:
            score += 2.5
        elif ps > 10:
            score += 1.5
        elif ps > 5:
            score += 0.5
        
        # EV/EBITDA分析
        ev_ebitda = data["ev_ebitda"]
        if ev_ebitda > 50:
            score += 2
        elif ev_ebitda > 30:
            score += 1
        
        # P/B分析
        pb = data["price_book"]
        if pb > 10:
            score += 1
        elif pb > 5:
            score += 0.5
        
        # 相对历史/行业溢价
        if "+" in data["vs_historical"]:
            premium = float(data["vs_historical"].replace("+", "").replace("%", ""))
            if premium > 200:
                score += 1
            elif premium > 100:
                score += 0.5
        
        score = min(10, score)
        
        return ValuationMetrics(
            pe_ratio=data["pe_ratio"],
            ps_ratio=data["ps_ratio"],
            peg_ratio=data["peg_ratio"],
            ev_ebitda=data["ev_ebitda"],
            price_book=data["price_book"],
            vs_historical=data["vs_historical"],
            vs_industry=data["vs_industry"],
            bubble_score=round(score, 1)
        )
    
    def _analyze_fundamental(self, data: dict) -> FundamentalRedFlags:
        """分析基本面红旗"""
        score = 0
        concerns = []
        
        # 收入下滑
        if data["revenue_decline_3y"] < -0.20:
            score += 2
            concerns.append(f"收入3年下滑{abs(data['revenue_decline_3y'])*100:.0f}%")
        elif data["revenue_decline_3y"] < -0.10:
            score += 1
        
        # 负现金流
        if data["negative_cash_flow"]:
            score += 2.5
            concerns.append("经营现金流持续为负")
        
        # 存货周转下降
        if data["inventory_turnover_decline"]:
            score += 1
            concerns.append("存货周转率下降")
        
        # 商誉减值
        if data["goodwill_impairment"]:
            score += 1.5
            concerns.append("商誉减值风险")
        
        # 高杠杆
        de = data["debt_to_equity"]
        if de > 2.0:
            score += 2
            concerns.append(f"高负债率(D/E={de:.1f})")
        elif de > 1.0:
            score += 1
        
        # 会计问题
        concerns.extend(data.get("accounting_issues", []))
        score += len(data.get("accounting_issues", [])) * 0.5
        
        score = min(10, score)
        
        # 确定风险级别
        if score >= 7:
            risk_level = "High"
        elif score >= 4:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        return FundamentalRedFlags(
            revenue_quality=max(0, 10 - abs(data["revenue_decline_3y"]) * 20),
            cash_flow_quality=0 if data["negative_cash_flow"] else 8,
            balance_sheet_risk=max(0, 10 - de * 3),
            accounting_concerns=concerns,
            overall_risk=risk_level,
            score=round(score, 1)
        )
    
    def _analyze_industry(self, data: dict) -> IndustryRisks:
        """分析行业风险"""
        score = 0
        
        # 周期阶段
        cycle_scores = {
            "衰退期": 3,
            "成熟期": 1.5,
            "成长期": 0.5,
            "萌芽期": 1
        }
        score += cycle_scores.get(data["cycle_phase"], 1)
        
        # 技术替代风险
        score += data["disruption_risk"] * 0.25
        
        # 监管风险
        score += data["regulatory_risk"] * 0.15
        
        # 竞争强度
        score += data["competition_intensity"] * 0.15
        
        # 增长前景
        if data["growth_outlook"] == "负增长":
            score += 1.5
        elif data["growth_outlook"] == "放缓":
            score += 0.5
        
        score = min(10, score)
        
        return IndustryRisks(
            cycle_phase=data["cycle_phase"],
            disruption_risk=data["disruption_risk"],
            regulatory_risk=data["regulatory_risk"],
            competition_intensity=data["competition_intensity"],
            growth_outlook=data["growth_outlook"],
            score=round(score, 1)
        )
    
    def _analyze_management(self, data: dict) -> ManagementRisks:
        """分析管理层风险"""
        score = 0
        
        # 内部人卖出
        if data["insider_selling"]:
            score += 2
        
        # 审计师变更
        if data["auditor_changes"]:
            score += 2.5
        
        # 关联交易
        related = data["related_party_pct"]
        if related > 0.20:
            score += 2
        elif related > 0.10:
            score += 1
        
        # 业绩指引准确性
        guidance_scores = {
            "差": 2,
            "中等": 1,
            "好": 0
        }
        score += guidance_scores.get(data["guidance_accuracy"], 1)
        
        score = min(10, score)
        
        return ManagementRisks(
            insider_selling=data["insider_selling"],
            auditor_changes=data["auditor_changes"],
            related_party_transactions=data["related_party_pct"],
            guidance_accuracy=data["guidance_accuracy"],
            score=round(score, 1)
        )
    
    def _calculate_overall_score(self, valuation: float, fundamental: float,
                                  industry: float, management: float) -> float:
        """计算综合评分 (0-100)"""
        weights = {
            "valuation": 0.25,
            "fundamental": 0.25,
            "industry": 0.20,
            "management": 0.15,
            "short_conditions": 0.15
        }
        
        # 做空条件评分（简化）
        short_conditions = 7.0
        
        overall = (valuation * weights["valuation"] +
                  fundamental * weights["fundamental"] +
                  industry * weights["industry"] +
                  management * weights["management"] +
                  short_conditions * weights["short_conditions"])
        
        return round(overall * 10, 1)  # 转换为百分制
    
    def _get_rating(self, score: float) -> str:
        """获取评级"""
        if score >= 90:
            return "强烈推荐做空 (Strong Short)"
        elif score >= 80:
            return "推荐做空 (Short)"
        elif score >= 70:
            return "中性偏空 (Underweight)"
        elif score >= 60:
            return "中性 (Neutral)"
        else:
            return "回避 (Avoid)"
    
    def _generate_thesis(self, data: dict, score: float) -> str:
        """生成做空主题"""
        company_name = data.get("name", self.symbol)
        
        if score >= 85:
            return f"{company_name}存在严重的估值泡沫和基本面问题。公司所处行业面临结构性衰退，管理层诚信存疑，财务数据异常。当前股价严重脱离基本面，存在显著的做空机会。"
        elif score >= 75:
            return f"{company_name}估值过高，基本面存在明显缺陷。行业竞争加剧，增长前景黯淡，建议做空或规避。"
        elif score >= 65:
            return f"{company_name}存在一定风险因素，但做空时机尚需等待。建议密切关注催化剂事件。"
        else:
            return f"{company_name}做空吸引力有限，建议寻找更好的做空标的。"
    
    def _identify_risks(self, data: dict, valuation: ValuationMetrics,
                       fundamental: FundamentalRedFlags, industry: IndustryRisks) -> List[str]:
        """识别关键风险"""
        risks = []
        
        # 估值风险
        if valuation.bubble_score >= 7:
            risks.append("估值泡沫严重")
        if valuation.pe_ratio < 0:
            risks.append("持续亏损")
        
        # 基本面风险
        if fundamental.overall_risk == "High":
            risks.append("基本面严重恶化")
        if fundamental.accounting_concerns:
            risks.extend(fundamental.accounting_concerns[:3])
        
        # 行业风险
        if industry.disruption_risk >= 8:
            risks.append("技术替代风险高")
        if industry.growth_outlook == "负增长":
            risks.append("行业负增长")
        
        # 通用风险
        risks.extend([
            "市场情绪逆转风险",
            "流动性风险",
            "轧空风险"
        ])
        
        return risks
    
    def _identify_catalysts(self, data: dict, industry: IndustryRisks) -> List[str]:
        """识别催化剂"""
        catalysts = []
        
        # 财务催化剂
        catalysts.append("季度业绩不及预期")
        catalysts.append("审计意见非标")
        
        # 行业催化剂
        if industry.disruption_risk >= 8:
            catalysts.append("技术替代加速")
        
        # 市场催化剂
        catalysts.append("做空报告发布")
        catalysts.append("机构下调评级")
        catalysts.append("宏观经济恶化")
        
        return catalysts
    
    def _generate_short_recommendation(self, score: float) -> str:
        """生成做空建议"""
        if score >= 85:
            return "强烈建议做空。建议通过融券或购买看跌期权建立空头头寸，目标仓位5-10%。"
        elif score >= 75:
            return "建议适度做空。可通过融券或看跌期权做空，目标仓位3-5%。"
        elif score >= 65:
            return "建议观望。等待更好的做空时机或催化剂事件。"
        else:
            return "不建议做空。寻找其他做空标的。"
    
    def save_report(self, report: BearCaseReport):
        """保存分析报告"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(
            self.output_dir,
            f"{self.symbol}_bear_case_analysis.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存: {output_file}")
        return output_file
    
    def print_report(self, report: BearCaseReport):
        """打印分析报告"""
        print("\n" + "=" * 70)
        print(f"空头分析报告 - {report.symbol}")
        print("=" * 70)
        
        # 综合评分
        print(f"\n【综合评估】")
        print(f"  空头评分: {report.overall_score}/100")
        print(f"  做空评级: {report.rating}")
        
        # 做空主题
        print(f"\n【做空主题】")
        print(f"  {report.short_thesis}")
        
        # 分项评分
        print(f"\n【分项评分】")
        print(f"  估值泡沫: {report.valuation_metrics.bubble_score}/10")
        print(f"  基本面风险: {report.fundamental_flags.score}/10 ({report.fundamental_flags.overall_risk})")
        print(f"  行业风险: {report.industry_risks.score}/10")
        print(f"  管理层风险: {report.management_risks.score}/10")
        
        # 估值详情
        print(f"\n【估值泡沫详情】")
        v = report.valuation_metrics
        print(f"  P/E Ratio: {v.pe_ratio:.1f}")
        print(f"  P/S Ratio: {v.ps_ratio:.1f}")
        print(f"  EV/EBITDA: {v.ev_ebitda:.1f}")
        print(f"  P/B Ratio: {v.price_book:.1f}")
        print(f"  相对历史溢价: {v.vs_historical}")
        print(f"  相对行业溢价: {v.vs_industry}")
        
        # 基本面风险
        print(f"\n【基本面红旗】")
        f = report.fundamental_flags
        print(f"  收入质量: {f.revenue_quality:.1f}/10")
        print(f"  现金流质量: {f.cash_flow_quality:.1f}/10")
        print(f"  资产负债表: {f.balance_sheet_risk:.1f}/10")
        print(f"\n  会计关注点:")
        for concern in f.accounting_concerns:
            print(f"    • {concern}")
        
        # 行业风险
        print(f"\n【行业风险详情】")
        i = report.industry_risks
        print(f"  行业周期: {i.cycle_phase}")
        print(f"  技术替代风险: {i.disruption_risk}/10")
        print(f"  监管风险: {i.regulatory_risk}/10")
        print(f"  竞争强度: {i.competition_intensity}/10")
        print(f"  增长前景: {i.growth_outlook}")
        
        # 管理层风险
        print(f"\n【管理层风险】")
        m = report.management_risks
        print(f"  内部人卖出: {'是' if m.insider_selling else '否'}")
        print(f"  审计师变更: {'是' if m.auditor_changes else '否'}")
        print(f"  关联交易占比: {m.related_party_transactions*100:.1f}%")
        print(f"  业绩指引准确性: {m.guidance_accuracy}")
        
        # 关键风险
        print(f"\n【关键风险因素】")
        for i, risk in enumerate(report.key_risks[:8], 1):
            print(f"  {i}. {risk}")
        
        # 催化剂
        print(f"\n【潜在催化剂】")
        for i, catalyst in enumerate(report.catalysts, 1):
            print(f"  {i}. {catalyst}")
        
        # 做空建议
        print(f"\n【做空建议】")
        print(f"  {report.short_recommendation}")
        
        if report.overall_score >= 80:
            print(f"\n  ⚠️ 风险提示:")
            print(f"    • 做空存在无限损失风险")
            print(f"    • 建议设置止损位")
            print(f"    • 密切关注轧空风险")
            print(f"    • 考虑使用期权限制风险")
        
        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description='空头研究分析')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--analysis-depth', default='full',
                       choices=['basic', 'full', 'comprehensive'],
                       help='分析深度')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = BearCaseAnalyzer(args.symbol, args.output)
    
    # 执行分析
    report = analyzer.analyze(args.analysis_depth)
    
    # 保存和打印报告
    analyzer.save_report(report)
    analyzer.print_report(report)


if __name__ == '__main__':
    main()
