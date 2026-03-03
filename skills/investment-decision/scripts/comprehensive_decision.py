#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合投资决策分析脚本
整合七大维度分析，给出最终投资建议

使用方法:
    python comprehensive_decision.py --symbol BABA --analysis-depth full
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class DimensionScore:
    """维度评分"""
    name: str
    weight: float
    score: float
    rating: str
    key_points: List[str]
    risks: List[str]
    opportunities: List[str]


@dataclass
class InvestmentDecision:
    """投资决策报告"""
    symbol: str
    analysis_date: str
    overall_score: float
    investment_rating: str
    recommendation: str
    position_size: str
    stop_loss: Optional[str]
    target_return: Optional[str]
    time_horizon: str
    dimension_scores: List[DimensionScore]
    key_risks: List[str]
    key_opportunities: List[str]
    catalysts: List[str]
    monitoring_metrics: List[str]


class InvestmentDecisionEngine:
    """投资决策引擎"""
    
    # 维度权重配置
    DIMENSION_WEIGHTS = {
        "macro": 0.15,
        "fundamental": 0.25,
        "technical": 0.15,
        "market_intelligence": 0.15,
        "geopolitical": 0.10,
        "bull_case": 0.10,
        "bear_case": 0.10
    }
    
    # 模拟数据
    MOCK_DATA = {
        "BABA": {
            "name": "阿里巴巴",
            "sector": "Technology",
            "dimensions": {
                "macro": {
                    "score": 65,
                    "key_points": [
                        "中国经济复苏缓慢",
                        "消费信心有待恢复",
                        "货币政策相对宽松"
                    ],
                    "risks": ["经济下行风险", "消费疲软"],
                    "opportunities": ["政策刺激预期", "复苏弹性大"]
                },
                "fundamental": {
                    "score": 72,
                    "key_points": [
                        "营收增长放缓但稳定",
                        "云计算业务增长强劲",
                        "利润率逐步改善",
                        "现金流健康"
                    ],
                    "risks": ["电商竞争加剧", "增长放缓"],
                    "opportunities": ["云计算高增长", "国际化扩张"]
                },
                "technical": {
                    "score": 58,
                    "key_points": [
                        "股价处于长期下行趋势",
                        "近期有企稳迹象",
                        "成交量萎缩",
                        "关键支撑位80美元"
                    ],
                    "risks": ["趋势仍偏空", "缺乏上涨动能"],
                    "opportunities": ["超跌反弹", "底部形成"]
                },
                "market_intelligence": {
                    "score": 62,
                    "key_points": [
                        "市场情绪偏谨慎",
                        "机构持仓有所下降",
                        "新闻情绪中性偏正面",
                        "做空比例适中"
                    ],
                    "risks": ["外资流出压力", "情绪脆弱"],
                    "opportunities": ["估值修复预期", "情绪改善空间"]
                },
                "geopolitical": {
                    "score": 45,
                    "key_points": [
                        "中美关系紧张",
                        "中概股监管风险",
                        "审计底稿问题",
                        "技术封锁风险"
                    ],
                    "risks": ["退市风险", "制裁升级", "政策不确定性"],
                    "opportunities": ["监管缓和预期", "中美关系改善"]
                },
                "bull_case": {
                    "score": 75,
                    "key_points": [
                        "电商市场地位稳固",
                        "云计算第二增长曲线",
                        "估值处于历史低位",
                        "股东回报改善"
                    ],
                    "risks": [],
                    "opportunities": ["估值修复", "业务分拆", "AI应用"]
                },
                "bear_case": {
                    "score": 55,
                    "key_points": [
                        "增长放缓明显",
                        "竞争压力加大",
                        "监管环境严峻",
                        "地缘政治风险"
                    ],
                    "risks": ["增长停滞", "份额流失", "监管加码"],
                    "opportunities": []
                }
            }
        },
        "NVDA": {
            "name": "英伟达",
            "sector": "Technology",
            "dimensions": {
                "macro": {
                    "score": 70,
                    "key_points": [
                        "美联储降息预期",
                        "AI投资热潮持续",
                        "科技股整体向好"
                    ],
                    "risks": ["利率风险", "经济衰退"],
                    "opportunities": ["AI浪潮", "流动性改善"]
                },
                "fundamental": {
                    "score": 88,
                    "key_points": [
                        "营收增长强劲",
                        "毛利率极高",
                        "现金流充沛",
                        "ROE优秀"
                    ],
                    "risks": ["估值过高", "增长可持续性"],
                    "opportunities": ["AI芯片垄断", "数据中心扩张"]
                },
                "technical": {
                    "score": 82,
                    "key_points": [
                        "长期上升趋势",
                        "近期创新高",
                        "成交量配合",
                        "均线多头排列"
                    ],
                    "risks": ["超买状态", "回调风险"],
                    "opportunities": ["趋势延续", "突破新高"]
                },
                "market_intelligence": {
                    "score": 85,
                    "key_points": [
                        "市场情绪极度乐观",
                        "机构一致看好",
                        "新闻情绪正面",
                        "资金持续流入"
                    ],
                    "risks": ["情绪过热", "预期过高"],
                    "opportunities": ["AI叙事持续", "机构增配"]
                },
                "geopolitical": {
                    "score": 60,
                    "key_points": [
                        "中美科技竞争",
                        "芯片出口管制",
                        "供应链风险",
                        "地缘政治紧张"
                    ],
                    "risks": ["出口限制", "供应链中断"],
                    "opportunities": ["国产替代需求", "全球AI需求"]
                },
                "bull_case": {
                    "score": 92,
                    "key_points": [
                        "AI芯片绝对龙头",
                        "数据中心需求爆发",
                        "技术护城河深厚",
                        "新市场拓展"
                    ],
                    "risks": [],
                    "opportunities": ["AI普及", "自动驾驶", "机器人"]
                },
                "bear_case": {
                    "score": 40,
                    "key_points": [
                        "估值过高",
                        "竞争加剧",
                        "地缘政治风险",
                        "增长放缓预期"
                    ],
                    "risks": ["估值回调", "竞争加剧"],
                    "opportunities": []
                }
            }
        },
        "TSLA": {
            "name": "特斯拉",
            "sector": "Automotive",
            "dimensions": {
                "macro": {
                    "score": 65,
                    "key_points": [
                        "电动车政策支持",
                        "利率环境改善",
                        "消费复苏缓慢"
                    ],
                    "risks": ["经济下行", "消费疲软"],
                    "opportunities": ["政策支持", "渗透率提升"]
                },
                "fundamental": {
                    "score": 68,
                    "key_points": [
                        "销量增长放缓",
                        "价格战影响利润",
                        "现金流健康",
                        "毛利率承压"
                    ],
                    "risks": ["增长放缓", "利润下滑"],
                    "opportunities": ["新车型推出", "FSD商业化"]
                },
                "technical": {
                    "score": 55,
                    "key_points": [
                        "股价大幅回调",
                        "处于震荡区间",
                        "成交量萎缩",
                        "趋势不明朗"
                    ],
                    "risks": ["趋势偏弱", "支撑不稳"],
                    "opportunities": ["超跌反弹", "底部震荡"]
                },
                "market_intelligence": {
                    "score": 58,
                    "key_points": [
                        "市场情绪分化",
                        "机构观点不一",
                        "看空声音增加",
                        "资金流出明显"
                    ],
                    "risks": ["情绪转空", "资金流出"],
                    "opportunities": ["情绪修复", "预期差"]
                },
                "geopolitical": {
                    "score": 55,
                    "key_points": [
                        "中美贸易摩擦",
                        "供应链本地化",
                        "数据安全法规",
                        "关税风险"
                    ],
                    "risks": ["关税增加", "供应链中断"],
                    "opportunities": ["本地化生产", "政策优惠"]
                },
                "bull_case": {
                    "score": 70,
                    "key_points": [
                        "电动车龙头地位",
                        "FSD技术领先",
                        "能源业务增长",
                        "机器人前景"
                    ],
                    "risks": [],
                    "opportunities": ["FSD普及", "Robotaxi", "Optimus"]
                },
                "bear_case": {
                    "score": 65,
                    "key_points": [
                        "竞争加剧",
                        "价格战持续",
                        "增长放缓",
                        "估值仍高"
                    ],
                    "risks": ["份额流失", "利润压缩"],
                    "opportunities": []
                }
            }
        }
    }
    
    def __init__(self, symbol: str, output_dir: str = "./output"):
        self.symbol = symbol
        self.output_dir = output_dir
        self.data = self.MOCK_DATA.get(symbol, self.MOCK_DATA["BABA"])
    
    def analyze(self) -> InvestmentDecision:
        """执行综合投资决策分析"""
        print(f"\n{'='*70}")
        print(f"综合投资决策分析 - {self.symbol}")
        print(f"{'='*70}")
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"公司名称: {self.data['name']}")
        print(f"所属行业: {self.data['sector']}")
        
        # 分析各维度
        dimension_scores = []
        
        print(f"\n{'='*70}")
        print("多维度分析")
        print(f"{'='*70}")
        
        for dim_name, weight in self.DIMENSION_WEIGHTS.items():
            print(f"\n【{self._get_dimension_name(dim_name)}】权重: {weight*100:.0f}%")
            
            dim_data = self.data["dimensions"][dim_name]
            score = dim_data["score"]
            
            # 确定评级
            rating = self._get_dimension_rating(score)
            
            print(f"  评分: {score}/100 | 评级: {rating}")
            
            # 关键点
            print(f"\n  关键发现:")
            for point in dim_data["key_points"]:
                print(f"    • {point}")
            
            dimension_scores.append(DimensionScore(
                name=self._get_dimension_name(dim_name),
                weight=weight,
                score=score,
                rating=rating,
                key_points=dim_data["key_points"],
                risks=dim_data.get("risks", []),
                opportunities=dim_data.get("opportunities", [])
            ))
        
        # 计算综合评分
        overall_score = self._calculate_overall_score(dimension_scores)
        
        # 生成投资建议
        investment_rating, recommendation, position_size, stop_loss, target_return = \
            self._generate_recommendation(overall_score)
        
        # 汇总关键风险和机会
        key_risks = self._aggregate_risks(dimension_scores)
        key_opportunities = self._aggregate_opportunities(dimension_scores)
        
        # 催化剂和监控指标
        catalysts = self._generate_catalysts()
        monitoring_metrics = self._generate_monitoring_metrics()
        
        # 构建决策报告
        decision = InvestmentDecision(
            symbol=self.symbol,
            analysis_date=datetime.now().isoformat(),
            overall_score=overall_score,
            investment_rating=investment_rating,
            recommendation=recommendation,
            position_size=position_size,
            stop_loss=stop_loss,
            target_return=target_return,
            time_horizon="6-12个月",
            dimension_scores=dimension_scores,
            key_risks=key_risks,
            key_opportunities=key_opportunities,
            catalysts=catalysts,
            monitoring_metrics=monitoring_metrics
        )
        
        return decision
    
    def _get_dimension_name(self, key: str) -> str:
        """获取维度中文名"""
        names = {
            "macro": "宏观分析",
            "fundamental": "基本面分析",
            "technical": "技术分析",
            "market_intelligence": "市场信息分析",
            "geopolitical": "地缘政治分析",
            "bull_case": "多头分析",
            "bear_case": "空头分析"
        }
        return names.get(key, key)
    
    def _get_dimension_rating(self, score: float) -> str:
        """获取维度评级"""
        if score >= 80:
            return "优秀"
        elif score >= 70:
            return "良好"
        elif score >= 60:
            return "一般"
        elif score >= 50:
            return "偏弱"
        else:
            return "较差"
    
    def _calculate_overall_score(self, dimensions: List[DimensionScore]) -> float:
        """计算综合评分"""
        total_score = sum(d.score * d.weight for d in dimensions)
        return round(total_score, 1)
    
    def _generate_recommendation(self, score: float) -> Tuple[str, str, str, Optional[str], Optional[str]]:
        """生成投资建议"""
        if score >= 90:
            return "强烈买入", "强烈建议买入，长期持有", "20-30%", "-8%", "+30%"
        elif score >= 80:
            return "买入", "建议买入，积极配置", "15-20%", "-7%", "+25%"
        elif score >= 70:
            return "增持", "建议增持，适度配置", "10-15%", "-6%", "+20%"
        elif score >= 60:
            return "持有", "建议持有，观望", "5-10%", "-5%", "+15%"
        elif score >= 50:
            return "减持", "建议减持，降低仓位", "0-5%", None, None
        elif score >= 40:
            return "卖出", "建议卖出，规避风险", "清仓", None, None
        else:
            return "强烈卖出", "强烈建议卖出或做空", "做空/对冲", None, None
    
    def _aggregate_risks(self, dimensions: List[DimensionScore]) -> List[str]:
        """汇总风险"""
        all_risks = []
        for d in dimensions:
            all_risks.extend(d.risks)
        # 去重并取前10个
        unique_risks = list(dict.fromkeys(all_risks))
        return unique_risks[:10]
    
    def _aggregate_opportunities(self, dimensions: List[DimensionScore]) -> List[str]:
        """汇总机会"""
        all_opps = []
        for d in dimensions:
            all_opps.extend(d.opportunities)
        # 去重并取前10个
        unique_opps = list(dict.fromkeys(all_opps))
        return unique_opps[:10]
    
    def _generate_catalysts(self) -> List[str]:
        """生成催化剂"""
        return [
            "季度业绩发布",
            "行业政策变化",
            "宏观经济数据",
            "美联储货币政策",
            "地缘政治事件",
            "技术创新突破",
            "竞争格局变化",
            "监管政策调整"
        ]
    
    def _generate_monitoring_metrics(self) -> List[str]:
        """生成监控指标"""
        return [
            "营收增长率",
            "利润率变化",
            "市场份额",
            "估值水平(PE/PB)",
            "机构持仓变化",
            "做空比例",
            "技术指标(均线/RSI)",
            "新闻情绪指数"
        ]
    
    def save_report(self, decision: InvestmentDecision):
        """保存报告"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(
            self.output_dir,
            f"{self.symbol}_investment_decision.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(decision), f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存: {output_file}")
        return output_file
    
    def print_report(self, decision: InvestmentDecision):
        """打印报告"""
        print(f"\n{'='*70}")
        print("投资决策报告")
        print(f"{'='*70}")
        
        # 执行摘要
        print(f"\n【执行摘要】")
        print(f"  标的: {decision.symbol}")
        print(f"  综合评分: {decision.overall_score}/100")
        print(f"  投资评级: {decision.investment_rating}")
        print(f"  核心建议: {decision.recommendation}")
        
        # 投资建议详情
        print(f"\n【投资建议详情】")
        print(f"  建议仓位: {decision.position_size}")
        if decision.stop_loss:
            print(f"  止损位: {decision.stop_loss}")
        if decision.target_return:
            print(f"  目标收益: {decision.target_return}")
        print(f"  时间周期: {decision.time_horizon}")
        
        # 各维度评分汇总
        print(f"\n【各维度评分汇总】")
        for d in decision.dimension_scores:
            bar = "█" * int(d.score / 10) + "░" * (10 - int(d.score / 10))
            print(f"  {d.name:12s} [{bar}] {d.score:5.1f}/100 ({d.rating})")
        
        # 关键风险
        print(f"\n【关键风险因素】")
        for i, risk in enumerate(decision.key_risks, 1):
            print(f"  {i}. {risk}")
        
        # 关键机会
        print(f"\n【关键机会因素】")
        for i, opp in enumerate(decision.key_opportunities, 1):
            print(f"  {i}. {opp}")
        
        # 催化剂
        print(f"\n【潜在催化剂】")
        for i, cat in enumerate(decision.catalysts, 1):
            print(f"  {i}. {cat}")
        
        # 监控指标
        print(f"\n【监控指标】")
        for i, metric in enumerate(decision.monitoring_metrics, 1):
            print(f"  {i}. {metric}")
        
        # 风险提示
        print(f"\n【风险提示】")
        print("  ⚠️ 本分析仅供参考，不构成投资建议")
        print("  ⚠️ 投资有风险，入市需谨慎")
        print("  ⚠️ 请根据自身风险承受能力做出投资决策")
        print("  ⚠️ 建议分散投资，控制单一标的仓位")
        
        print(f"\n{'='*70}")


def main():
    parser = argparse.ArgumentParser(description='综合投资决策分析')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建决策引擎
    engine = InvestmentDecisionEngine(args.symbol, args.output)
    
    # 执行分析
    decision = engine.analyze()
    
    # 保存和打印报告
    engine.save_report(decision)
    engine.print_report(decision)


if __name__ == '__main__':
    main()
