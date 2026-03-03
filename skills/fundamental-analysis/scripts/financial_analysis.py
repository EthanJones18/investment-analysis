#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务报表分析脚本
分析三大报表，计算关键财务指标

使用方法:
    python financial_analysis.py --symbol AAPL --report all --period 5y
"""

import argparse
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd


class FinancialAnalyzer:
    """财务报表分析器"""
    
    def __init__(self, financial_data):
        """
        初始化
        
        Args:
            financial_data: 包含财务报表数据的DataFrame
        """
        self.data = financial_data
    
    # ==================== 盈利能力分析 ====================
    
    def calculate_profitability_ratios(self):
        """计算盈利能力指标"""
        ratios = {}
        
        # ROE (净资产收益率)
        if 'net_income' in self.data.columns and 'equity' in self.data.columns:
            ratios['roe'] = self.data['net_income'] / self.data['equity']
        
        # ROA (总资产收益率)
        if 'net_income' in self.data.columns and 'total_assets' in self.data.columns:
            ratios['roa'] = self.data['net_income'] / self.data['total_assets']
        
        # ROIC (投入资本回报率)
        if 'ebit' in self.data.columns and 'invested_capital' in self.data.columns:
            ratios['roic'] = self.data['ebit'] * (1 - 0.25) / self.data['invested_capital']
        
        # 毛利率
        if 'gross_profit' in self.data.columns and 'revenue' in self.data.columns:
            ratios['gross_margin'] = self.data['gross_profit'] / self.data['revenue']
        
        # 净利率
        if 'net_income' in self.data.columns and 'revenue' in self.data.columns:
            ratios['net_margin'] = self.data['net_income'] / self.data['revenue']
        
        # 营业利润率
        if 'operating_income' in self.data.columns and 'revenue' in self.data.columns:
            ratios['operating_margin'] = self.data['operating_income'] / self.data['revenue']
        
        return pd.DataFrame(ratios)
    
    # ==================== 偿债能力分析 ====================
    
    def calculate_solvency_ratios(self):
        """计算偿债能力指标"""
        ratios = {}
        
        # 资产负债率
        if 'total_liabilities' in self.data.columns and 'total_assets' in self.data.columns:
            ratios['debt_to_asset'] = self.data['total_liabilities'] / self.data['total_assets']
        
        # 权益乘数
        if 'total_assets' in self.data.columns and 'equity' in self.data.columns:
            ratios['equity_multiplier'] = self.data['total_assets'] / self.data['equity']
        
        # 流动比率
        if 'current_assets' in self.data.columns and 'current_liabilities' in self.data.columns:
            ratios['current_ratio'] = self.data['current_assets'] / self.data['current_liabilities']
        
        # 速动比率
        if 'current_assets' in self.data.columns and 'inventory' in self.data.columns and 'current_liabilities' in self.data.columns:
            ratios['quick_ratio'] = (self.data['current_assets'] - self.data['inventory']) / self.data['current_liabilities']
        
        # 利息保障倍数
        if 'ebit' in self.data.columns and 'interest_expense' in self.data.columns:
            ratios['interest_coverage'] = self.data['ebit'] / self.data['interest_expense']
        
        return pd.DataFrame(ratios)
    
    # ==================== 运营效率分析 ====================
    
    def calculate_efficiency_ratios(self):
        """计算运营效率指标"""
        ratios = {}
        
        # 总资产周转率
        if 'revenue' in self.data.columns and 'total_assets' in self.data.columns:
            ratios['asset_turnover'] = self.data['revenue'] / self.data['total_assets']
        
        # 存货周转率
        if 'cogs' in self.data.columns and 'inventory' in self.data.columns:
            ratios['inventory_turnover'] = self.data['cogs'] / self.data['inventory']
        
        # 应收账款周转率
        if 'revenue' in self.data.columns and 'accounts_receivable' in self.data.columns:
            ratios['receivables_turnover'] = self.data['revenue'] / self.data['accounts_receivable']
        
        return pd.DataFrame(ratios)
    
    # ==================== 成长能力分析 ====================
    
    def calculate_growth_ratios(self):
        """计算成长能力指标"""
        growth = {}
        
        # 营收增长率
        if 'revenue' in self.data.columns:
            growth['revenue_growth'] = self.data['revenue'].pct_change()
        
        # 净利润增长率
        if 'net_income' in self.data.columns:
            growth['net_income_growth'] = self.data['net_income'].pct_change()
        
        # 营业利润增长率
        if 'operating_income' in self.data.columns:
            growth['operating_income_growth'] = self.data['operating_income'].pct_change()
        
        # 总资产增长率
        if 'total_assets' in self.data.columns:
            growth['asset_growth'] = self.data['total_assets'].pct_change()
        
        return pd.DataFrame(growth)
    
    # ==================== 现金流分析 ====================
    
    def calculate_cashflow_ratios(self):
        """计算现金流指标"""
        ratios = {}
        
        # 经营现金流/净利润
        if 'operating_cashflow' in self.data.columns and 'net_income' in self.data.columns:
            ratios['ocf_to_netincome'] = self.data['operating_cashflow'] / self.data['net_income']
        
        # 自由现金流
        if 'operating_cashflow' in self.data.columns and 'capex' in self.data.columns:
            ratios['free_cashflow'] = self.data['operating_cashflow'] - self.data['capex']
        
        # 经营现金流/营收
        if 'operating_cashflow' in self.data.columns and 'revenue' in self.data.columns:
            ratios['ocf_to_revenue'] = self.data['operating_cashflow'] / self.data['revenue']
        
        return pd.DataFrame(ratios)
    
    def generate_report(self):
        """生成完整财务分析报告"""
        report = {
            'symbol': 'AAPL',
            'analysis_date': datetime.now().strftime('%Y-%m-%d'),
            'profitability': self.calculate_profitability_ratios().iloc[-1].to_dict() if not self.calculate_profitability_ratios().empty else {},
            'solvency': self.calculate_solvency_ratios().iloc[-1].to_dict() if not self.calculate_solvency_ratios().empty else {},
            'efficiency': self.calculate_efficiency_ratios().iloc[-1].to_dict() if not self.calculate_efficiency_ratios().empty else {},
            'growth': self.calculate_growth_ratios().iloc[-1].to_dict() if not self.calculate_growth_ratios().empty else {},
            'cashflow': self.calculate_cashflow_ratios().iloc[-1].to_dict() if not self.calculate_cashflow_ratios().empty else {}
        }
        
        return report


def main():
    parser = argparse.ArgumentParser(description='财务报表分析工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--report', default='all', choices=['all', 'profitability', 'solvency', 'efficiency', 'growth'],
                       help='报告类型')
    parser.add_argument('--period', default='5y', help='分析周期')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建模拟财务数据
    years = pd.date_range(end=datetime.now(), periods=5, freq='Y')
    
    # 模拟数据（实际应从API获取）
    data = pd.DataFrame({
        'year': years,
        'revenue': [365000, 394000, 383000, 394000, 383000],  # 百万美元
        'net_income': [94680, 99803, 96995, 97000, 97000],
        'total_assets': [338000, 352000, 352000, 352000, 352000],
        'equity': [63090, 65339, 50672, 50672, 50672],
        'total_liabilities': [274910, 286661, 301328, 301328, 301328],
        'current_assets': [135000, 140000, 135000, 135000, 135000],
        'current_liabilities': [125000, 130000, 125000, 125000, 125000],
        'inventory': [5000, 5500, 5200, 5200, 5200],
        'gross_profit': [152000, 170000, 165000, 165000, 165000],
        'operating_income': [108000, 119000, 115000, 115000, 115000],
        'ebit': [108000, 119000, 115000, 115000, 115000],
        'interest_expense': [3000, 3200, 3100, 3100, 3100],
        'operating_cashflow': [116000, 122000, 118000, 118000, 118000],
        'capex': [11000, 12000, 11500, 11500, 11500],
        'accounts_receivable': [25000, 26000, 25500, 25500, 25500]
    })
    
    # 分析
    analyzer = FinancialAnalyzer(data)
    report = analyzer.generate_report()
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_financial_analysis.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'财务分析报告 - {args.symbol}')
    print('=' * 60)
    
    print('\n【盈利能力】')
    for k, v in report['profitability'].items():
        if pd.notna(v):
            print(f'  {k}: {v:.2%}')
    
    print('\n【偿债能力】')
    for k, v in report['solvency'].items():
        if pd.notna(v):
            print(f'  {k}: {v:.2f}')
    
    print('\n【运营效率】')
    for k, v in report['efficiency'].items():
        if pd.notna(v):
            print(f'  {k}: {v:.2f}')
    
    print('\n【成长能力】')
    for k, v in report['growth'].items():
        if pd.notna(v):
            print(f'  {k}: {v:.2%}')
    
    print('\n【现金流】')
    for k, v in report['cashflow'].items():
        if pd.notna(v):
            print(f'  {k}: {v:.2f}')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
