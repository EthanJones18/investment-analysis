#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻情绪分析脚本
采集财经新闻并进行情绪打分

使用方法:
    python news_sentiment.py --symbol AAPL --sources bloomberg,reuters --days 7
"""

import argparse
import json
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
from textblob import TextBlob


class NewsSentimentAnalyzer:
    """新闻情绪分析器"""
    
    def __init__(self, symbol):
        """
        初始化
        
        Args:
            symbol: 股票代码
        """
        self.symbol = symbol
        self.news_data = []
    
    def fetch_news(self, sources, days=7):
        """
        获取新闻数据（模拟）
        
        Args:
            sources: 新闻源列表
            days: 获取天数
            
        Returns:
            list: 新闻列表
        """
        # 实际应用中应调用新闻API
        # 这里使用模拟数据
        mock_news = [
            {
                'title': f'{self.symbol} announces strong quarterly earnings',
                'content': 'The company beat expectations with revenue growth of 15%',
                'source': 'Bloomberg',
                'date': datetime.now() - timedelta(days=1),
                'url': 'https://example.com/1'
            },
            {
                'title': f'Analysts upgrade {self.symbol} price target',
                'content': 'Multiple analysts raised their price targets citing strong fundamentals',
                'source': 'Reuters',
                'date': datetime.now() - timedelta(days=2),
                'url': 'https://example.com/2'
            },
            {
                'title': f'{self.symbol} faces regulatory scrutiny',
                'content': 'Regulators are investigating potential antitrust issues',
                'source': 'WSJ',
                'date': datetime.now() - timedelta(days=3),
                'url': 'https://example.com/3'
            },
            {
                'title': f'{self.symbol} launches new product line',
                'content': 'The new products are expected to drive significant revenue growth',
                'source': 'TechCrunch',
                'date': datetime.now() - timedelta(days=4),
                'url': 'https://example.com/4'
            },
            {
                'title': f'Market volatility affects {self.symbol}',
                'content': 'Broader market selloff impacts stock performance',
                'source': 'CNBC',
                'date': datetime.now() - timedelta(days=5),
                'url': 'https://example.com/5'
            }
        ]
        
        self.news_data = mock_news
        return mock_news
    
    def analyze_sentiment(self, text):
        """
        分析文本情绪
        
        Args:
            text: 文本内容
            
        Returns:
            dict: 情绪分数
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # 情绪分类
        if polarity > 0.5:
            sentiment = '极度乐观'
        elif polarity > 0.2:
            sentiment = '乐观'
        elif polarity > -0.2:
            sentiment = '中性'
        elif polarity > -0.5:
            sentiment = '悲观'
        else:
            sentiment = '极度悲观'
        
        return {
            'polarity': round(polarity, 4),
            'subjectivity': round(subjectivity, 4),
            'sentiment': sentiment
        }
    
    def analyze_all_news(self):
        """分析所有新闻"""
        results = []
        
        for news in self.news_data:
            title_sentiment = self.analyze_sentiment(news['title'])
            content_sentiment = self.analyze_sentiment(news['content'])
            
            # 综合情绪（标题权重40%，内容权重60%）
            combined_polarity = title_sentiment['polarity'] * 0.4 + content_sentiment['polarity'] * 0.6
            
            results.append({
                'title': news['title'],
                'source': news['source'],
                'date': news['date'].strftime('%Y-%m-%d'),
                'title_sentiment': title_sentiment,
                'content_sentiment': content_sentiment,
                'combined_polarity': round(combined_polarity, 4),
                'combined_sentiment': self._classify_sentiment(combined_polarity)
            })
        
        return results
    
    def _classify_sentiment(self, polarity):
        """情绪分类"""
        if polarity > 0.5:
            return '极度乐观'
        elif polarity > 0.2:
            return '乐观'
        elif polarity > -0.2:
            return '中性'
        elif polarity > -0.5:
            return '悲观'
        else:
            return '极度悲观'
    
    def calculate_aggregate_sentiment(self, results):
        """计算综合情绪指标"""
        polarities = [r['combined_polarity'] for r in results]
        
        return {
            'average_sentiment': round(np.mean(polarities), 4),
            'sentiment_std': round(np.std(polarities), 4),
            'positive_ratio': round(sum([1 for p in polarities if p > 0]) / len(polarities), 4),
            'negative_ratio': round(sum([1 for p in polarities if p < 0]) / len(polarities), 4),
            'neutral_ratio': round(sum([1 for p in polarities if p == 0]) / len(polarities), 4),
            'overall_sentiment': self._classify_sentiment(np.mean(polarities))
        }
    
    def identify_key_events(self, results):
        """识别关键事件"""
        # 识别情绪极值事件
        key_events = []
        
        for r in results:
            if abs(r['combined_polarity']) > 0.5:
                key_events.append({
                    'date': r['date'],
                    'title': r['title'],
                    'sentiment': r['combined_sentiment'],
                    'polarity': r['combined_polarity']
                })
        
        return sorted(key_events, key=lambda x: abs(x['polarity']), reverse=True)
    
    def generate_report(self):
        """生成分析报告"""
        results = self.analyze_all_news()
        aggregate = self.calculate_aggregate_sentiment(results)
        key_events = self.identify_key_events(results)
        
        return {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'news_count': len(results),
            'aggregate_sentiment': aggregate,
            'key_events': key_events[:5],
            'detailed_results': results
        }


def main():
    parser = argparse.ArgumentParser(description='新闻情绪分析工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--sources', default='bloomberg,reuters', help='新闻源，逗号分隔')
    parser.add_argument('--days', type=int, default=7, help='获取天数')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = NewsSentimentAnalyzer(args.symbol)
    
    # 获取新闻
    sources = args.sources.split(',')
    analyzer.fetch_news(sources, args.days)
    
    # 生成报告
    report = analyzer.generate_report()
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_news_sentiment.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'新闻情绪分析报告 - {args.symbol}')
    print('=' * 60)
    
    agg = report['aggregate_sentiment']
    print(f'\n【综合情绪】')
    print(f'  平均情绪分数: {agg["average_sentiment"]}')
    print(f'  整体情绪: {agg["overall_sentiment"]}')
    print(f'  情绪标准差: {agg["sentiment_std"]}')
    print(f'  正面新闻占比: {agg["positive_ratio"]:.1%}')
    print(f'  负面新闻占比: {agg["negative_ratio"]:.1%}')
    print(f'  中性新闻占比: {agg["neutral_ratio"]:.1%}')
    
    print(f'\n【关键事件】')
    for i, event in enumerate(report['key_events'], 1):
        print(f'  {i}. [{event["date"]}] {event["title"]}')
        print(f'     情绪: {event["sentiment"]} ({event["polarity"]})')
    
    print(f'\n【新闻详情】')
    for news in report['detailed_results']:
        print(f'  [{news["date"]}] {news["source"]}')
        print(f'    标题: {news["title"][:50]}...')
        print(f'    情绪: {news["combined_sentiment"]} ({news["combined_polarity"]})')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
