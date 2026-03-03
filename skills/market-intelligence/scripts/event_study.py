#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件研究脚本
分析特定事件对股价的影响

使用方法:
    python event_study.py --symbol AAPL --event earnings --date 2025-01-30 --window 30
"""

import argparse
import json
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


class EventStudy:
    """事件研究"""
    
    def __init__(self, symbol):
        """
        初始化
        
        Args:
            symbol: 股票代码
        """
        self.symbol = symbol
    
    def fetch_price_data(self, start_date, end_date):
        """
        获取股价数据（模拟）
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame: 股价数据
        """
        # 实际应用中应调用数据API
        # 这里使用模拟数据
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        np.random.seed(42)
        
        # 生成模拟股价（随机游走）
        returns = np.random.normal(0.001, 0.02, len(dates))
        price = 100 * np.exp(np.cumsum(returns))
        
        df = pd.DataFrame({
            'date': dates,
            'close': price,
            'volume': np.random.randint(1000000, 10000000, len(dates))
        })
        df.set_index('date', inplace=True)
        
        return df
    
    def calculate_returns(self, price_data):
        """
        计算收益率
        
        Args:
            price_data: 股价数据
            
        Returns:
            Series: 日收益率
        """
        return price_data['close'].pct_change().dropna()
    
    def calculate_abnormal_returns(self, returns, market_returns=None):
        """
        计算异常收益率
        
        Args:
            returns: 个股收益率
            market_returns: 市场收益率（如不提供则使用均值调整）
            
        Returns:
            Series: 异常收益率
        """
        if market_returns is None:
            # 使用均值调整模型
            normal_return = returns.mean()
            abnormal_returns = returns - normal_return
        else:
            # 使用市场调整模型
            abnormal_returns = returns - market_returns
        
        return abnormal_returns
    
    def event_study_analysis(self, event_date, window=30):
        """
        事件研究分析
        
        Args:
            event_date: 事件日期
            window: 事件窗口（前后天数）
            
        Returns:
            dict: 分析结果
        """
        event_date = pd.to_datetime(event_date)
        
        # 定义窗口
        estimation_start = event_date - timedelta(days=window*2)
        estimation_end = event_date - timedelta(days=window+1)
        event_start = event_date - timedelta(days=window)
        event_end = event_date + timedelta(days=window)
        
        # 获取数据
        price_data = self.fetch_price_data(estimation_start, event_end)
        returns = self.calculate_returns(price_data)
        
        # 分割数据
        estimation_returns = returns[estimation_start:estimation_end]
        event_returns = returns[event_start:event_end]
        
        # 计算异常收益率
        abnormal_returns = self.calculate_abnormal_returns(returns)
        event_abnormal = abnormal_returns[event_start:event_end]
        
        # 累计异常收益率 (CAR)
        car = event_abnormal.cumsum()
        
        # 统计检验
        car_mean = car.mean()
        car_std = car.std()
        car_tstat = car_mean / (car_std / np.sqrt(len(car)))
        
        # 事件日反应
        event_day_ar = event_abnormal.get(event_date, 0)
        
        return {
            'event_date': event_date.strftime('%Y-%m-%d'),
            'window': window,
            'estimation_period': f'{estimation_start.date()} to {estimation_end.date()}',
            'event_period': f'{event_start.date()} to {event_end.date()}',
            'cumulative_abnormal_return': round(car.iloc[-1], 4),
            'car_mean': round(car_mean, 4),
            'car_std': round(car_std, 4),
            'car_tstat': round(car_tstat, 4),
            'event_day_abnormal_return': round(event_day_ar, 4),
            'significance': '显著' if abs(car_tstat) > 1.96 else '不显著',
            'daily_returns': event_returns.round(4).to_dict(),
            'abnormal_returns': event_abnormal.round(4).to_dict(),
            'cumulative_returns': car.round(4).to_dict()
        }
    
    def analyze_earnings_event(self, earnings_date, eps_estimate, eps_actual):
        """
        财报事件分析
        
        Args:
            earnings_date: 财报日期
            eps_estimate: 预期EPS
            eps_actual: 实际EPS
            
        Returns:
            dict: 分析结果
        """
        # 计算超预期幅度
        surprise = (eps_actual - eps_estimate) / abs(eps_estimate) if eps_estimate != 0 else 0
        
        # 事件研究
        event_result = self.event_study_analysis(earnings_date, window=10)
        
        # 判断市场反应
        if surprise > 0.1 and event_result['event_day_abnormal_return'] > 0:
            reaction = '正面反应（业绩超预期+股价上涨）'
        elif surprise < -0.1 and event_result['event_day_abnormal_return'] < 0:
            reaction = '负面反应（业绩低于预期+股价下跌）'
        elif surprise > 0 and event_result['event_day_abnormal_return'] < 0:
            reaction = '卖出事实（利好出尽）'
        elif surprise < 0 and event_result['event_day_abnormal_return'] > 0:
            reaction = '利空出尽（股价已提前反应）'
        else:
            reaction = '反应平淡'
        
        return {
            'event_type': 'earnings',
            'earnings_date': earnings_date,
            'eps_estimate': eps_estimate,
            'eps_actual': eps_actual,
            'eps_surprise': round(surprise, 4),
            'surprise_pct': round(surprise * 100, 2),
            'market_reaction': reaction,
            'event_study': event_result
        }


def main():
    parser = argparse.ArgumentParser(description='事件研究工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--event', required=True, choices=['earnings', 'announcement', 'merger'],
                       help='事件类型')
    parser.add_argument('--date', required=True, help='事件日期 (YYYY-MM-DD)')
    parser.add_argument('--window', type=int, default=30, help='事件窗口天数')
    parser.add_argument('--eps-estimate', type=float, help='预期EPS（财报事件）')
    parser.add_argument('--eps-actual', type=float, help='实际EPS（财报事件）')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化
    study = EventStudy(args.symbol)
    
    # 执行分析
    if args.event == 'earnings':
        if args.eps_estimate is None or args.eps_actual is None:
            print('财报事件分析需要提供 --eps-estimate 和 --eps-actual')
            return
        result = study.analyze_earnings_event(args.date, args.eps_estimate, args.eps_actual)
    else:
        result = study.event_study_analysis(args.date, args.window)
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_event_study.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'事件研究报告 - {args.symbol}')
    print('=' * 60)
    
    print(f'\n【事件信息】')
    print(f'  事件类型: {args.event}')
    print(f'  事件日期: {args.date}')
    
    if args.event == 'earnings':
        print(f'  预期EPS: {args.eps_estimate}')
        print(f'  实际EPS: {args.eps_actual}')
        print(f'  超预期幅度: {result["surprise_pct"]}%')
        print(f'  市场反应: {result["market_reaction"]}')
    
    if 'event_study' in result:
        es = result['event_study']
    else:
        es = result
    
    print(f'\n【事件研究分析】')
    print(f'  估计窗口: {es["estimation_period"]}')
    print(f'  事件窗口: {es["event_period"]}')
    print(f'  累计异常收益率(CAR): {es["cumulative_abnormal_return"]:.2%}')
    print(f'  事件日异常收益: {es["event_day_abnormal_return"]:.2%}')
    print(f'  T统计量: {es["car_tstat"]:.2f}')
    print(f'  显著性: {es["significance"]}')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
