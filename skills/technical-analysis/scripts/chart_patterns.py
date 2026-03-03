#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表形态识别脚本
识别支撑阻力、趋势线、K线形态等

使用方法:
    python chart_patterns.py --symbol AAPL --pattern support_resistance,trendline
"""

import argparse
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema


class ChartPatterns:
    """图表形态识别器"""
    
    def __init__(self, df):
        """
        初始化
        
        Args:
            df: DataFrame包含OHLCV数据
        """
        self.df = df.copy()
    
    def find_support_resistance(self, window=5, tolerance=0.02):
        """
        识别支撑阻力位
        
        Args:
            window: 极值点查找窗口
            tolerance: 价格容忍度（百分比）
            
        Returns:
            dict: 支撑位和阻力位列表
        """
        close = self.df['close']
        
        # 找局部高点（阻力位候选）
        local_max = argrelextrema(close.values, np.greater, order=window)[0]
        resistance_levels = close.iloc[local_max].values
        
        # 找局部低点（支撑位候选）
        local_min = argrelextrema(close.values, np.less, order=window)[0]
        support_levels = close.iloc[local_min].values
        
        # 合并相近的价格水平
        def merge_levels(levels, tolerance):
            if len(levels) == 0:
                return []
            
            levels = sorted(levels)
            merged = [[levels[0], 1]]  # [价格, 触碰次数]
            
            for price in levels[1:]:
                # 检查是否与已有水平接近
                found = False
                for i, (level, count) in enumerate(merged):
                    if abs(price - level) / level < tolerance:
                        # 更新平均水平
                        merged[i][0] = (level * count + price) / (count + 1)
                        merged[i][1] += 1
                        found = True
                        break
                
                if not found:
                    merged.append([price, 1])
            
            # 按触碰次数排序，返回重要的水平
            merged = sorted(merged, key=lambda x: x[1], reverse=True)
            return [round(level[0], 2) for level in merged[:5]]
        
        support = merge_levels(support_levels, tolerance)
        resistance = merge_levels(resistance_levels, tolerance)
        
        # 当前价格附近的支撑阻力
        current_price = close.iloc[-1]
        
        nearest_support = None
        nearest_resistance = None
        
        for s in support:
            if s < current_price:
                nearest_support = s
                break
        
        for r in resistance:
            if r > current_price:
                nearest_resistance = r
                break
        
        return {
            'support_levels': support,
            'resistance_levels': resistance,
            'current_price': round(current_price, 2),
            'nearest_support': nearest_support,
            'nearest_resistance': nearest_resistance,
            'support_distance': round((current_price - nearest_support) / current_price * 100, 2) if nearest_support else None,
            'resistance_distance': round((nearest_resistance - current_price) / current_price * 100, 2) if nearest_resistance else None
        }
    
    def find_trendlines(self, window=5):
        """
        识别趋势线
        
        Args:
            window: 极值点查找窗口
            
        Returns:
            dict: 上升趋势线和下降趋势线
        """
        close = self.df['close']
        
        # 找局部高点和低点
        local_max_idx = argrelextrema(close.values, np.greater, order=window)[0]
        local_min_idx = argrelextrema(close.values, np.less, order=window)[0]
        
        # 简单的线性拟合找趋势线
        def fit_trendline(indices, prices):
            if len(indices) < 2:
                return None
            
            x = np.array(indices)
            y = prices[indices]
            
            # 线性拟合
            coeffs = np.polyfit(x, y, 1)
            slope = coeffs[0]
            intercept = coeffs[1]
            
            # 计算R²
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_squared,
                'start_price': round(y[0], 2),
                'end_price': round(y[-1], 2)
            }
        
        # 上升趋势线（连接低点）
        uptrend = fit_trendline(local_min_idx, close.values)
        
        # 下降趋势线（连接高点）
        downtrend = fit_trendline(local_max_idx, close.values)
        
        return {
            'uptrend': uptrend,
            'downtrend': downtrend,
            'current_trend': 'up' if uptrend and uptrend['r_squared'] > 0.7 else ('down' if downtrend and downtrend['r_squared'] > 0.7 else 'sideways')
        }
    
    def identify_candlestick_patterns(self):
        """
        识别K线形态
        
        Returns:
            list: 最近识别的K线形态
        """
        patterns = []
        
        o = self.df['open']
        h = self.df['high']
        l = self.df['low']
        c = self.df['close']
        
        # 计算K线实体和影线
        body = abs(c - o)
        upper_shadow = h - np.maximum(o, c)
        lower_shadow = np.minimum(o, c) - l
        
        # 最近5天的形态识别
        for i in range(-5, 0):
            pattern = None
            
            # 锤子线（Hammer）
            if lower_shadow.iloc[i] > 2 * body.iloc[i] and upper_shadow.iloc[i] < body.iloc[i]:
                if c.iloc[i] > o.iloc[i]:
                    pattern = '锤子线（看涨）'
                else:
                    pattern = '倒锤子线（看跌）'
            
            # 十字星（Doji）
            elif body.iloc[i] <= 0.1 * (h.iloc[i] - l.iloc[i]):
                pattern = '十字星'
            
            # 吞没形态（Engulfing）
            if i > -len(self.df):
                prev_body = abs(c.iloc[i-1] - o.iloc[i-1])
                curr_body = body.iloc[i]
                
                # 看涨吞没
                if c.iloc[i-1] < o.iloc[i-1] and c.iloc[i] > o.iloc[i]:
                    if o.iloc[i] < c.iloc[i-1] and c.iloc[i] > o.iloc[i-1] and curr_body > prev_body:
                        pattern = '看涨吞没'
                
                # 看跌吞没
                elif c.iloc[i-1] > o.iloc[i-1] and c.iloc[i] < o.iloc[i]:
                    if o.iloc[i] > c.iloc[i-1] and c.iloc[i] < o.iloc[i-1] and curr_body > prev_body:
                        pattern = '看跌吞没'
            
            if pattern:
                patterns.append({
                    'date': self.df.index[i].strftime('%Y-%m-%d') if isinstance(self.df.index[i], pd.Timestamp) else str(self.df.index[i]),
                    'pattern': pattern,
                    'open': round(o.iloc[i], 2),
                    'high': round(h.iloc[i], 2),
                    'low': round(l.iloc[i], 2),
                    'close': round(c.iloc[i], 2)
                })
        
        return patterns
    
    def generate_report(self, patterns_list):
        """
        生成形态识别报告
        
        Args:
            patterns_list: 要识别的形态列表
            
        Returns:
            dict: 报告数据
        """
        report = {
            'symbol': 'AAPL',
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'patterns': {}
        }
        
        for pattern in patterns_list:
            pattern = pattern.lower().strip()
            
            if pattern == 'support_resistance':
                report['patterns']['support_resistance'] = self.find_support_resistance()
            elif pattern == 'trendline':
                report['patterns']['trendline'] = self.find_trendlines()
            elif pattern == 'candlestick':
                report['patterns']['candlestick'] = self.identify_candlestick_patterns()
        
        return report


def main():
    parser = argparse.ArgumentParser(description='图表形态识别工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--pattern', required=True, help='形态列表，逗号分隔')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建模拟数据
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    np.random.seed(42)
    
    close = 100 + np.cumsum(np.random.randn(100) * 2)
    df = pd.DataFrame({
        'open': close + np.random.randn(100),
        'high': close + abs(np.random.randn(100)) + 1,
        'low': close - abs(np.random.randn(100)) - 1,
        'close': close,
        'volume': np.random.randint(1000000, 10000000, 100)
    }, index=dates)
    
    # 识别形态
    cp = ChartPatterns(df)
    patterns = args.pattern.split(',')
    report = cp.generate_report(patterns)
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_patterns.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'图表形态识别报告 - {args.symbol}')
    print('=' * 60)
    
    if 'support_resistance' in report['patterns']:
        sr = report['patterns']['support_resistance']
        print(f'\n【支撑阻力位】')
        print(f'当前价格: {sr["current_price"]}')
        print(f'支撑位: {sr["support_levels"]}')
        print(f'阻力位: {sr["resistance_levels"]}')
        print(f'最近支撑: {sr["nearest_support"]} (距离 {sr["support_distance"]}%)')
        print(f'最近阻力: {sr["nearest_resistance"]} (距离 {sr["resistance_distance"]}%)')
    
    if 'trendline' in report['patterns']:
        tl = report['patterns']['trendline']
        print(f'\n【趋势线】')
        print(f'当前趋势: {tl["current_trend"]}')
    
    if 'candlestick' in report['patterns']:
        cs = report['patterns']['candlestick']
        print(f'\n【K线形态】')
        for p in cs:
            print(f'  {p["date"]}: {p["pattern"]}')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
