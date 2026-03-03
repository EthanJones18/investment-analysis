#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多头综合分析脚本
深入研究公司的成长机会和上升潜力

使用方法:
    python comprehensive_analysis.py --symbol AAPL --analysis-depth full
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class GrowthMetrics:
    """增长质量指标"""
    revenue_growth_3y: float
    revenue_growth_5y: float
    earnings_growth_3y: float
    gross_margin_trend: str
    operating_margin_trend: str
    fcf_growth: float
    roe: float
    roic: float
    score: float


@dataclass
class MoatAnalysis:
    """护城河分析"""
    brand_strength: float  # 0-10
    cost_advantage: float  # 0-10
    network_effects: float  # 0-10
    switching_costs: float  # 0-10
    patents_ip: float  # 0-10
    overall_moat: str  # Wide/Narrow/None
    score: float


@dataclass
class InnovationMetrics:
    """创新驱动指标"""
    rd_spending_pct: float
    rd_growth: float
    patent_count: int
    new_product_contribution: float
    tech_leadership: str
    score: float


@dataclass
class MarketOpportunity:
    """市场机会"""
    tam: float  # Total Addressable Market
    sam: float  # Serviceable Addressable Market
    som: float  # Serviceable Obtainable Market
    market_growth_rate: float
    market_share: float
    expansion_opportunities: List[str]
    score: float


@dataclass
class BullCaseReport:
    """多头案例报告"""
    symbol: str
    analysis_date: str
    overall_score: float
    rating: str
    investment_thesis: str
    growth_metrics: GrowthMetrics
    moat_analysis: MoatAnalysis
    innovation_metrics: InnovationMetrics
    market_opportunity: MarketOpportunity
    key_strengths: List[str]
    risk_factors: List[str]
    target_price: Optional[float]
    upside_potential: Optional[float]


class BullCaseAnalyzer:
    """多头案例分析器"""
    
    def __init__(self, symbol: str, output_dir: str = "./output"):
        self.symbol = symbol
        self.output_dir = output_dir
        
        # 模拟数据存储
        self.mock_data = self._load_mock_data()
    
    def _load_mock_data(self) -> dict:
        """加载模拟数据（实际应用中应从API获取）"""
        return {
            "AAPL": {
                "name": "Apple Inc.",
                "sector": "Technology",
                "growth": {
                    "revenue_growth_3y": 0.15,
                    "revenue_growth_5y": 0.12,
                    "earnings_growth_3y": 0.18,
                    "gross_margin_trend": "stable",
                    "operating_margin_trend": "improving",
                    "fcf_growth": 0.14,
                    "roe": 0.28,
                    "roic": 0.25
                },
                "moat": {
                    "brand_strength": 9.5,
                    "cost_advantage": 7.0,
                    "network_effects": 8.5,
                    "switching_costs": 8.0,
                    "patents_ip": 7.5
                },
                "innovation": {
                    "rd_spending_pct": 0.07,
                    "rd_growth": 0.12,
                    "patent_count": 2500,
                    "new_product_contribution": 0.25,
                    "tech_leadership": "leading"
                },
                "market": {
                    "tam": 1000000000000,  # $1T
                    "sam": 500000000000,   # $500B
                    "som": 50000000000,    # $50B
                    "market_growth_rate": 0.08,
                    "market_share": 0.20,
                    "expansion_opportunities": ["Services", "AR/VR", "Automotive"]
                }
            },
            "NVDA": {
                "name": "NVIDIA Corporation",
                "sector": "Technology",
                "growth": {
                    "revenue_growth_3y": 0.45,
                    "revenue_growth_5y": 0.35,
                    "earnings_growth_3y": 0.55,
                    "gross_margin_trend": "improving",
                    "operating_margin_trend": "improving",
                    "fcf_growth": 0.50,
                    "roe": 0.35,
                    "roic": 0.30
                },
                "moat": {
                    "brand_strength": 9.0,
                    "cost_advantage": 6.0,
                    "network_effects": 7.5,
                    "switching_costs": 7.0,
                    "patents_ip": 8.5
                },
                "innovation": {
                    "rd_spending_pct": 0.20,
                    "rd_growth": 0.25,
                    "patent_count": 8000,
                    "new_product_contribution": 0.40,
                    "tech_leadership": "dominant"
                },
                "market": {
                    "tam": 500000000000,   # $500B
                    "sam": 200000000000,   # $200B
                    "som": 30000000000,    # $30B
                    "market_growth_rate": 0.25,
                    "market_share": 0.80,
                    "expansion_opportunities": ["AI/Data Center", "Automotive", "Robotics"]
                }
            },
            "TSLA": {
                "name": "Tesla, Inc.",
                "sector": "Automotive",
                "growth": {
                    "revenue_growth_3y": 0.35,
                    "revenue_growth_5y": 0.28,
                    "earnings_growth_3y": 0.40,
                    "gross_margin_trend": "improving",
                    "operating_margin_trend": "improving",
                    "fcf_growth": 0.30,
                    "roe": 0.20,
                    "roic": 0.15
                },
                "moat": {
                    "brand_strength": 8.5,
                    "cost_advantage": 6.5,
                    "network_effects": 7.0,
                    "switching_costs": 5.0,
                    "patents_ip": 7.0
                },
                "innovation": {
                    "rd_spending_pct": 0.15,
                    "rd_growth": 0.20,
                    "patent_count": 1200,
                    "new_product_contribution": 0.30,
                    "tech_leadership": "leading"
                },
                "market": {
                    "tam": 3000000000000,  # $3T
                    "sam": 500000000000,   # $500B
                    "som": 100000000000,   # $100B
                    "market_growth_rate": 0.15,
                    "market_share": 0.05,
                    "expansion_opportunities": ["Energy Storage", "Robotaxi", "AI/Robotics"]
                }
            }
        }
    
    def analyze(self, analysis_depth: str = "full") -> BullCaseReport:
        """
        执行多头分析
        
        Args:
            analysis_depth: 分析深度 (basic/full/comprehensive)
        """
        print(f"\n开始多头分析 - {self.symbol}")
        print("=" * 70)
        
        # 获取数据
        data = self.mock_data.get(self.symbol, self.mock_data["AAPL"])
        
        # 1. 增长质量分析
        print("\n【步骤 1/4】增长质量分析...")
        growth_metrics = self._analyze_growth(data["growth"])
        print(f"  增长质量评分: {growth_metrics.score:.1f}/10")
        
        # 2. 护城河分析
        print("\n【步骤 2/4】护城河分析...")
        moat_analysis = self._analyze_moat(data["moat"])
        print(f"  护城河评分: {moat_analysis.score:.1f}/10")
        print(f"  护城河等级: {moat_analysis.overall_moat}")
        
        # 3. 创新驱动分析
        print("\n【步骤 3/4】创新驱动分析...")
        innovation_metrics = self._analyze_innovation(data["innovation"])
        print(f"  创新评分: {innovation_metrics.score:.1f}/10")
        
        # 4. 市场机会分析
        print("\n【步骤 4/4】市场机会分析...")
        market_opportunity = self._analyze_market(data["market"])
        print(f"  市场机会评分: {market_opportunity.score:.1f}/10")
        
        # 计算综合评分 (0-100)
        overall_score = self._calculate_overall_score(
            growth_metrics.score,
            moat_analysis.score,
            innovation_metrics.score,
            market_opportunity.score
        ) * 10  # 转换为百分制
        
        # 确定评级
        rating = self._get_rating(overall_score)
        
        # 生成投资主题
        investment_thesis = self._generate_thesis(data, overall_score)
        
        # 识别关键优势
        key_strengths = self._identify_strengths(data, growth_metrics, moat_analysis, innovation_metrics)
        
        # 识别风险因素
        risk_factors = self._identify_risks(data, overall_score)
        
        # 构建报告
        report = BullCaseReport(
            symbol=self.symbol,
            analysis_date=datetime.now().isoformat(),
            overall_score=overall_score,
            rating=rating,
            investment_thesis=investment_thesis,
            growth_metrics=growth_metrics,
            moat_analysis=moat_analysis,
            innovation_metrics=innovation_metrics,
            market_opportunity=market_opportunity,
            key_strengths=key_strengths,
            risk_factors=risk_factors,
            target_price=None,  # 需要估值模型
            upside_potential=None
        )
        
        return report
    
    def _analyze_growth(self, data: dict) -> GrowthMetrics:
        """分析增长质量"""
        # 计算增长评分
        revenue_score = min(10, (data["revenue_growth_3y"] / 0.20) * 10)
        earnings_score = min(10, (data["earnings_growth_3y"] / 0.25) * 10)
        fcf_score = min(10, (data["fcf_growth"] / 0.20) * 10)
        roe_score = min(10, (data["roe"] / 0.25) * 10)
        roic_score = min(10, (data["roic"] / 0.20) * 10)
        
        # 趋势加分
        trend_bonus = 0
        if data["gross_margin_trend"] == "improving":
            trend_bonus += 1
        if data["operating_margin_trend"] == "improving":
            trend_bonus += 1
        
        overall_score = (revenue_score + earnings_score + fcf_score + 
                        roe_score + roic_score) / 5 + trend_bonus
        overall_score = min(10, overall_score)
        
        return GrowthMetrics(
            revenue_growth_3y=data["revenue_growth_3y"],
            revenue_growth_5y=data["revenue_growth_5y"],
            earnings_growth_3y=data["earnings_growth_3y"],
            gross_margin_trend=data["gross_margin_trend"],
            operating_margin_trend=data["operating_margin_trend"],
            fcf_growth=data["fcf_growth"],
            roe=data["roe"],
            roic=data["roic"],
            score=round(overall_score, 1)
        )
    
    def _analyze_moat(self, data: dict) -> MoatAnalysis:
        """分析护城河"""
        avg_score = sum(data.values()) / len(data)
        
        # 确定护城河等级
        if avg_score >= 8:
            overall_moat = "Wide"
        elif avg_score >= 6:
            overall_moat = "Narrow"
        else:
            overall_moat = "None"
        
        return MoatAnalysis(
            brand_strength=data["brand_strength"],
            cost_advantage=data["cost_advantage"],
            network_effects=data["network_effects"],
            switching_costs=data["switching_costs"],
            patents_ip=data["patents_ip"],
            overall_moat=overall_moat,
            score=round(avg_score, 1)
        )
    
    def _analyze_innovation(self, data: dict) -> InnovationMetrics:
        """分析创新驱动"""
        # 研发强度评分
        rd_score = min(10, (data["rd_spending_pct"] / 0.15) * 10)
        
        # 专利评分
        patent_score = min(10, (data["patent_count"] / 5000) * 10)
        
        # 新产品贡献评分
        product_score = min(10, (data["new_product_contribution"] / 0.30) * 10)
        
        # 技术领导力加分
        leadership_bonus = {"dominant": 2, "leading": 1, "following": 0}
        leadership_score = leadership_bonus.get(data["tech_leadership"], 0)
        
        overall_score = (rd_score + patent_score + product_score) / 3 + leadership_score
        overall_score = min(10, overall_score)
        
        return InnovationMetrics(
            rd_spending_pct=data["rd_spending_pct"],
            rd_growth=data["rd_growth"],
            patent_count=data["patent_count"],
            new_product_contribution=data["new_product_contribution"],
            tech_leadership=data["tech_leadership"],
            score=round(overall_score, 1)
        )
    
    def _analyze_market(self, data: dict) -> MarketOpportunity:
        """分析市场机会"""
        # 市场规模评分
        tam_score = min(10, (data["tam"] / 1000000000000) * 10)
        
        # 市场增长评分
        growth_score = min(10, (data["market_growth_rate"] / 0.15) * 10)
        
        # 市场份额评分（考虑增长空间）
        share_score = min(10, (1 - data["market_share"]) * 10)
        
        # 扩张机会加分
        expansion_bonus = len(data["expansion_opportunities"]) * 0.5
        
        overall_score = (tam_score + growth_score + share_score) / 3 + expansion_bonus
        overall_score = min(10, overall_score)
        
        return MarketOpportunity(
            tam=data["tam"],
            sam=data["sam"],
            som=data["som"],
            market_growth_rate=data["market_growth_rate"],
            market_share=data["market_share"],
            expansion_opportunities=data["expansion_opportunities"],
            score=round(overall_score, 1)
        )
    
    def _calculate_overall_score(self, growth: float, moat: float, 
                                  innovation: float, market: float) -> float:
        """计算综合评分"""
        # 权重配置
        weights = {
            "growth": 0.25,
            "moat": 0.25,
            "innovation": 0.20,
            "market": 0.15,
            "financial": 0.10,
            "management": 0.05
        }
        
        # 财务健康评分（简化）
        financial_score = 8.0
        
        # 管理层评分（简化）
        management_score = 8.0
        
        overall = (growth * weights["growth"] + 
                  moat * weights["moat"] + 
                  innovation * weights["innovation"] + 
                  market * weights["market"] +
                  financial_score * weights["financial"] +
                  management_score * weights["management"])
        
        return round(overall, 1)
    
    def _get_rating(self, score: float) -> str:
        """获取评级"""
        if score >= 90:
            return "强烈推荐 (Strong Buy)"
        elif score >= 80:
            return "推荐 (Buy)"
        elif score >= 70:
            return "中性偏多 (Overweight)"
        elif score >= 60:
            return "中性 (Neutral)"
        else:
            return "回避 (Avoid)"
    
    def _generate_thesis(self, data: dict, score: float) -> str:
        """生成投资主题"""
        company_name = data.get("name", self.symbol)
        sector = data.get("sector", "Technology")
        
        if score >= 85:
            return f"{company_name}是{sector}行业的领导者，拥有深厚的护城河和持续的创新能力。公司在高增长市场中占据有利地位，财务表现优异，是长期持有的优质标的。"
        elif score >= 75:
            return f"{company_name}在{sector}领域具有竞争优势，增长前景良好。公司持续投入研发，市场拓展机会明确，适合积极配置。"
        elif score >= 65:
            return f"{company_name}基本面稳健，但面临一定竞争压力。建议关注其创新进展和市场拓展情况，适度配置。"
        else:
            return f"{company_name}面临较大挑战，竞争优势不明显或增长放缓。建议观望或寻找更好的投资机会。"
    
    def _identify_strengths(self, data: dict, growth: GrowthMetrics, 
                           moat: MoatAnalysis, innovation: InnovationMetrics) -> List[str]:
        """识别关键优势"""
        strengths = []
        
        if growth.revenue_growth_3y > 0.20:
            strengths.append(f"强劲的收入增长 ({growth.revenue_growth_3y*100:.0f}% CAGR)")
        
        if growth.roe > 0.20:
            strengths.append(f"优秀的资本回报率 (ROE {growth.roe*100:.0f}%)")
        
        if moat.overall_moat == "Wide":
            strengths.append("深厚的护城河保护")
        
        if moat.brand_strength >= 8:
            strengths.append("强大的品牌价值")
        
        if innovation.tech_leadership in ["leading", "dominant"]:
            strengths.append("技术领先地位")
        
        if innovation.rd_spending_pct > 0.10:
            strengths.append(f"高研发投入 ({innovation.rd_spending_pct*100:.0f}%)")
        
        return strengths
    
    def _identify_risks(self, data: dict, score: float) -> List[str]:
        """识别风险因素"""
        risks = []
        
        if score < 70:
            risks.append("整体竞争力不足")
        
        market_data = data.get("market", {})
        if market_data.get("market_share", 0) > 0.50:
            risks.append("市场份额已高，增长空间有限")
        
        growth_data = data.get("growth", {})
        if growth_data.get("revenue_growth_3y", 0) < 0.10:
            risks.append("增长放缓")
        
        risks.append("宏观经济波动风险")
        risks.append("行业竞争加剧")
        risks.append("监管政策变化")
        
        return risks
    
    def save_report(self, report: BullCaseReport):
        """保存分析报告"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(
            self.output_dir,
            f"{self.symbol}_bull_case_analysis.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存: {output_file}")
        return output_file
    
    def print_report(self, report: BullCaseReport):
        """打印分析报告"""
        print("\n" + "=" * 70)
        print(f"多头分析报告 - {report.symbol}")
        print("=" * 70)
        
        # 综合评分
        print(f"\n【综合评估】")
        print(f"  综合评分: {report.overall_score}/100")
        print(f"  投资评级: {report.rating}")
        
        # 投资主题
        print(f"\n【投资主题】")
        print(f"  {report.investment_thesis}")
        
        # 分项评分
        print(f"\n【分项评分】")
        print(f"  增长质量: {report.growth_metrics.score}/10")
        print(f"  护城河:   {report.moat_analysis.score}/10 ({report.moat_analysis.overall_moat})")
        print(f"  创新驱动: {report.innovation_metrics.score}/10")
        print(f"  市场机会: {report.market_opportunity.score}/10")
        
        # 增长质量详情
        print(f"\n【增长质量详情】")
        g = report.growth_metrics
        print(f"  营收增长 (3年CAGR): {g.revenue_growth_3y*100:.1f}%")
        print(f"  盈利增长 (3年CAGR): {g.earnings_growth_3y*100:.1f}%")
        print(f"  自由现金流增长: {g.fcf_growth*100:.1f}%")
        print(f"  ROE: {g.roe*100:.1f}%")
        print(f"  ROIC: {g.roic*100:.1f}%")
        
        # 护城河详情
        print(f"\n【护城河详情】")
        m = report.moat_analysis
        print(f"  品牌强度: {m.brand_strength}/10")
        print(f"  成本优势: {m.cost_advantage}/10")
        print(f"  网络效应: {m.network_effects}/10")
        print(f"  转换成本: {m.switching_costs}/10")
        print(f"  专利/IP: {m.patents_ip}/10")
        
        # 创新驱动详情
        print(f"\n【创新驱动详情】")
        i = report.innovation_metrics
        print(f"  研发支出占比: {i.rd_spending_pct*100:.1f}%")
        print(f"  专利数量: {i.patent_count}")
        print(f"  新产品贡献: {i.new_product_contribution*100:.0f}%")
        print(f"  技术地位: {i.tech_leadership}")
        
        # 市场机会详情
        print(f"\n【市场机会详情】")
        mo = report.market_opportunity
        print(f"  TAM: ${mo.tam/1e12:.1f}T")
        print(f"  SAM: ${mo.sam/1e9:.0f}B")
        print(f"  SOM: ${mo.som/1e9:.0f}B")
        print(f"  市场增长率: {mo.market_growth_rate*100:.0f}%")
        print(f"  当前市占率: {mo.market_share*100:.0f}%")
        print(f"  扩张机会: {', '.join(mo.expansion_opportunities)}")
        
        # 关键优势
        print(f"\n【关键优势】")
        for i, strength in enumerate(report.key_strengths, 1):
            print(f"  {i}. {strength}")
        
        # 风险因素
        print(f"\n【风险因素】")
        for i, risk in enumerate(report.risk_factors, 1):
            print(f"  {i}. {risk}")
        
        # 投资建议
        print(f"\n【投资建议】")
        if report.overall_score >= 80:
            print(f"  ✅ 强烈推荐：该标的具备优秀的增长前景和竞争优势，建议重仓配置")
            print(f"  📈 策略：长期持有，逢低加仓")
        elif report.overall_score >= 70:
            print(f"  ✅ 推荐：该标的具备良好的成长潜力，建议积极配置")
            print(f"  📈 策略：逐步建仓，关注季度业绩")
        else:
            print(f"  ⚠️ 观望：该标的吸引力有限，建议谨慎")
            print(f"  📊 策略：等待更好的入场时机")
        
        print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description='多头研究分析')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--analysis-depth', default='full', 
                       choices=['basic', 'full', 'comprehensive'],
                       help='分析深度')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建分析器
    analyzer = BullCaseAnalyzer(args.symbol, args.output)
    
    # 执行分析
    report = analyzer.analyze(args.analysis_depth)
    
    # 保存和打印报告
    analyzer.save_report(report)
    analyzer.print_report(report)


if __name__ == '__main__':
    main()
