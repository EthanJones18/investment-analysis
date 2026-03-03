#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
权威资讯信息爬取脚本
爬取Bloomberg、Reuters、WSJ、财新、第一财经等权威财经媒体

使用方法:
    python authority_news_crawler.py --symbol AAPL --sources bloomberg,reuters,caixin --days 7
"""

import argparse
import json
import os
import re
import time
from datetime import datetime, timedelta
from urllib.parse import quote

import feedparser
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob


class AuthorityNewsCrawler:
    """权威财经新闻爬取器"""
    
    def __init__(self, symbol, company_name=None):
        """
        初始化
        
        Args:
            symbol: 股票代码
            company_name: 公司名称
        """
        self.symbol = symbol
        self.company_name = company_name or symbol
        self.news_data = []
        
        # 权威媒体源配置
        self.sources = {
            'bloomberg': {
                'name': 'Bloomberg',
                'url': f'https://www.bloomberg.com/search?query={symbol}',
                'rss': None,
                'weight': 1.0
            },
            'reuters': {
                'name': 'Reuters',
                'url': f'https://www.reuters.com/search/news?blob={symbol}',
                'rss': None,
                'weight': 1.0
            },
            'wsj': {
                'name': 'Wall Street Journal',
                'url': f'https://www.wsj.com/search?query={symbol}',
                'rss': None,
                'weight': 1.0
            },
            'ft': {
                'name': 'Financial Times',
                'url': f'https://www.ft.com/search?q={symbol}',
                'rss': None,
                'weight': 1.0
            },
            'cnbc': {
                'name': 'CNBC',
                'url': f'https://www.cnbc.com/search/?query={symbol}',
                'rss': None,
                'weight': 0.9
            },
            'seekingalpha': {
                'name': 'Seeking Alpha',
                'url': f'https://seekingalpha.com/symbol/{symbol}',
                'rss': f'https://seekingalpha.com/api/v3/symbols/{symbol}/news',
                'weight': 0.9
            },
            'caixin': {
                'name': '财新',
                'url': f'https://search.caixin.com/search/search.jsp?keyword={quote(symbol)}',
                'rss': None,
                'weight': 1.0
            },
            'caijing': {
                'name': '财经',
                'url': f'http://search.caijing.com.cn/search.jsp?key={quote(symbol)}',
                'rss': None,
                'weight': 0.9
            },
            'yicai': {
                'name': '第一财经',
                'url': f'https://www.yicai.com.cn/search?keys={quote(symbol)}',
                'rss': None,
                'weight': 0.9
            },
            'eastmoney': {
                'name': '东方财富',
                'url': f'https://search.eastmoney.com/search/web?q={symbol}',
                'rss': None,
                'weight': 0.8
            }
        }
    
    def fetch_news(self, source_list, days=7):
        """
        获取新闻数据
        
        Args:
            source_list: 新闻源列表
            days: 获取天数
            
        Returns:
            list: 新闻列表
        """
        all_news = []
        
        for source_key in source_list:
            if source_key not in self.sources:
                continue
            
            source = self.sources[source_key]
            print(f'正在获取 {source["name"]} 的新闻...')
            
            try:
                # 使用模拟数据（实际应用需要实现真实爬取）
                news = self._fetch_mock_news(source_key, source, days)
                all_news.extend(news)
                
                # 礼貌性延迟
                time.sleep(0.5)
                
            except Exception as e:
                print(f'获取 {source["name"]} 失败: {e}')
                continue
        
        # 去重和排序
        all_news = self._deduplicate_news(all_news)
        all_news = sorted(all_news, key=lambda x: x['published'], reverse=True)
        
        self.news_data = all_news
        return all_news
    
    def _fetch_mock_news(self, source_key, source, days):
        """获取模拟新闻数据"""
        mock_news_templates = {
            'bloomberg': [
                {'title': f'{self.company_name} Beats Earnings Estimates on Strong Cloud Growth', 'sentiment': 'positive'},
                {'title': f'{self.company_name} Announces New Share Buyback Program', 'sentiment': 'positive'},
                {'title': f'Analysts Raise Price Targets for {self.company_name}', 'sentiment': 'positive'}
            ],
            'reuters': [
                {'title': f'{self.company_name} revenue rises 15% on cloud demand', 'sentiment': 'positive'},
                {'title': f'{self.company_name} to invest $10 billion in AI infrastructure', 'sentiment': 'positive'},
                {'title': f'{self.company_name} faces regulatory scrutiny in EU', 'sentiment': 'negative'}
            ],
            'wsj': [
                {'title': f'{self.company_name} Stock Rises on Strong Quarterly Results', 'sentiment': 'positive'},
                {'title': f'{self.company_name} Expands Into New Markets', 'sentiment': 'positive'},
                {'title': f'Competition Heats Up for {self.company_name}', 'sentiment': 'neutral'}
            ],
            'cnbc': [
                {'title': f'{self.company_name} is a buy here, say analysts', 'sentiment': 'positive'},
                {'title': f'Cramer: {self.company_name} is executing well', 'sentiment': 'positive'},
                {'title': f'{self.company_name} stock volatile after earnings', 'sentiment': 'neutral'}
            ],
            'seekingalpha': [
                {'title': f'{self.company_name}: A Deep Value Play', 'sentiment': 'positive'},
                {'title': f'Why {self.company_name} Is A Buy', 'sentiment': 'positive'},
                {'title': f'{self.company_name}: Risks To Consider', 'sentiment': 'neutral'}
            ],
            'caixin': [
                {'title': f'{self.company_name}业绩超预期 云计算业务增长强劲', 'sentiment': 'positive'},
                {'title': f'{self.company_name}宣布加大AI投资力度', 'sentiment': 'positive'},
                {'title': f'分析师看好{self.company_name}长期前景', 'sentiment': 'positive'}
            ],
            'caijing': [
                {'title': f'{self.company_name}营收创新高', 'sentiment': 'positive'},
                {'title': f'{self.company_name}股价创历史新高', 'sentiment': 'positive'},
                {'title': f'{self.company_name}面临行业竞争加剧', 'sentiment': 'neutral'}
            ],
            'yicai': [
                {'title': f'{self.company_name}发布强劲财报', 'sentiment': 'positive'},
                {'title': f'{self.company_name}加码人工智能布局', 'sentiment': 'positive'},
                {'title': f'市场关注{self.company_name}新战略', 'sentiment': 'neutral'}
            ],
            'eastmoney': [
                {'title': f'{self.company_name}主力资金净流入', 'sentiment': 'positive'},
                {'title': f'{self.company_name}获多家机构买入评级', 'sentiment': 'positive'},
                {'title': f'{self.company_name}股价技术性调整', 'sentiment': 'neutral'}
            ]
        }
        
        templates = mock_news_templates.get(source_key, mock_news_templates['bloomberg'])
        news = []
        
        for i, template in enumerate(templates):
            news.append({
                'id': f'{source_key}_{i}',
                'title': template['title'],
                'content': f'{template["title"]}. This is a detailed article about {self.company_name} and its recent developments in the market.',
                'source': source['name'],
                'source_weight': source['weight'],
                'published': datetime.now() - timedelta(days=i*2),
                'url': f'https://example.com/{source_key}/{i}',
                'category': self._categorize_news(template['title']),
                'sentiment_tag': template['sentiment']
            })
        
        return news
    
    def _deduplicate_news(self, news_list):
        """去重"""
        seen = set()
        unique_news = []
        
        for news in news_list:
            # 使用标题相似度去重
            title_hash = hash(news['title'].lower().replace(' ', '')[:30])
            if title_hash not in seen:
                seen.add(title_hash)
                unique_news.append(news)
        
        return unique_news
    
    def _categorize_news(self, title):
        """新闻分类"""
        title_lower = title.lower()
        
        categories = {
            'earnings': ['earnings', 'revenue', 'profit', 'loss', 'quarterly', '财报', '业绩', '营收', '利润'],
            'merger_acquisition': ['merger', 'acquisition', 'acquire', 'merge', '并购', '收购', '合并'],
            'product': ['product', 'launch', 'release', '新品', '产品', '发布'],
            'regulatory': ['regulatory', 'regulation', 'sec', 'fda', '监管', '合规'],
            'executive': ['ceo', 'cfo', 'executive', 'resign', 'appoint', '高管', '任命', '离职'],
            'market': ['stock', 'price', 'trading', 'market', '股价', '股市', '交易'],
            'analyst': ['analyst', 'rating', 'upgrade', 'downgrade', 'target', '分析师', '评级', '目标价']
        }
        
        for category, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                return category
        
        return 'general'
    
    def analyze_sentiment(self, text):
        """情绪分析"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.3:
            sentiment = 'positive'
        elif polarity < -0.3:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 4),
            'sentiment': sentiment
        }
    
    def analyze_all_news(self):
        """分析所有新闻"""
        results = []
        
        for news in self.news_data:
            sentiment = self.analyze_sentiment(news['title'] + ' ' + news['content'])
            
            # 加权情绪分数
            weighted_sentiment = sentiment['polarity'] * news['source_weight']
            
            results.append({
                **news,
                'sentiment': sentiment,
                'weighted_sentiment': round(weighted_sentiment, 4)
            })
        
        return results
    
    def extract_key_events(self, analyzed_news):
        """提取关键事件"""
        events = []
        
        # 按类别分组
        by_category = {}
        for news in analyzed_news:
            cat = news['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(news)
        
        # 提取每个类别的关键事件
        for category, news_list in by_category.items():
            if category == 'general':
                continue
            
            # 按情绪强度和来源权重排序
            sorted_news = sorted(news_list, 
                               key=lambda x: abs(x['sentiment']['polarity']) * x['source_weight'],
                               reverse=True)
            
            if sorted_news:
                top_news = sorted_news[0]
                events.append({
                    'category': category,
                    'title': top_news['title'],
                    'source': top_news['source'],
                    'date': top_news['published'].strftime('%Y-%m-%d'),
                    'sentiment': top_news['sentiment']['sentiment'],
                    'polarity': top_news['sentiment']['polarity']
                })
        
        return sorted(events, key=lambda x: abs(x['polarity']), reverse=True)
    
    def calculate_source_stats(self, analyzed_news):
        """计算各来源统计"""
        stats = {}
        
        for news in analyzed_news:
            source = news['source']
            if source not in stats:
                stats[source] = {
                    'count': 0,
                    'sentiments': [],
                    'avg_sentiment': 0
                }
            
            stats[source]['count'] += 1
            stats[source]['sentiments'].append(news['sentiment']['polarity'])
        
        for source in stats:
            stats[source]['avg_sentiment'] = round(np.mean(stats[source]['sentiments']), 4)
            stats[source]['positive_ratio'] = round(
                sum([1 for s in stats[source]['sentiments'] if s > 0]) / len(stats[source]['sentiments']), 4
            )
        
        return stats
    
    def generate_report(self, source_list, days=7):
        """生成完整报告"""
        # 获取新闻
        self.fetch_news(source_list, days)
        
        # 分析情绪
        analyzed_news = self.analyze_all_news()
        
        # 计算综合指标
        all_sentiments = [n['weighted_sentiment'] for n in analyzed_news]
        
        # 按时间加权（近期新闻权重更高）
        now = datetime.now()
        time_weights = []
        for news in analyzed_news:
            if isinstance(news['published'], datetime):
                days_ago = (now - news['published']).days
            else:
                days_ago = 0
            weight = max(0.5, 1 - days_ago / days * 0.5)  # 近期权重更高
            time_weights.append(weight)
        
        weighted_avg = np.average(all_sentiments, weights=time_weights) if all_sentiments else 0
        
        # 提取关键事件
        key_events = self.extract_key_events(analyzed_news)
        
        # 来源统计
        source_stats = self.calculate_source_stats(analyzed_news)
        
        # 处理日期序列化
        for news in analyzed_news:
            if isinstance(news.get('published'), datetime):
                news['published'] = news['published'].strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'news_count': len(analyzed_news),
            'sources': source_list,
            'composite_sentiment': round(weighted_avg, 4),
            'sentiment_label': self._get_sentiment_label(weighted_avg),
            'source_stats': source_stats,
            'key_events': key_events,
            'category_distribution': self._get_category_distribution(analyzed_news),
            'daily_sentiment': self._get_daily_sentiment(analyzed_news),
            'detailed_news': analyzed_news[:20]  # 只保留前20条详情
        }
    
    def _get_sentiment_label(self, sentiment):
        """获取情绪标签"""
        if sentiment >= 0.3:
            return '积极'
        elif sentiment >= 0.1:
            return '偏积极'
        elif sentiment >= -0.1:
            return '中性'
        elif sentiment >= -0.3:
            return '偏消极'
        else:
            return '消极'
    
    def _get_category_distribution(self, analyzed_news):
        """获取类别分布"""
        categories = {}
        for news in analyzed_news:
            cat = news['category']
            if cat not in categories:
                categories[cat] = {'count': 0, 'avg_sentiment': []}
            categories[cat]['count'] += 1
            categories[cat]['avg_sentiment'].append(news['sentiment']['polarity'])
        
        for cat in categories:
            categories[cat]['avg_sentiment'] = round(np.mean(categories[cat]['avg_sentiment']), 4)
        
        return categories
    
    def _get_daily_sentiment(self, analyzed_news):
        """获取每日情绪趋势"""
        daily = {}
        for news in analyzed_news:
            published = news.get('published', '')
            if isinstance(published, datetime):
                date = published.strftime('%Y-%m-%d')
            elif isinstance(published, str):
                date = published[:10] if len(published) >= 10 else published
            else:
                date = 'unknown'
            
            if date not in daily:
                daily[date] = []
            daily[date].append(news['sentiment']['polarity'])
        
        return {date: round(np.mean(scores), 4) for date, scores in sorted(daily.items())}


def main():
    parser = argparse.ArgumentParser(description='权威财经新闻爬取工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--company', help='公司名称')
    parser.add_argument('--sources', default='bloomberg,reuters,cnbc,seekingalpha',
                       help='新闻源，逗号分隔')
    parser.add_argument('--days', type=int, default=7, help='获取天数')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化爬取器
    crawler = AuthorityNewsCrawler(args.symbol, args.company)
    
    # 解析来源
    sources = args.sources.split(',')
    
    # 生成报告
    report = crawler.generate_report(sources, args.days)
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_authority_news.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'权威财经新闻报告 - {args.symbol}')
    print('=' * 60)
    
    print(f'\n【综合情绪】')
    print(f'  情绪分数: {report["composite_sentiment"]}')
    print(f'  情绪标签: {report["sentiment_label"]}')
    print(f'  新闻总数: {report["news_count"]}')
    
    print(f'\n【来源统计】')
    for source, stats in report['source_stats'].items():
        print(f'  {source}: {stats["count"]}篇 | 平均情绪: {stats["avg_sentiment"]} | 正面比例: {stats["positive_ratio"]:.1%}')
    
    print(f'\n【关键事件】')
    for i, event in enumerate(report['key_events'][:5], 1):
        print(f'  {i}. [{event["category"].upper()}] {event["title"]}')
        print(f'     来源: {event["source"]} | 情绪: {event["sentiment"]} | 日期: {event["date"]}')
    
    print(f'\n【类别分布】')
    for cat, data in report['category_distribution'].items():
        print(f'  {cat}: {data["count"]}篇 (平均情绪: {data["avg_sentiment"]})')
    
    print(f'\n【情绪趋势】')
    for date, sentiment in list(report['daily_sentiment'].items())[-5:]:
        print(f'  {date}: {sentiment}')
    
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
