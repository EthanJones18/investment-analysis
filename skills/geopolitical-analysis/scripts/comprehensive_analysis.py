#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地缘政治综合分析脚本
整合事件监控、情景分析、资产影响评估

使用方法:
    python comprehensive_analysis.py --symbol BABA --watch-regions east_asia --days 30
"""

import argparse
import json
import os
from datetime import datetime

# 导入监控模块
from geopolitical_monitor import GDELTClient, EventSeverity


class GeopoliticalAnalyzer:
    """地缘政治综合分析器"""
    
    # 地区-国家映射
    REGION_COUNTRIES = {
        "east_asia": ["CHN", "JPN", "KOR", "TWN"],
        "middle_east": ["IRN", "ISR", "SAU", "IRQ", "SYR"],
        "europe": ["RUS", "UKR", "DEU", "FRA", "GBR"],
        "south_asia": ["IND", "PAK", "AFG"],
        "americas": ["USA", "CAN", "MEX", "BRA"]
    }
    
    # 资产-地区暴露映射
    ASSET_EXPOSURE = {
        "BABA": {
            "regions": ["east_asia"],
            "countries": ["CHN"],
            "sectors": ["tech", "ecommerce"],
            "exposure_type": "direct"
        },
        "AAPL": {
            "regions": ["east_asia", "americas"],
            "countries": ["CHN", "USA"],
            "sectors": ["tech"],
            "exposure_type": "indirect"
        },
        "TSLA": {
            "regions": ["east_asia", "americas"],
            "countries": ["CHN", "USA"],
            "sectors": ["auto", "tech"],
            "exposure_type": "direct"
        },
        "GLD": {
            "regions": ["global"],
            "countries": [],
            "sectors": ["commodity"],
            "exposure_type": "sentiment"
        }
    }
    
    def __init__(self, symbol: str, output_dir: str = "./output"):
        self.symbol = symbol
        self.output_dir = output_dir
        self.gdelt_client = GDELTClient()
        
        # 获取资产暴露信息
        self.asset_info = self.ASSET_EXPOSURE.get(symbol, {
            "regions": ["global"],
            "countries": [],
            "sectors": [],
            "exposure_type": "unknown"
        })
    
    def analyze(self, watch_regions: list = None, days: int = 30) -> dict:
        """
        执行综合分析
        
        Args:
            watch_regions: 监控地区列表
            days: 监控天数
            
        Returns:
            综合分析报告
        """
        print(f"\n开始地缘政治综合分析 - {self.symbol}")
        print("=" * 60)
        
        # 确定监控国家
        watch_countries = []
        if watch_regions:
            for region in watch_regions:
                watch_countries.extend(self.REGION_COUNTRIES.get(region, []))
        
        # 添加资产相关国家
        watch_countries.extend(self.asset_info.get("countries", []))
        watch_countries = list(set(watch_countries))  # 去重
        
        print(f"\n监控国家: {', '.join(watch_countries)}")
        
        # 1. 获取地缘政治事件
        print(f"\n步骤 1/3: 获取地缘政治事件...")
        events = self.gdelt_client.fetch_events(
            countries=watch_countries if watch_countries else None,
            days=days
        )
        print(f"  获取到 {len(events)} 条事件")
        
        # 2. 评估资产影响
        print(f"\n步骤 2/3: 评估资产影响...")
        impact_assessment = self._assess_impact(events)
        
        # 3. 生成情景分析
        print(f"\n步骤 3/3: 生成情景分析...")
        scenarios = self._generate_scenarios(events)
        
        # 构建报告
        report = {
            "symbol": self.symbol,
            "analysis_date": datetime.now().isoformat(),
            "analysis_period_days": days,
            "asset_exposure": self.asset_info,
            "event_summary": self._summarize_events(events),
            "impact_assessment": impact_assessment,
            "scenarios": scenarios,
            "recommendations": self._generate_recommendations(impact_assessment, scenarios),
            "events": [e.to_dict() for e in events]
        }
        
        return report
    
    def _summarize_events(self, events: list) -> dict:
        """汇总事件统计"""
        if not events:
            return {"count": 0, "severity_breakdown": {}, "type_breakdown": {}}
        
        severity_counts = {}
        type_counts = {}
        
        for event in events:
            sev = event.severity.name
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            evt_type = event.event_type.value
            type_counts[evt_type] = type_counts.get(evt_type, 0) + 1
        
        return {
            "count": len(events),
            "severity_breakdown": severity_counts,
            "type_breakdown": type_counts,
            "critical_events": [e.to_dict() for e in events if e.severity == EventSeverity.CRITICAL],
            "high_events": [e.to_dict() for e in events if e.severity == EventSeverity.HIGH]
        }
    
    def _assess_impact(self, events: list) -> dict:
        """评估资产影响"""
        if not events:
            return {
                "overall_score": 0,
                "risk_level": "low",
                "confidence": 0,
                "factors": []
            }
        
        # 计算整体影响分数
        total_score = 0
        weights = []
        factors = []
        
        for event in events:
            # 根据严重程度给分
            severity_score = event.severity.value / 5.0  # 0.2 - 1.0
            
            # 根据事件类型调整
            type_multiplier = self._get_type_multiplier(event.event_type)
            
            # 计算权重（越新的事件权重越高）
            weight = 1.0  # 简化处理
            
            event_score = severity_score * type_multiplier
            total_score += event_score * weight
            weights.append(weight)
            
            if event.severity.value >= 4:  # HIGH及以上
                factors.append({
                    "event": event.title,
                    "severity": event.severity.name,
                    "type": event.event_type.value,
                    "impact": "negative" if type_multiplier < 0 else "positive"
                })
        
        # 归一化分数
        if weights:
            overall_score = total_score / sum(weights)
        else:
            overall_score = 0
        
        # 确定风险级别
        if overall_score >= 0.7:
            risk_level = "critical"
        elif overall_score >= 0.4:
            risk_level = "high"
        elif overall_score >= 0.2:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "overall_score": round(overall_score, 4),
            "risk_level": risk_level,
            "confidence": round(min(1.0, len(events) / 10), 2),
            "factors": factors[:5]  # 前5个重要因素
        }
    
    def _get_type_multiplier(self, event_type) -> float:
        """获取事件类型乘数"""
        multipliers = {
            "conflict": -1.0,
            "sanction": -0.8,
            "trade": -0.6,
            "terrorism": -0.7,
            "cyber": -0.5,
            "diplomatic": -0.3,
            "economic": -0.2,
            "election": -0.3,
            "other": -0.1
        }
        return multipliers.get(event_type.value, -0.1)
    
    def _generate_scenarios(self, events: list) -> list:
        """生成情景分析"""
        scenarios = []
        
        # 基准情景
        scenarios.append({
            "name": "基准情景 (Base Case)",
            "probability": 0.5,
            "description": "地缘政治局势维持现状，无重大突发事件",
            "asset_impact": "中性",
            "indicators": ["无重大冲突升级", "外交渠道畅通"]
        })
        
        # 检查是否有高风险事件
        high_risk_events = [e for e in events if e.severity.value >= 4]
        
        if high_risk_events:
            # 悲观情景
            scenarios.append({
                "name": "悲观情景 (Bear Case)",
                "probability": 0.3,
                "description": f"地缘政治紧张局势升级，{len(high_risk_events)}个高风险事件恶化",
                "asset_impact": "负面 -10%至-20%",
                "indicators": ["冲突扩大", "新制裁措施", "外交关系恶化"]
            })
            
            # 极端情景
            scenarios.append({
                "name": "极端情景 (Tail Risk)",
                "probability": 0.1,
                "description": "黑天鹅事件发生，地缘政治格局剧变",
                "asset_impact": "严重负面 -30%以上",
                "indicators": ["战争爆发", "重大恐怖袭击", "政权更迭"]
            })
        
        # 乐观情景
        scenarios.append({
            "name": "乐观情景 (Bull Case)",
            "probability": 0.2 if high_risk_events else 0.3,
            "description": "地缘政治紧张局势缓解，外交突破",
            "asset_impact": "正面 +5%至+15%",
            "indicators": ["谈判进展", "制裁解除", "合作协议签署"]
        })
        
        return scenarios
    
    def _generate_recommendations(self, impact: dict, scenarios: list) -> list:
        """生成投资建议"""
        recommendations = []
        
        risk_level = impact.get("risk_level", "low")
        score = impact.get("overall_score", 0)
        
        if risk_level == "critical":
            recommendations.append({
                "priority": "🔴 紧急",
                "action": "立即避险",
                "details": "地缘政治风险极高，建议立即减仓或对冲"
            })
        elif risk_level == "high":
            recommendations.append({
                "priority": "🟠 高",
                "action": "减仓对冲",
                "details": "地缘政治风险较高，建议降低仓位并配置避险资产"
            })
        elif risk_level == "medium":
            recommendations.append({
                "priority": "🟡 中",
                "action": "加强监控",
                "details": "地缘政治风险中等，建议密切关注事态发展"
            })
        else:
            recommendations.append({
                "priority": "🟢 低",
                "action": "正常持仓",
                "details": "地缘政治风险较低，可按正常策略操作"
            })
        
        # 添加通用建议
        recommendations.append({
            "priority": "📊 监控",
            "action": "持续跟踪",
            "details": "建议每日检查地缘政治事件更新，特别是HIGH及以上级别事件"
        })
        
        return recommendations
    
    def save_report(self, report: dict):
        """保存分析报告"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(
            self.output_dir,
            f"{self.symbol}_geopolitical_analysis.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n报告已保存: {output_file}")
        return output_file
    
    def print_report(self, report: dict):
        """打印分析报告"""
        print("\n" + "=" * 60)
        print(f"地缘政治分析报告 - {self.symbol}")
        print("=" * 60)
        
        # 资产暴露
        print(f"\n【资产暴露】")
        exposure = report["asset_exposure"]
        print(f"  地区: {', '.join(exposure['regions'])}")
        print(f"  国家: {', '.join(exposure['countries'])}")
        print(f"  行业: {', '.join(exposure['sectors'])}")
        print(f"  暴露类型: {exposure['exposure_type']}")
        
        # 事件汇总
        print(f"\n【事件汇总】")
        summary = report["event_summary"]
        print(f"  总事件数: {summary['count']}")
        
        if summary["severity_breakdown"]:
            print(f"\n  严重程度分布:")
            for sev, count in sorted(summary["severity_breakdown"].items(), 
                                     key=lambda x: -ord(x[0][0])):
                print(f"    • {sev}: {count}条")
        
        # 影响评估
        print(f"\n【影响评估】")
        impact = report["impact_assessment"]
        print(f"  整体分数: {impact['overall_score']}")
        print(f"  风险级别: {impact['risk_level'].upper()}")
        print(f"  置信度: {impact['confidence']}")
        
        if impact["factors"]:
            print(f"\n  关键风险因素:")
            for factor in impact["factors"]:
                print(f"    • [{factor['severity']}] {factor['event'][:50]}...")
        
        # 情景分析
        print(f"\n【情景分析】")
        for scenario in report["scenarios"]:
            print(f"\n  {scenario['name']}")
            print(f"    概率: {scenario['probability']*100:.0f}%")
            print(f"    描述: {scenario['description']}")
            print(f"    资产影响: {scenario['asset_impact']}")
        
        # 投资建议
        print(f"\n【投资建议】")
        for rec in report["recommendations"]:
            print(f"\n  {rec['priority']}")
            print(f"    行动: {rec['action']}")
            print(f"    详情: {rec['details']}")
        
        print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description='地缘政治综合分析')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--watch-regions', help='监控地区，逗号分隔')
    parser.add_argument('--days', type=int, default=30, help='监控天数')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 解析地区
    watch_regions = None
    if args.watch_regions:
        watch_regions = args.watch_regions.split(',')
    
    # 创建分析器
    analyzer = GeopoliticalAnalyzer(args.symbol, args.output)
    
    # 执行分析
    report = analyzer.analyze(
        watch_regions=watch_regions,
        days=args.days
    )
    
    # 保存和打印报告
    analyzer.save_report(report)
    analyzer.print_report(report)


if __name__ == '__main__':
    main()
