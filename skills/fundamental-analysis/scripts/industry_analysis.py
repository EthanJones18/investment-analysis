#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行业分析脚本
行业研究、竞争格局、市场规模分析

使用方法:
    python industry_analysis.py --industry "新能源汽车" --peers TSLA,BYD,NIO
"""

import argparse
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd


class IndustryAnalyzer:
    """行业分析器"""
    
    def __init__(self, industry_name):
        """
        初始化
        
        Args:
            industry_name: 行业名称
        """
        self.industry = industry_name
        self.data = {}
    
    # ==================== 市场规模分析 ====================
    
    def analyze_market_size(self, tam, sam, som, growth_rate):
        """
        市场规模分析 (TAM/SAM/SOM)
        
        Args:
            tam: 总可及市场 (Total Addressable Market)
            sam: 可服务市场 (Serviceable Addressable Market)
            som: 可获得市场 (Serviceable Obtainable Market)
            growth_rate: 年复合增长率
            
        Returns:
            dict: 市场分析结果
        """
        market_penetration = (som / tam) * 100 if tam > 0 else 0
        
        # 预测未来5年市场规模
        future_tam = tam * (1 + growth_rate) ** 5
        
        return {
            'tam': tam,
            'sam': sam,
            'som': som,
            'market_penetration': round(market_penetration, 2),
            'growth_rate': growth_rate,
            'future_tam_5y': round(future_tam, 2),
            'growth_stage': self._classify_growth_stage(growth_rate)
        }
    
    def _classify_growth_stage(self, growth_rate):
        """判断行业生命周期阶段"""
        if growth_rate > 0.30:
            return '导入期/高速成长期'
        elif growth_rate > 0.15:
            return '成长期'
        elif growth_rate > 0.05:
            return '成熟期'
        else:
            return '衰退期'
    
    # ==================== 波特五力分析 ====================
    
    def porter_five_forces(self, 
                          rivalry_intensity,
                          new_entrant_threat,
                          substitute_threat,
                          supplier_power,
                          buyer_power):
        """
        波特五力分析
        
        Args:
            rivalry_intensity: 现有竞争者竞争强度 (1-5)
            new_entrant_threat: 潜在进入者威胁 (1-5)
            substitute_threat: 替代品威胁 (1-5)
            supplier_power: 供应商议价能力 (1-5)
            buyer_power: 购买者议价能力 (1-5)
            
        Returns:
            dict: 五力分析结果
        """
        forces = {
            '现有竞争者竞争强度': {'score': rivalry_intensity, 'level': self._score_to_level(rivalry_intensity)},
            '潜在进入者威胁': {'score': new_entrant_threat, 'level': self._score_to_level(new_entrant_threat)},
            '替代品威胁': {'score': substitute_threat, 'level': self._score_to_level(substitute_threat)},
            '供应商议价能力': {'score': supplier_power, 'level': self._score_to_level(supplier_power)},
            '购买者议价能力': {'score': buyer_power, 'level': self._score_to_level(buyer_power)}
        }
        
        # 计算行业吸引力得分（越低越好）
        total_score = sum([f['score'] for f in forces.values()])
        avg_score = total_score / 5
        
        if avg_score <= 2:
            attractiveness = '高吸引力'
        elif avg_score <= 3:
            attractiveness = '中等吸引力'
        else:
            attractiveness = '低吸引力'
        
        return {
            'forces': forces,
            'total_score': total_score,
            'average_score': round(avg_score, 2),
            'attractiveness': attractiveness
        }
    
    def _score_to_level(self, score):
        """分数转等级"""
        if score <= 2:
            return '低'
        elif score <= 3:
            return '中'
        else:
            return '高'
    
    # ==================== 竞争格局分析 ====================
    
    def analyze_competitive_landscape(self, companies_data):
        """
        竞争格局分析
        
        Args:
            companies_data: 公司数据列表 [{name, market_share, revenue, growth}]
            
        Returns:
            dict: 竞争格局分析
        """
        df = pd.DataFrame(companies_data)
        
        # 计算CR4（前4名集中度）
        df_sorted = df.sort_values('market_share', ascending=False)
        cr4 = df_sorted.head(4)['market_share'].sum()
        
        # 判断竞争格局
        if cr4 >= 0.60:
            structure = '寡头垄断'
        elif cr4 >= 0.40:
            structure = '集中度较高'
        elif cr4 >= 0.20:
            structure = '集中度中等'
        else:
            structure = '分散竞争'
        
        # 计算赫芬达尔指数 (HHI)
        hhi = (df['market_share'] ** 2).sum() * 10000
        
        if hhi >= 2500:
            competition_level = '高度集中'
        elif hhi >= 1500:
            competition_level = '中度集中'
        else:
            competition_level = '低度集中'
        
        return {
            'cr4': round(cr4, 4),
            'hhi': round(hhi, 2),
            'market_structure': structure,
            'competition_level': competition_level,
            'leader': df_sorted.iloc[0]['name'] if len(df_sorted) > 0 else None,
            'leader_share': round(df_sorted.iloc[0]['market_share'], 4) if len(df_sorted) > 0 else 0,
            'companies': companies_data
        }
    
    # ==================== SWOT分析 ====================
    
    def swot_analysis(self, strengths, weaknesses, opportunities, threats):
        """
        SWOT分析
        
        Args:
            strengths: 优势列表
            weaknesses: 劣势列表
            opportunities: 机会列表
            threats: 威胁列表
            
        Returns:
            dict: SWOT分析结果
        """
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'opportunities': opportunities,
            'threats': threats,
            'so_strategy': self._generate_so_strategy(strengths, opportunities),
            'wo_strategy': self._generate_wo_strategy(weaknesses, opportunities),
            'st_strategy': self._generate_st_strategy(strengths, threats),
            'wt_strategy': self._generate_wt_strategy(weaknesses, threats)
        }
    
    def _generate_so_strategy(self, strengths, opportunities):
        """SO战略：利用优势抓住机会"""
        strategies = []
        for s in strengths[:2]:
            for o in opportunities[:2]:
                strategies.append(f"利用{s}，抓住{o}")
        return strategies
    
    def _generate_wo_strategy(self, weaknesses, opportunities):
        """WO战略：克服劣势抓住机会"""
        strategies = []
        for w in weaknesses[:2]:
            for o in opportunities[:2]:
                strategies.append(f"克服{w}，利用{o}")
        return strategies
    
    def _generate_st_strategy(self, strengths, threats):
        """ST战略：利用优势规避威胁"""
        strategies = []
        for s in strengths[:2]:
            for t in threats[:2]:
                strategies.append(f"利用{s}，应对{t}")
        return strategies
    
    def _generate_wt_strategy(self, weaknesses, threats):
        """WT战略：防御性战略"""
        strategies = []
        for w in weaknesses[:1]:
            for t in threats[:1]:
                strategies.append(f"解决{w}，防范{t}")
        return strategies
    
    # ==================== 价值链分析 ====================
    
    def value_chain_analysis(self, upstream, midstream, downstream):
        """
        价值链分析
        
        Args:
            upstream: 上游环节 [{activity, value_add, key_players}]
            midstream: 中游环节
            downstream: 下游环节
            
        Returns:
            dict: 价值链分析
        """
        total_value = sum([u['value_add'] for u in upstream]) + \
                      sum([m['value_add'] for m in midstream]) + \
                      sum([d['value_add'] for d in downstream])
        
        upstream_value = sum([u['value_add'] for u in upstream])
        midstream_value = sum([m['value_add'] for m in midstream])
        downstream_value = sum([d['value_add'] for d in downstream])
        
        return {
            'upstream': {
                'activities': upstream,
                'total_value': upstream_value,
                'value_share': round(upstream_value / total_value, 4) if total_value > 0 else 0
            },
            'midstream': {
                'activities': midstream,
                'total_value': midstream_value,
                'value_share': round(midstream_value / total_value, 4) if total_value > 0 else 0
            },
            'downstream': {
                'activities': downstream,
                'total_value': downstream_value,
                'value_share': round(downstream_value / total_value, 4) if total_value > 0 else 0
            },
            'total_value': total_value
        }
    
    def generate_report(self):
        """生成完整行业分析报告"""
        return {
            'industry': self.industry,
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'data': self.data
        }


def main():
    parser = argparse.ArgumentParser(description='行业分析工具')
    parser.add_argument('--industry', required=True, help='行业名称')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = IndustryAnalyzer(args.industry)
    
    # 示例：新能源汽车行业分析
    if args.industry == '新能源汽车':
        # 市场规模
        market = analyzer.analyze_market_size(
            tam=5000,  # 全球5000亿美元
            sam=1500,  # 中国1500亿美元
            som=300,   # 目标公司300亿美元
            growth_rate=0.25  # 25%年增长
        )
        analyzer.data['market_size'] = market
        
        # 波特五力
        five_forces = analyzer.porter_five_forces(
            rivalry_intensity=4,      # 竞争激烈
            new_entrant_threat=3,     # 进入门槛中等
            substitute_threat=2,      # 替代品威胁低
            supplier_power=3,         # 供应商议价中等
            buyer_power=3             # 买家议价中等
        )
        analyzer.data['porter_five_forces'] = five_forces
        
        # 竞争格局
        companies = [
            {'name': '比亚迪', 'market_share': 0.30, 'revenue': 600, 'growth': 0.40},
            {'name': '特斯拉', 'market_share': 0.20, 'revenue': 400, 'growth': 0.25},
            {'name': '蔚来', 'market_share': 0.08, 'revenue': 160, 'growth': 0.35},
            {'name': '小鹏', 'market_share': 0.06, 'revenue': 120, 'growth': 0.30},
            {'name': '理想', 'market_share': 0.10, 'revenue': 200, 'growth': 0.50},
            {'name': '其他', 'market_share': 0.26, 'revenue': 520, 'growth': 0.15}
        ]
        competitive = analyzer.analyze_competitive_landscape(companies)
        analyzer.data['competitive_landscape'] = competitive
        
        # SWOT
        swot = analyzer.swot_analysis(
            strengths=['技术领先', '政策支持', '产业链完整'],
            weaknesses=['充电设施不足', '成本较高', '续航里程焦虑'],
            opportunities=['碳中和目标', '智能化趋势', '出口增长'],
            threats=['原材料涨价', '补贴退坡', '传统车企转型']
        )
        analyzer.data['swot'] = swot
    
    # 生成报告
    report = analyzer.generate_report()
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.industry}_industry_analysis.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'行业分析报告 - {args.industry}')
    print('=' * 60)
    
    if 'market_size' in analyzer.data:
        m = analyzer.data['market_size']
        print(f'\n【市场规模】')
        print(f'  TAM (总市场): {m["tam"]} 亿美元')
        print(f'  SAM (可服务): {m["sam"]} 亿美元')
        print(f'  SOM (可获得): {m["som"]} 亿美元')
        print(f'  市场渗透率: {m["market_penetration"]}%')
        print(f'  年增长率: {m["growth_rate"]:.1%}')
        print(f'  5年后TAM: {m["future_tam_5y"]} 亿美元')
        print(f'  发展阶段: {m["growth_stage"]}')
    
    if 'porter_five_forces' in analyzer.data:
        p = analyzer.data['porter_five_forces']
        print(f'\n【波特五力分析】')
        for force, data in p['forces'].items():
            print(f'  {force}: {data["score"]}/5 ({data["level"]}威胁)')
        print(f'  行业吸引力: {p["attractiveness"]}')
    
    if 'competitive_landscape' in analyzer.data:
        c = analyzer.data['competitive_landscape']
        print(f'\n【竞争格局】')
        print(f'  CR4 (前4集中度): {c["cr4"]:.1%}')
        print(f'  HHI指数: {c["hhi"]:.0f}')
        print(f'  市场结构: {c["market_structure"]}')
        print(f'  竞争程度: {c["competition_level"]}')
        print(f'  行业龙头: {c["leader"]} ({c["leader_share"]:.1%})')
    
    if 'swot' in analyzer.data:
        s = analyzer.data['swot']
        print(f'\n【SWOT分析】')
        print(f'  优势: {", ".join(s["strengths"])}')
        print(f'  劣势: {", ".join(s["weaknesses"])}')
        print(f'  机会: {", ".join(s["opportunities"])}')
        print(f'  威胁: {", ".join(s["threats"])}')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
