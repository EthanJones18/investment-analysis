#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
杜邦分析脚本
ROE三因素分解分析

使用方法:
    python dupont_analysis.py --symbol AAPL --period 5y
"""

import argparse
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DupontAnalysis:
    """杜邦分析器"""
    
    def __init__(self, financial_data):
        """
        初始化
        
        Args:
            financial_data: 财务数据DataFrame
        """
        self.data = financial_data
    
    def calculate_dupont(self):
        """
        计算杜邦分析三因素
        
        Returns:
            DataFrame: 杜邦分析结果
        """
        dupont = pd.DataFrame(index=self.data.index)
        
        # 净利润率 = 净利润 / 营业收入
        dupont['net_margin'] = self.data['net_income'] / self.data['revenue']
        
        # 资产周转率 = 营业收入 / 总资产
        dupont['asset_turnover'] = self.data['revenue'] / self.data['total_assets']
        
        # 权益乘数 = 总资产 / 净资产
        dupont['equity_multiplier'] = self.data['total_assets'] / self.data['equity']
        
        # ROE = 净利润率 × 资产周转率 × 权益乘数
        dupont['roe'] = dupont['net_margin'] * dupont['asset_turnover'] * dupont['equity_multiplier']
        
        # 验证：直接计算ROE
        dupont['roe_direct'] = self.data['net_income'] / self.data['equity']
        
        return dupont
    
    def analyze_roe_drivers(self):
        """
        分析ROE驱动因素变化
        
        Returns:
            dict: 分析报告
        """
        dupont = self.calculate_dupont()
        
        # 计算各因素对ROE变化的贡献
        roe_change = dupont['roe'].iloc[-1] - dupont['roe'].iloc[0]
        
        # 简化分析：计算各因素的变化
        margin_change = dupont['net_margin'].iloc[-1] - dupont['net_margin'].iloc[0]
        turnover_change = dupont['asset_turnover'].iloc[-1] - dupont['asset_turnover'].iloc[0]
        leverage_change = dupont['equity_multiplier'].iloc[-1] - dupont['equity_multiplier'].iloc[0]
        
        # 判断ROE质量
        latest = dupont.iloc[-1]
        
        quality = []
        if latest['net_margin'] > 0.15:
            quality.append('高利润率')
        elif latest['net_margin'] > 0.10:
            quality.append('中等利润率')
        else:
            quality.append('低利润率')
        
        if latest['asset_turnover'] > 1.0:
            quality.append('高周转率')
        elif latest['asset_turnover'] > 0.5:
            quality.append('中等周转率')
        else:
            quality.append('低周转率')
        
        if latest['equity_multiplier'] > 3:
            quality.append('高杠杆')
        elif latest['equity_multiplier'] > 2:
            quality.append('中等杠杆')
        else:
            quality.append('低杠杆')
        
        # 商业模式判断
        if latest['net_margin'] > 0.15 and latest['asset_turnover'] < 0.5:
            business_model = '高利润低周转模式（如奢侈品、软件）'
        elif latest['net_margin'] < 0.10 and latest['asset_turnover'] > 1.0:
            business_model = '低利润高周转模式（如零售、超市）'
        elif latest['net_margin'] > 0.10 and latest['asset_turnover'] > 0.5:
            business_model = '平衡模式（如制造业）'
        else:
            business_model = '需关注模式'
        
        return {
            'roe_change': round(roe_change, 4),
            'margin_change': round(margin_change, 4),
            'turnover_change': round(turnover_change, 4),
            'leverage_change': round(leverage_change, 4),
            'latest_roe': round(latest['roe'], 4),
            'latest_margin': round(latest['net_margin'], 4),
            'latest_turnover': round(latest['asset_turnover'], 4),
            'latest_leverage': round(latest['equity_multiplier'], 4),
            'quality': quality,
            'business_model': business_model
        }
    
    def plot_dupont(self, output_path):
        """
        绘制杜邦分析图表
        
        Args:
            output_path: 输出路径
        """
        dupont = self.calculate_dupont()
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # ROE趋势
        axes[0, 0].plot(dupont.index, dupont['roe'] * 100, marker='o', linewidth=2)
        axes[0, 0].set_title('ROE趋势 (%)', fontsize=14)
        axes[0, 0].set_ylabel('ROE (%)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 三因素趋势
        axes[0, 1].plot(dupont.index, dupont['net_margin'] * 100, marker='o', label='净利润率')
        axes[0, 1].plot(dupont.index, dupont['asset_turnover'], marker='s', label='资产周转率')
        axes[0, 1].plot(dupont.index, (dupont['equity_multiplier'] - 1) * 10, marker='^', label='权益乘数(缩放)')
        axes[0, 1].set_title('杜邦三因素趋势', fontsize=14)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # ROE构成（最新一期）
        latest = dupont.iloc[-1]
        factors = ['净利润率', '资产周转率', '权益乘数']
        values = [latest['net_margin'], latest['asset_turnover'], latest['equity_multiplier'] / 10]
        axes[1, 0].bar(factors, values, color=['#3498db', '#2ecc71', '#e74c3c'])
        axes[1, 0].set_title('ROE构成（最新）', fontsize=14)
        axes[1, 0].set_ylabel('数值')
        
        # ROE分解瀑布图
        base_roe = dupont['roe'].iloc[0]
        changes = [
            base_roe,
            dupont['net_margin'].iloc[-1] * dupont['asset_turnover'].iloc[0] * dupont['equity_multiplier'].iloc[0] - base_roe,
            dupont['net_margin'].iloc[-1] * dupont['asset_turnover'].iloc[-1] * dupont['equity_multiplier'].iloc[0] - dupont['net_margin'].iloc[-1] * dupont['asset_turnover'].iloc[0] * dupont['equity_multiplier'].iloc[0],
            dupont['roe'].iloc[-1] - dupont['net_margin'].iloc[-1] * dupont['asset_turnover'].iloc[-1] * dupont['equity_multiplier'].iloc[0]
        ]
        
        cumulative = [base_roe]
        for c in changes[1:]:
            cumulative.append(cumulative[-1] + c)
        
        axes[1, 1].bar(['期初ROE', '利润率影响', '周转率影响', '杠杆影响'], 
                       [base_roe * 100] + [c * 100 for c in changes[1:]],
                       color=['gray', '#3498db', '#2ecc71', '#e74c3c'])
        axes[1, 1].set_title('ROE变化分解', fontsize=14)
        axes[1, 1].set_ylabel('ROE (%)')
        axes[1, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path


def main():
    parser = argparse.ArgumentParser(description='杜邦分析工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--period', default='5y', help='分析周期')
    parser.add_argument('--output', default='./output', help='输出目录')
    parser.add_argument('--plot', action='store_true', help='生成图表')
    
    args = parser.parse_args()
    
    # 模拟财务数据
    data = pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024],
        'revenue': [274515, 365817, 394328, 383285, 391035],
        'net_income': [57411, 94680, 99803, 96995, 97000],
        'total_assets': [323888, 351002, 352755, 352583, 352583],
        'equity': [65339, 63090, 65339, 50672, 50672]
    })
    
    # 杜邦分析
    analyzer = DupontAnalysis(data)
    dupont = analyzer.calculate_dupont()
    analysis = analyzer.analyze_roe_drivers()
    
    # 保存结果
    os.makedirs(args.output, exist_ok=True)
    
    # 保存数据
    output_csv = os.path.join(args.output, f'{args.symbol}_dupont.csv')
    dupont.to_csv(output_csv)
    
    # 保存分析
    output_json = os.path.join(args.output, f'{args.symbol}_dupont_analysis.json')
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
    
    # 生成图表
    if args.plot:
        output_png = os.path.join(args.output, f'{args.symbol}_dupont.png')
        analyzer.plot_dupont(output_png)
    
    # 打印报告
    print('=' * 60)
    print(f'杜邦分析报告 - {args.symbol}')
    print('=' * 60)
    
    print('\n【ROE分解】')
    print(f'  最新ROE: {analysis["latest_roe"]:.2%}')
    print(f'  净利润率: {analysis["latest_margin"]:.2%}')
    print(f'  资产周转率: {analysis["latest_turnover"]:.2f}')
    print(f'  权益乘数: {analysis["latest_leverage"]:.2f}')
    
    print('\n【ROE变化分析】')
    print(f'  ROE变化: {analysis["roe_change"]:.2%}')
    print(f'  利润率贡献: {analysis["margin_change"]:.2%}')
    print(f'  周转率贡献: {analysis["turnover_change"]:.2f}')
    print(f'  杠杆率贡献: {analysis["leverage_change"]:.2f}')
    
    print('\n【质量评估】')
    print(f'  特征: {", ".join(analysis["quality"])}')
    print(f'  商业模式: {analysis["business_model"]}')
    
    print('=' * 60)
    print(f'报告已保存: {output_json}')
    if args.plot:
        print(f'图表已保存: {output_png}')


if __name__ == '__main__':
    main()
