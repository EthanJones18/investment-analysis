#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
估值分析脚本
支持DCF、PE、PB等多种估值方法

使用方法:
    python valuation.py --symbol AAPL --method dcf,pe,pb
"""

import argparse
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd


class ValuationModel:
    """估值模型"""
    
    def __init__(self, financial_data, market_data):
        """
        初始化
        
        Args:
            financial_data: 财务数据
            market_data: 市场数据（股价、股本等）
        """
        self.financial = financial_data
        self.market = market_data
    
    # ==================== DCF估值 ====================
    
    def dcf_valuation(self, 
                      growth_rate=0.05,
                      terminal_growth=0.025,
                      discount_rate=0.10,
                      forecast_years=5):
        """
        现金流贴现模型
        
        Args:
            growth_rate: 预测期增长率
            terminal_growth: 永续增长率
            discount_rate: 贴现率（WACC）
            forecast_years: 预测年数
            
        Returns:
            dict: DCF估值结果
        """
        # 获取当前自由现金流
        if 'free_cashflow' in self.financial.columns:
            current_fcf = self.financial['free_cashflow'].iloc[-1]
        elif 'operating_cashflow' in self.financial.columns and 'capex' in self.financial.columns:
            current_fcf = self.financial['operating_cashflow'].iloc[-1] - self.financial['capex'].iloc[-1]
        else:
            # 用净利润估算
            current_fcf = self.financial['net_income'].iloc[-1] * 0.8
        
        # 预测未来现金流
        forecasted_fcf = []
        for year in range(1, forecast_years + 1):
            fcf = current_fcf * (1 + growth_rate) ** year
            forecasted_fcf.append(fcf)
        
        # 计算预测期现值
        pv_forecast = sum([
            fcf / (1 + discount_rate) ** (year + 1)
            for year, fcf in enumerate(forecasted_fcf)
        ])
        
        # 计算终值
        terminal_fcf = forecasted_fcf[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / (1 + discount_rate) ** forecast_years
        
        # 企业价值
        enterprise_value = pv_forecast + pv_terminal
        
        # 股权价值（减去净债务）
        if 'total_liabilities' in self.financial.columns and 'cash' in self.financial.columns:
            net_debt = self.financial['total_liabilities'].iloc[-1] - self.financial.get('cash', pd.Series([0])).iloc[-1]
        else:
            net_debt = 0
        
        equity_value = enterprise_value - net_debt
        
        # 每股价值
        shares_outstanding = self.market.get('shares_outstanding', 1)
        value_per_share = equity_value / shares_outstanding
        
        return {
            'method': 'DCF',
            'current_fcf': round(current_fcf, 2),
            'growth_rate': growth_rate,
            'terminal_growth': terminal_growth,
            'discount_rate': discount_rate,
            'pv_forecast': round(pv_forecast, 2),
            'pv_terminal': round(pv_terminal, 2),
            'enterprise_value': round(enterprise_value, 2),
            'equity_value': round(equity_value, 2),
            'value_per_share': round(value_per_share, 2),
            'current_price': self.market.get('current_price', 0),
            'upside': round((value_per_share / self.market.get('current_price', 1) - 1) * 100, 2) if self.market.get('current_price') else None
        }
    
    # ==================== PE估值 ====================
    
    def pe_valuation(self, target_pe=None):
        """
        市盈率估值
        
        Args:
            target_pe: 目标PE（如不提供则使用历史平均）
            
        Returns:
            dict: PE估值结果
        """
        eps = self.financial['net_income'].iloc[-1] / self.market.get('shares_outstanding', 1)
        
        if target_pe is None:
            # 使用历史平均PE或行业平均
            target_pe = 15  # 默认值
        
        value_per_share = eps * target_pe
        
        return {
            'method': 'PE',
            'eps': round(eps, 2),
            'target_pe': target_pe,
            'value_per_share': round(value_per_share, 2),
            'current_price': self.market.get('current_price', 0),
            'current_pe': round(self.market.get('current_price', 0) / eps, 2) if eps > 0 else None,
            'upside': round((value_per_share / self.market.get('current_price', 1) - 1) * 100, 2) if self.market.get('current_price') else None
        }
    
    # ==================== PB估值 ====================
    
    def pb_valuation(self, target_pb=None):
        """
        市净率估值
        
        Args:
            target_pb: 目标PB（如不提供则使用历史平均）
            
        Returns:
            dict: PB估值结果
        """
        bvps = self.financial['equity'].iloc[-1] / self.market.get('shares_outstanding', 1)
        
        if target_pb is None:
            # 使用历史平均PB或行业平均
            target_pb = 2.0  # 默认值
        
        value_per_share = bvps * target_pb
        
        return {
            'method': 'PB',
            'bvps': round(bvps, 2),
            'target_pb': target_pb,
            'value_per_share': round(value_per_share, 2),
            'current_price': self.market.get('current_price', 0),
            'current_pb': round(self.market.get('current_price', 0) / bvps, 2) if bvps > 0 else None,
            'upside': round((value_per_share / self.market.get('current_price', 1) - 1) * 100, 2) if self.market.get('current_price') else None
        }
    
    # ==================== PEG估值 ====================
    
    def peg_valuation(self):
        """
        PEG估值（适用于成长股）
        
        Returns:
            dict: PEG估值结果
        """
        eps = self.financial['net_income'].iloc[-1] / self.market.get('shares_outstanding', 1)
        
        # 计算盈利增长率
        if len(self.financial) >= 2:
            earnings_growth = (self.financial['net_income'].iloc[-1] / self.financial['net_income'].iloc[0]) ** (1 / (len(self.financial) - 1)) - 1
        else:
            earnings_growth = 0.10  # 默认10%
        
        current_pe = self.market.get('current_price', 0) / eps if eps > 0 else 0
        peg = current_pe / (earnings_growth * 100) if earnings_growth > 0 else float('inf')
        
        # PEG < 1 被认为低估
        fair_pe = earnings_growth * 100  # 假设PEG=1为合理
        value_per_share = eps * fair_pe
        
        return {
            'method': 'PEG',
            'eps': round(eps, 2),
            'earnings_growth': round(earnings_growth, 4),
            'current_pe': round(current_pe, 2),
            'peg': round(peg, 2),
            'value_per_share': round(value_per_share, 2),
            'current_price': self.market.get('current_price', 0),
            'upside': round((value_per_share / self.market.get('current_price', 1) - 1) * 100, 2) if self.market.get('current_price') else None
        }
    
    def run_all_valuations(self):
        """运行所有估值方法"""
        results = {
            'dcf': self.dcf_valuation(),
            'pe': self.pe_valuation(),
            'pb': self.pb_valuation(),
            'peg': self.peg_valuation()
        }
        
        # 计算平均估值
        values = [r['value_per_share'] for r in results.values() if r.get('value_per_share')]
        if values:
            results['average'] = {
                'value_per_share': round(np.mean(values), 2),
                'current_price': self.market.get('current_price', 0),
                'upside': round((np.mean(values) / self.market.get('current_price', 1) - 1) * 100, 2) if self.market.get('current_price') else None
            }
        
        return results


def main():
    parser = argparse.ArgumentParser(description='估值分析工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--method', default='dcf,pe,pb', help='估值方法，逗号分隔')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 模拟财务数据
    financial_data = pd.DataFrame({
        'year': [2020, 2021, 2022, 2023, 2024],
        'net_income': [57411, 94680, 99803, 96995, 97000],
        'operating_cashflow': [80674, 116000, 122000, 118000, 118000],
        'capex': [7309, 11000, 12000, 11500, 11500],
        'free_cashflow': [73365, 105000, 110000, 106500, 106500],
        'total_liabilities': [258549, 274910, 286661, 301328, 301328],
        'equity': [65339, 63090, 65339, 50672, 50672],
        'cash': [38016, 34940, 36565, 30795, 30795]
    })
    
    # 模拟市场数据
    market_data = {
        'current_price': 225,
        'shares_outstanding': 15200000000  # 152亿股
    }
    
    # 估值
    model = ValuationModel(financial_data, market_data)
    
    methods = args.method.split(',')
    results = {}
    
    for method in methods:
        method = method.strip().lower()
        if method == 'dcf':
            results['DCF'] = model.dcf_valuation()
        elif method == 'pe':
            results['PE'] = model.pe_valuation()
        elif method == 'pb':
            results['PB'] = model.pb_valuation()
        elif method == 'peg':
            results['PEG'] = model.peg_valuation()
    
    # 计算平均估值
    values = [r['value_per_share'] for r in results.values() if r.get('value_per_share')]
    if values:
        results['综合估值'] = {
            'value_per_share': round(np.mean(values), 2),
            'current_price': market_data['current_price'],
            'upside': round((np.mean(values) / market_data['current_price'] - 1) * 100, 2)
        }
    
    # 保存结果
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_valuation.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'估值分析报告 - {args.symbol}')
    print('=' * 60)
    
    for method, result in results.items():
        print(f'\n【{method}】')
        print(f'  每股价值: {result.get("value_per_share", "N/A")}')
        print(f'  当前股价: {result.get("current_price", "N/A")}')
        upside = result.get('upside')
        if upside is not None:
            print(f'  上涨空间: {upside}%')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
