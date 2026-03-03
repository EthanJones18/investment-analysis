#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪指数构建脚本
综合多种情绪数据源构建情绪指数

使用方法:
    python sentiment_index.py --symbol AAPL --components news,social,options
"""

import argparse
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd


class SentimentIndexBuilder:
    """情绪指数构建器"""
    
    def __init__(self, symbol):
        """
        初始化
        
        Args:
            symbol: 股票代码
        """
        self.symbol = symbol
        self.components = {}
    
    def fetch_news_sentiment(self):
        """获取新闻情绪数据（模拟）"""
        # 模拟新闻情绪数据
        return {
            'score': 0.25,
            'weight': 0.35,
            'source': 'news'
        }
    
    def fetch_social_sentiment(self):
        """获取社交媒体情绪数据（模拟）"""
        # 模拟社交媒体情绪数据
        return {
            'score': 0.15,
            'weight': 0.30,
            'source': 'social'
        }
    
    def fetch_options_sentiment(self):
        """获取期权情绪数据（模拟）"""
        # 模拟期权情绪数据（Put/Call Ratio等）
        put_call_ratio = 0.8  # 低于1表示乐观
        options_score = (1 - put_call_ratio) * 2 - 1  # 转换到-1到1
        
        return {
            'score': options_score,
            'weight': 0.20,
            'source': 'options'
        }
    
    def fetch_analyst_sentiment(self):
        """获取分析师情绪数据（模拟）"""
        # 模拟分析师评级
        ratings = {'buy': 15, 'hold': 8, 'sell': 2}
        total = sum(ratings.values())
        
        # 计算情绪分数
        analyst_score = (ratings['buy'] - ratings['sell']) / total
        
        return {
            'score': analyst_score,
            'weight': 0.15,
            'source': 'analyst'
        }
    
    def build_composite_index(self, components_list):
        """
        构建综合情绪指数
        
        Args:
            components_list: 组件列表
            
        Returns:
            dict: 情绪指数结果
        """
        components = []
        total_weight = 0
        weighted_score = 0
        
        # 获取各组件数据
        if 'news' in components_list:
            data = self.fetch_news_sentiment()
            components.append(data)
            weighted_score += data['score'] * data['weight']
            total_weight += data['weight']
        
        if 'social' in components_list:
            data = self.fetch_social_sentiment()
            components.append(data)
            weighted_score += data['score'] * data['weight']
            total_weight += data['weight']
        
        if 'options' in components_list:
            data = self.fetch_options_sentiment()
            components.append(data)
            weighted_score += data['score'] * data['weight']
            total_weight += data['weight']
        
        if 'analyst' in components_list:
            data = self.fetch_analyst_sentiment()
            components.append(data)
            weighted_score += data['score'] * data['weight']
            total_weight += data['weight']
        
        # 标准化
        if total_weight > 0:
            composite_score = weighted_score / total_weight
        else:
            composite_score = 0
        
        # 转换到0-100指数
        index_value = (composite_score + 1) * 50
        
        return {
            'composite_score': round(composite_score, 4),
            'index_value': round(index_value, 2),
            'components': components,
            'interpretation': self._interpret_index(index_value)
        }
    
    def _interpret_index(self, index_value):
        """解读情绪指数"""
        if index_value >= 80:
            return {
                'level': '极度乐观',
                'signal': '警惕过热，考虑减仓',
                'color': 'red'
            }
        elif index_value >= 60:
            return {
                'level': '乐观',
                'signal': '偏多，但注意风险',
                'color': 'orange'
            }
        elif index_value >= 40:
            return {
                'level': '中性',
                'signal': '观望，等待方向',
                'color': 'yellow'
            }
        elif index_value >= 20:
            return {
                'level': '悲观',
                'signal': '偏空，但可能超跌',
                'color': 'blue'
            }
        else:
            return {
                'level': '极度悲观',
                'signal': '恐慌情绪，可能见底',
                'color': 'green'
            }
    
    def calculate_fear_greed_index(self):
        """
        计算恐慌/贪婪指数（类似CNN Fear & Greed Index）
        
        Returns:
            dict: 恐慌/贪婪指数
        """
        # 模拟各指标
        indicators = {
            'price_momentum': 65,      # 股价动量
            'price_strength': 55,      # 股价强度
            'price_breadth': 45,       # 市场广度
            'put_call_ratio': 40,      # 期权 put/call 比（反向）
            'junk_bond_demand': 60,    # 垃圾债需求
            'market_volatility': 30    # 市场波动率（VIX，反向）
        }
        
        # 计算综合指数
        index_value = np.mean(list(indicators.values()))
        
        if index_value >= 75:
            sentiment = '极度贪婪'
        elif index_value >= 55:
            sentiment = '贪婪'
        elif index_value >= 45:
            sentiment = '中性'
        elif index_value >= 25:
            sentiment = '恐惧'
        else:
            sentiment = '极度恐惧'
        
        return {
            'index_value': round(index_value, 2),
            'sentiment': sentiment,
            'indicators': indicators,
            'last_month': round(index_value + np.random.randint(-20, 20), 2),
            'last_year': round(index_value + np.random.randint(-30, 30), 2)
        }
    
    def generate_contrarian_signals(self, sentiment_index):
        """
        生成逆向投资信号
        
        Args:
            sentiment_index: 情绪指数值
            
        Returns:
            dict: 交易信号
        """
        signals = []
        
        # 极度乐观 - 卖出信号
        if sentiment_index >= 80:
            signals.append({
                'type': 'SELL',
                'confidence': 'HIGH',
                'reason': '市场情绪极度乐观，可能过热'
            })
        
        # 极度悲观 - 买入信号
        elif sentiment_index <= 20:
            signals.append({
                'type': 'BUY',
                'confidence': 'HIGH',
                'reason': '市场情绪极度悲观，可能见底'
            })
        
        # 乐观 - 谨慎
        elif sentiment_index >= 60:
            signals.append({
                'type': 'HOLD',
                'confidence': 'MEDIUM',
                'reason': '市场情绪乐观，保持警惕'
            })
        
        # 悲观 - 关注
        elif sentiment_index <= 40:
            signals.append({
                'type': 'WATCH',
                'confidence': 'MEDIUM',
                'reason': '市场情绪悲观，关注机会'
            })
        
        else:
            signals.append({
                'type': 'NEUTRAL',
                'confidence': 'LOW',
                'reason': '市场情绪中性，等待方向'
            })
        
        return signals


def main():
    parser = argparse.ArgumentParser(description='情绪指数构建工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--components', default='news,social,options,analyst',
                       help='情绪组件，逗号分隔')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化
    builder = SentimentIndexBuilder(args.symbol)
    
    # 解析组件
    components = args.components.split(',')
    
    # 构建综合情绪指数
    composite = builder.build_composite_index(components)
    
    # 计算恐慌/贪婪指数
    fear_greed = builder.calculate_fear_greed_index()
    
    # 生成交易信号
    signals = builder.generate_contrarian_signals(composite['index_value'])
    
    # 汇总报告
    report = {
        'symbol': args.symbol,
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'composite_sentiment_index': composite,
        'fear_greed_index': fear_greed,
        'trading_signals': signals
    }
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_sentiment_index.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'情绪指数报告 - {args.symbol}')
    print('=' * 60)
    
    print(f'\n【综合情绪指数】')
    print(f'  指数值: {composite["index_value"]} / 100')
    print(f'  情绪水平: {composite["interpretation"]["level"]}')
    print(f'  投资建议: {composite["interpretation"]["signal"]}')
    
    print(f'\n【指数构成】')
    for comp in composite['components']:
        print(f'  {comp["source"]}: {comp["score"]:.2f} (权重{comp["weight"]:.0%})')
    
    print(f'\n【恐慌/贪婪指数】')
    print(f'  指数值: {fear_greed["index_value"]} / 100')
    print(f'  情绪状态: {fear_greed["sentiment"]}')
    print(f'  上月: {fear_greed["last_month"]}')
    print(f'  上年: {fear_greed["last_year"]}')
    
    print(f'\n【交易信号】')
    for sig in signals:
        print(f'  信号: {sig["type"]} (置信度: {sig["confidence"]})')
        print(f'  理由: {sig["reason"]}')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
