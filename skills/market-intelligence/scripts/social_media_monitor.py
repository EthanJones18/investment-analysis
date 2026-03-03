#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社交媒体监控脚本
监控Twitter/X、Reddit、雪球、股吧等平台的股票讨论情绪

使用方法:
    python social_media_monitor.py --symbol AAPL --platform twitter,reddit --hours 24
"""

import argparse
import json
import os
import re
from datetime import datetime, timedelta
from collections import Counter

import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SocialMediaMonitor:
    """社交媒体监控器"""
    
    def __init__(self, symbol):
        """
        初始化
        
        Args:
            symbol: 股票代码
        """
        self.symbol = symbol
        self.analyzer = SentimentIntensityAnalyzer()
        self.data = {
            'twitter': [],
            'reddit': [],
            'xueqiu': [],  # 雪球
            'guba': []     # 股吧
        }
    
    def fetch_twitter_data(self, hours=24):
        """
        获取Twitter/X数据（模拟）
        
        Args:
            hours: 获取最近几小时的数据
            
        Returns:
            list: Twitter帖子列表
        """
        # 实际应用中应使用Twitter API v2
        # 这里使用模拟数据
        mock_tweets = [
            {
                'id': '1',
                'text': f'${self.symbol} is looking bullish today! 🚀 Great earnings report.',
                'author': 'trader_joe',
                'followers': 15000,
                'created_at': datetime.now() - timedelta(hours=2),
                'likes': 245,
                'retweets': 89,
                'replies': 32
            },
            {
                'id': '2',
                'text': f'Just bought more ${self.symbol}. The fundamentals are strong.',
                'author': 'investor_sarah',
                'followers': 8200,
                'created_at': datetime.now() - timedelta(hours=5),
                'likes': 156,
                'retweets': 45,
                'replies': 18
            },
            {
                'id': '3',
                'text': f'${self.symbol} is overvalued at this price. Taking profits here.',
                'author': 'bearish_bob',
                'followers': 5300,
                'created_at': datetime.now() - timedelta(hours=8),
                'likes': 89,
                'retweets': 34,
                'replies': 56
            },
            {
                'id': '4',
                'text': f'Not sure about ${self.symbol} anymore. Market is too volatile.',
                'author': 'confused_trader',
                'followers': 1200,
                'created_at': datetime.now() - timedelta(hours=12),
                'likes': 45,
                'retweets': 12,
                'replies': 23
            },
            {
                'id': '5',
                'text': f'${self.symbol} to the moon! 🌙💎🙌 Best stock in my portfolio.',
                'author': 'moon_boy',
                'followers': 3400,
                'created_at': datetime.now() - timedelta(hours=18),
                'likes': 567,
                'retweets': 234,
                'replies': 89
            }
        ]
        
        self.data['twitter'] = mock_tweets
        return mock_tweets
    
    def fetch_reddit_data(self, hours=24):
        """
        获取Reddit数据（模拟）
        
        Args:
            hours: 获取最近几小时的数据
            
        Returns:
            list: Reddit帖子列表
        """
        mock_posts = [
            {
                'id': 'r1',
                'title': f'Why {self.symbol} is a buy at current levels',
                'text': 'Been analyzing the financials and the company is undervalued. Strong cash flow, growing market share.',
                'subreddit': 'wallstreetbets',
                'author': 'dd_analyst',
                'created_at': datetime.now() - timedelta(hours=3),
                'upvotes': 1200,
                'comments': 145,
                'awards': 5
            },
            {
                'id': 'r2',
                'title': f'{self.symbol} earnings discussion thread',
                'text': 'What are your thoughts on the latest earnings? Beat expectations but guidance was weak.',
                'subreddit': 'stocks',
                'author': 'earnings_watcher',
                'created_at': datetime.now() - timedelta(hours=6),
                'upvotes': 890,
                'comments': 234,
                'awards': 2
            },
            {
                'id': 'r3',
                'title': f'Selling my {self.symbol} position',
                'text': 'The technicals look terrible. Breaking below support levels. Time to cut losses.',
                'subreddit': 'wallstreetbets',
                'author': 'technical_trader',
                'created_at': datetime.now() - timedelta(hours=10),
                'upvotes': 456,
                'comments': 89,
                'awards': 1
            }
        ]
        
        self.data['reddit'] = mock_posts
        return mock_posts
    
    def fetch_xueqiu_data(self, hours=24):
        """
        获取雪球数据（模拟）
        
        Args:
            hours: 获取最近几小时的数据
            
        Returns:
            list: 雪球帖子列表
        """
        mock_posts = [
            {
                'id': 'x1',
                'title': f'深度分析：{self.symbol}的投资价值',
                'content': '从基本面来看，这家公司估值合理，未来增长空间大。建议长期持有。',
                'author': '价值投资者',
                'followers': 25000,
                'created_at': datetime.now() - timedelta(hours=4),
                'likes': 567,
                'comments': 123,
                'views': 15000
            },
            {
                'id': 'x2',
                'title': f'{self.symbol}短期调整，中期看好',
                'content': '最近股价回调，但基本面没有变化。逢低可以加仓。',
                'author': '趋势跟踪者',
                'followers': 12000,
                'created_at': datetime.now() - timedelta(hours=9),
                'likes': 345,
                'comments': 67,
                'views': 8900
            },
            {
                'id': 'x3',
                'title': f'为什么我不看好{self.symbol}',
                'content': '竞争加剧，市场份额被侵蚀。短期看不到好转迹象。',
                'author': '谨慎投资者',
                'followers': 8000,
                'created_at': datetime.now() - timedelta(hours=15),
                'likes': 234,
                'comments': 156,
                'views': 12000
            }
        ]
        
        self.data['xueqiu'] = mock_posts
        return mock_posts
    
    def fetch_guba_data(self, hours=24):
        """
        获取股吧数据（模拟）
        
        Args:
            hours: 获取最近几小时的数据
            
        Returns:
            list: 股吧帖子列表
        """
        mock_posts = [
            {
                'id': 'g1',
                'title': f'{self.symbol}明天必涨！',
                'content': '今天洗盘结束，主力已经吸筹完毕。明天高开高走！',
                'author': '股神888',
                'created_at': datetime.now() - timedelta(hours=1),
                'replies': 89,
                'views': 5600
            },
            {
                'id': 'g2',
                'title': f'{self.symbol}被套了，怎么办？',
                'content': '高位追进去的，现在亏损20%。要不要割肉？',
                'author': '小散户',
                'created_at': datetime.now() - timedelta(hours=7),
                'replies': 234,
                'views': 12000
            },
            {
                'id': 'g3',
                'title': f'理性分析{self.symbol}',
                'content': '从财报看业绩稳定，但估值偏高。建议观望为主。',
                'author': '老股民',
                'created_at': datetime.now() - timedelta(hours=14),
                'replies': 45,
                'views': 3400
            }
        ]
        
        self.data['guba'] = mock_posts
        return mock_posts
    
    def analyze_sentiment(self, text):
        """
        分析文本情绪
        
        Args:
            text: 文本内容
            
        Returns:
            dict: 情绪分析结果
        """
        scores = self.analyzer.polarity_scores(text)
        
        # 判断情绪
        if scores['compound'] >= 0.5:
            sentiment = '极度乐观'
        elif scores['compound'] >= 0.2:
            sentiment = '乐观'
        elif scores['compound'] >= -0.2:
            sentiment = '中性'
        elif scores['compound'] >= -0.5:
            sentiment = '悲观'
        else:
            sentiment = '极度悲观'
        
        return {
            'compound': round(scores['compound'], 4),
            'positive': round(scores['pos'], 4),
            'neutral': round(scores['neu'], 4),
            'negative': round(scores['neg'], 4),
            'sentiment': sentiment
        }
    
    def analyze_all_platforms(self):
        """分析所有平台数据"""
        results = {}
        
        for platform, posts in self.data.items():
            if not posts:
                continue
            
            platform_results = []
            sentiments = []
            
            for post in posts:
                # 合并标题和内容
                text = post.get('title', '') + ' ' + post.get('text', post.get('content', ''))
                
                # 情绪分析
                sentiment = self.analyze_sentiment(text)
                sentiments.append(sentiment['compound'])
                
                # 计算影响力分数
                influence = self._calculate_influence(post, platform)
                
                platform_results.append({
                    'id': post['id'],
                    'text': text[:100] + '...' if len(text) > 100 else text,
                    'author': post['author'],
                    'sentiment': sentiment,
                    'influence': influence,
                    'created_at': post['created_at'].strftime('%Y-%m-%d %H:%M')
                })
            
            # 平台统计
            results[platform] = {
                'posts': platform_results,
                'stats': {
                    'count': len(posts),
                    'avg_sentiment': round(np.mean(sentiments), 4),
                    'positive_ratio': round(sum([1 for s in sentiments if s > 0]) / len(sentiments), 4),
                    'negative_ratio': round(sum([1 for s in sentiments if s < 0]) / len(sentiments), 4),
                    'neutral_ratio': round(sum([1 for s in sentiments if s == 0]) / len(sentiments), 4)
                }
            }
        
        return results
    
    def _calculate_influence(self, post, platform):
        """计算帖子影响力"""
        if platform == 'twitter':
            return post.get('followers', 0) * 0.1 + post.get('likes', 0) * 0.5 + post.get('retweets', 0) * 2
        elif platform == 'reddit':
            return post.get('upvotes', 0) * 0.5 + post.get('comments', 0) * 2 + post.get('awards', 0) * 10
        elif platform == 'xueqiu':
            return post.get('followers', 0) * 0.1 + post.get('likes', 0) * 0.5 + post.get('comments', 0) * 2
        elif platform == 'guba':
            return post.get('replies', 0) * 2 + post.get('views', 0) * 0.01
        return 0
    
    def extract_keywords(self, platform_data):
        """提取关键词"""
        all_text = ' '.join([post['text'] for post in platform_data])
        
        # 简单关键词提取（实际应用可使用TF-IDF或NER）
        words = re.findall(r'\b[A-Za-z]{4,}\b', all_text.lower())
        word_counts = Counter(words)
        
        # 过滤常见停用词
        stop_words = {'this', 'that', 'with', 'from', 'they', 'have', 'been', 'their', 'than', 'when', 'what', 'will', 'would', 'could', 'should'}
        filtered = {k: v for k, v in word_counts.items() if k not in stop_words}
        
        return dict(sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def detect_sentiment_shifts(self, platform_results):
        """检测情绪变化"""
        shifts = []
        
        for platform, data in platform_results.items():
            posts = data['posts']
            if len(posts) < 2:
                continue
            
            # 按时间排序
            sorted_posts = sorted(posts, key=lambda x: x['created_at'])
            
            # 计算情绪变化
            early_sentiment = np.mean([p['sentiment']['compound'] for p in sorted_posts[:len(sorted_posts)//2]])
            late_sentiment = np.mean([p['sentiment']['compound'] for p in sorted_posts[len(sorted_posts)//2:]])
            
            shift = late_sentiment - early_sentiment
            
            if abs(shift) > 0.3:
                shifts.append({
                    'platform': platform,
                    'shift': round(shift, 4),
                    'direction': '转向乐观' if shift > 0 else '转向悲观',
                    'early_avg': round(early_sentiment, 4),
                    'late_avg': round(late_sentiment, 4)
                })
        
        return shifts
    
    def generate_report(self, platforms):
        """生成监控报告"""
        # 获取数据
        if 'twitter' in platforms:
            self.fetch_twitter_data()
        if 'reddit' in platforms:
            self.fetch_reddit_data()
        if 'xueqiu' in platforms:
            self.fetch_xueqiu_data()
        if 'guba' in platforms:
            self.fetch_guba_data()
        
        # 分析所有平台
        platform_results = self.analyze_all_platforms()
        
        # 计算综合情绪
        all_sentiments = []
        total_posts = 0
        
        for platform, data in platform_results.items():
            all_sentiments.append(data['stats']['avg_sentiment'])
            total_posts += data['stats']['count']
        
        composite_sentiment = np.mean(all_sentiments) if all_sentiments else 0
        
        # 检测情绪变化
        sentiment_shifts = self.detect_sentiment_shifts(platform_results)
        
        # 提取关键词
        keywords = {}
        for platform, data in platform_results.items():
            keywords[platform] = self.extract_keywords(data['posts'])
        
        return {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_posts': total_posts,
            'composite_sentiment': round(composite_sentiment, 4),
            'sentiment_label': self._get_sentiment_label(composite_sentiment),
            'platform_results': platform_results,
            'sentiment_shifts': sentiment_shifts,
            'keywords': keywords
        }
    
    def _get_sentiment_label(self, sentiment):
        """获取情绪标签"""
        if sentiment >= 0.5:
            return '极度乐观'
        elif sentiment >= 0.2:
            return '乐观'
        elif sentiment >= -0.2:
            return '中性'
        elif sentiment >= -0.5:
            return '悲观'
        else:
            return '极度悲观'


def main():
    parser = argparse.ArgumentParser(description='社交媒体监控工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--platform', default='twitter,reddit,xueqiu,guba',
                       help='监控平台，逗号分隔')
    parser.add_argument('--hours', type=int, default=24, help='监控时长（小时）')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化监控器
    monitor = SocialMediaMonitor(args.symbol)
    
    # 解析平台
    platforms = args.platform.split(',')
    
    # 生成报告
    report = monitor.generate_report(platforms)
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_social_media.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'社交媒体监控报告 - {args.symbol}')
    print('=' * 60)
    
    print(f'\n【综合情绪】')
    print(f'  情绪分数: {report["composite_sentiment"]}')
    print(f'  情绪标签: {report["sentiment_label"]}')
    print(f'  总帖子数: {report["total_posts"]}')
    
    print(f'\n【分平台统计】')
    for platform, data in report['platform_results'].items():
        stats = data['stats']
        print(f'  {platform.upper()}:')
        print(f'    帖子数: {stats["count"]}')
        print(f'    平均情绪: {stats["avg_sentiment"]}')
        print(f'    正面比例: {stats["positive_ratio"]:.1%}')
        print(f'    负面比例: {stats["negative_ratio"]:.1%}')
    
    if report['sentiment_shifts']:
        print(f'\n【情绪变化检测】')
        for shift in report['sentiment_shifts']:
            print(f'  {shift["platform"]}: {shift["direction"]} (变化: {shift["shift"]:.2f})')
    
    print(f'\n【热门关键词】')
    for platform, words in report['keywords'].items():
        print(f'  {platform.upper()}: {", ".join(list(words.keys())[:5])}')
    
    print(f'\n【热门帖子】')
    for platform, data in report['platform_results'].items():
        if data['posts']:
            top_post = max(data['posts'], key=lambda x: x['influence'])
            print(f'  {platform.upper()}: {top_post["text"][:60]}...')
            print(f'    情绪: {top_post["sentiment"]["sentiment"]} ({top_post["sentiment"]["compound"]})')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
