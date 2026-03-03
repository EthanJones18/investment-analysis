#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
市场信息深度解读分析脚本
对重点资讯和情绪进行详细解读分析

使用方法:
    python market_intelligence_analysis.py --symbol AAPL --report-type comprehensive
"""

import argparse
import json
import os
from datetime import datetime
from collections import Counter

import numpy as np


class MarketIntelligenceAnalyzer:
    """市场信息深度解读分析器"""
    
    def __init__(self, symbol, data_file=None):
        """
        初始化
        
        Args:
            symbol: 股票代码
            data_file: 已有数据文件路径
        """
        self.symbol = symbol
        self.data = self._load_data(data_file) if data_file else {}
    
    def _load_data(self, data_file):
        """加载已有数据"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def analyze_key_news(self, news_data):
        """
        重点资讯深度解读
        
        Args:
            news_data: 新闻数据
            
        Returns:
            dict: 重点资讯分析
        """
        if not news_data or 'detailed_news' not in news_data:
            return {}
        
        news_list = news_data['detailed_news']
        
        # 按来源权重和情绪强度排序
        weighted_news = []
        for news in news_list:
            impact_score = abs(news.get('weighted_sentiment', 0)) * news.get('source_weight', 1)
            weighted_news.append({
                **news,
                'impact_score': impact_score
            })
        
        weighted_news.sort(key=lambda x: x['impact_score'], reverse=True)
        
        # 提取重点资讯（前5条）
        key_news = []
        for news in weighted_news[:5]:
            key_news.append({
                'title': news['title'],
                'source': news['source'],
                'date': news.get('published', 'N/A'),
                'category': news.get('category', 'general'),
                'sentiment': news['sentiment']['sentiment'],
                'polarity': news['sentiment']['polarity'],
                'impact_score': round(news['impact_score'], 4),
                'interpretation': self._interpret_single_news(news)
            })
        
        # 按类别分组分析
        category_analysis = self._analyze_by_category(news_list)
        
        return {
            'key_news': key_news,
            'category_analysis': category_analysis,
            'narrative_analysis': self._analyze_market_narrative(news_list)
        }
    
    def _interpret_single_news(self, news):
        """单条新闻解读"""
        sentiment = news['sentiment']['sentiment']
        polarity = news['sentiment']['polarity']
        category = news.get('category', 'general')
        
        interpretations = {
            'positive': {
                'earnings': '业绩超预期，市场信心增强，可能推动股价上涨',
                'product': '新产品/服务发布，增长前景改善',
                'analyst': '分析师看好，目标价上调，机构关注度提升',
                'merger_acquisition': '并购消息利好，协同效应预期',
                'regulatory': '监管利好，政策风险降低',
                'general': '利好消息，市场情绪正面'
            },
            'negative': {
                'earnings': '业绩不及预期，可能引发股价调整',
                'product': '产品问题或竞争加剧，增长担忧',
                'analyst': '分析师下调评级，目标价下调',
                'regulatory': '监管压力增加，合规风险上升',
                'executive': '高管变动，管理层稳定性担忧',
                'general': '利空消息，市场情绪负面'
            },
            'neutral': {
                'earnings': '业绩符合预期，市场反应平淡',
                'market': '市场正常波动，无特殊影响',
                'general': '中性消息，影响有限'
            }
        }
        
        return interpretations.get(sentiment, {}).get(category, '影响待观察')
    
    def _analyze_by_category(self, news_list):
        """按类别分析"""
        categories = {}
        
        for news in news_list:
            cat = news.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(news)
        
        category_analysis = {}
        for cat, news_items in categories.items():
            sentiments = [n['sentiment']['polarity'] for n in news_items]
            avg_sentiment = np.mean(sentiments)
            
            category_names = {
                'earnings': '财报业绩',
                'merger_acquisition': '并购重组',
                'product': '产品动态',
                'regulatory': '监管政策',
                'executive': '高管变动',
                'market': '市场表现',
                'analyst': '分析师观点',
                'general': '一般资讯'
            }
            
            category_analysis[cat] = {
                'name': category_names.get(cat, cat),
                'count': len(news_items),
                'avg_sentiment': round(avg_sentiment, 4),
                'sentiment_label': self._get_sentiment_label(avg_sentiment),
                'key_points': self._extract_category_insights(cat, news_items),
                'impact_assessment': self._assess_category_impact(cat, avg_sentiment)
            }
        
        return category_analysis
    
    def _extract_category_insights(self, category, news_items):
        """提取类别洞察"""
        insights = []
        
        if category == 'earnings':
            positive = sum([1 for n in news_items if n['sentiment']['polarity'] > 0])
            negative = sum([1 for n in news_items if n['sentiment']['polarity'] < 0])
            
            if positive > negative:
                insights.append('多数财报消息正面，业绩表现良好')
            elif negative > positive:
                insights.append('财报消息偏负面，业绩承压')
            else:
                insights.append('财报消息多空交织，业绩分化')
        
        elif category == 'analyst':
            upgrades = sum([1 for n in news_items if 'upgrade' in n['title'].lower()])
            downgrades = sum([1 for n in news_items if 'downgrade' in n['title'].lower()])
            
            if upgrades > downgrades:
                insights.append(f'分析师以看好为主，{upgrades}家上调评级')
            elif downgrades > upgrades:
                insights.append(f'分析师态度谨慎，{downgrades}家下调评级')
        
        elif category == 'regulatory':
            sentiments = [n['sentiment']['polarity'] for n in news_items]
            if np.mean(sentiments) > 0:
                insights.append('监管环境改善，政策风险下降')
            else:
                insights.append('监管压力持续，需关注政策变化')
        
        return insights
    
    def _assess_category_impact(self, category, avg_sentiment):
        """评估类别影响"""
        impact_levels = {
            'earnings': '高',
            'merger_acquisition': '高',
            'regulatory': '高',
            'product': '中',
            'analyst': '中',
            'executive': '中',
            'market': '低',
            'general': '低'
        }
        
        level = impact_levels.get(category, '中')
        direction = '正面' if avg_sentiment > 0.2 else ('负面' if avg_sentiment < -0.2 else '中性')
        
        return f'{level}影响 - {direction}'
    
    def _analyze_market_narrative(self, news_list):
        """分析市场叙事/主线"""
        # 提取关键词
        all_titles = ' '.join([n['title'] for n in news_list])
        
        # 定义关键主题
        themes = {
            'growth': ['growth', 'expansion', 'revenue', '增长', '营收'],
            'profitability': ['profit', 'margin', 'earnings', '利润', '盈利'],
            'innovation': ['innovation', 'ai', 'technology', '创新', '技术'],
            'competition': ['competition', 'competitor', 'market share', '竞争', '市场份额'],
            'regulation': ['regulation', 'policy', '监管', '政策'],
            'macro': ['economy', 'recession', 'inflation', '经济', '通胀']
        }
        
        theme_scores = {}
        for theme, keywords in themes.items():
            score = sum([all_titles.lower().count(kw) for kw in keywords])
            if score > 0:
                theme_scores[theme] = score
        
        # 排序主题
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        
        narratives = []
        for theme, score in sorted_themes[:3]:
            theme_names = {
                'growth': '增长叙事',
                'profitability': '盈利叙事',
                'innovation': '创新叙事',
                'competition': '竞争叙事',
                'regulation': '监管叙事',
                'macro': '宏观叙事'
            }
            
            narratives.append({
                'theme': theme_names.get(theme, theme),
                'mentions': score,
                'significance': '高' if score > 3 else '中' if score > 1 else '低'
            })
        
        return narratives
    
    def analyze_social_sentiment(self, social_data):
        """
        社交媒体情绪深度解读
        
        Args:
            social_data: 社交媒体数据
            
        Returns:
            dict: 社交媒体情绪分析
        """
        if not social_data or 'platform_results' not in social_data:
            return {}
        
        platforms = social_data['platform_results']
        
        # 平台差异分析
        platform_comparison = []
        for platform, data in platforms.items():
            stats = data['stats']
            platform_comparison.append({
                'platform': platform.upper(),
                'sentiment': stats['avg_sentiment'],
                'sentiment_label': self._get_sentiment_label(stats['avg_sentiment']),
                'positive_ratio': stats['positive_ratio'],
                'activity_level': '高' if stats['count'] > 10 else '中' if stats['count'] > 5 else '低',
                'characteristics': self._describe_platform_characteristics(platform, stats)
            })
        
        # 情绪变化分析
        sentiment_shifts = social_data.get('sentiment_shifts', [])
        shift_analysis = []
        for shift in sentiment_shifts:
            shift_analysis.append({
                'platform': shift['platform'],
                'direction': shift['direction'],
                'magnitude': '显著' if abs(shift['shift']) > 0.5 else '温和',
                'interpretation': self._interpret_sentiment_shift(shift)
            })
        
        # 热门话题分析
        keywords = social_data.get('keywords', {})
        topic_analysis = self._analyze_hot_topics(keywords)
        
        # 散户情绪 vs 机构情绪
        retail_vs_institutional = self._compare_retail_institutional(platforms)
        
        return {
            'platform_comparison': platform_comparison,
            'sentiment_shift_analysis': shift_analysis,
            'hot_topics': topic_analysis,
            'retail_vs_institutional': retail_vs_institutional,
            'overall_interpretation': self._interpret_social_overall(platforms, sentiment_shifts)
        }
    
    def _describe_platform_characteristics(self, platform, stats):
        """描述平台特征"""
        characteristics = {
            'twitter': '国际投资者、机构关注度高',
            'reddit': '散户集中、情绪波动大',
            'xueqiu': '中国价值投资者、分析深入',
            'guba': '散户情绪、短期投机氛围'
        }
        
        sentiment_desc = '看多' if stats['avg_sentiment'] > 0.2 else '看空' if stats['avg_sentiment'] < -0.2 else '分歧'
        
        return f"{characteristics.get(platform, '')} | 情绪{sentiment_desc}"
    
    def _interpret_sentiment_shift(self, shift):
        """解读情绪变化"""
        platform = shift['platform']
        direction = shift['direction']
        
        interpretations = {
            'twitter': {
                '转向乐观': '国际投资者情绪改善，可能预示外资流入',
                '转向悲观': '国际投资者情绪恶化，需警惕外资流出'
            },
            'reddit': {
                '转向乐观': '散户情绪回暖，短期可能反弹',
                '转向悲观': '散户恐慌加剧，可能超跌'
            },
            'xueqiu': {
                '转向乐观': '价值投资者开始看好，中长期信号',
                '转向悲观': '价值投资者信心动摇'
            },
            'guba': {
                '转向乐观': '散户割肉盘减少，抛压减轻',
                '转向悲观': '散户套牢情绪加重'
            }
        }
        
        return interpretations.get(platform, {}).get(direction, '情绪变化需持续关注')
    
    def _analyze_hot_topics(self, keywords):
        """分析热门话题"""
        topics = []
        
        for platform, words in keywords.items():
            top_words = list(words.keys())[:3]
            if top_words:
                topics.append({
                    'platform': platform.upper(),
                    'hot_words': top_words,
                    'theme': self._infer_topic_theme(top_words)
                })
        
        return topics
    
    def _infer_topic_theme(self, words):
        """推断话题主题"""
        word_str = ' '.join(words).lower()
        
        if any(w in word_str for w in ['earnings', 'revenue', 'profit', '业绩', '财报']):
            return '财报业绩讨论'
        elif any(w in word_str for w in ['buy', 'sell', 'hold', '买入', '卖出']):
            return '买卖策略讨论'
        elif any(w in word_str for w in ['growth', 'expansion', '增长', '发展']):
            return '增长前景讨论'
        else:
            return '一般行情讨论'
    
    def _compare_retail_institutional(self, platforms):
        """比较散户与机构情绪"""
        # 散户平台
        retail_platforms = ['reddit', 'guba']
        # 机构/专业投资者平台
        institutional_platforms = ['twitter', 'xueqiu']
        
        retail_sentiments = []
        institutional_sentiments = []
        
        for platform, data in platforms.items():
            if platform in retail_platforms:
                retail_sentiments.append(data['stats']['avg_sentiment'])
            elif platform in institutional_platforms:
                institutional_sentiments.append(data['stats']['avg_sentiment'])
        
        retail_avg = np.mean(retail_sentiments) if retail_sentiments else 0
        institutional_avg = np.mean(institutional_sentiments) if institutional_sentiments else 0
        
        gap = institutional_avg - retail_avg
        
        if gap > 0.3:
            divergence = '机构比散户乐观，可能存在信息差'
        elif gap < -0.3:
            divergence = '散户比机构乐观，需警惕情绪过热'
        else:
            divergence = '机构与散户情绪基本一致'
        
        return {
            'retail_sentiment': round(retail_avg, 4),
            'institutional_sentiment': round(institutional_avg, 4),
            'sentiment_gap': round(gap, 4),
            'divergence_analysis': divergence
        }
    
    def _interpret_social_overall(self, platforms, sentiment_shifts):
        """整体社交媒体解读"""
        all_sentiments = [p['stats']['avg_sentiment'] for p in platforms.values()]
        avg_sentiment = np.mean(all_sentiments)
        
        # 计算情绪一致性
        sentiment_std = np.std(all_sentiments)
        consistency = '高' if sentiment_std < 0.3 else '中' if sentiment_std < 0.6 else '低'
        
        # 判断趋势
        positive_shifts = sum([1 for s in sentiment_shifts if s['shift'] > 0])
        negative_shifts = sum([1 for s in sentiment_shifts if s['shift'] < 0])
        
        if positive_shifts > negative_shifts:
            trend = '情绪改善中'
        elif negative_shifts > positive_shifts:
            trend = '情绪恶化中'
        else:
            trend = '情绪震荡'
        
        return {
            'overall_sentiment': round(avg_sentiment, 4),
            'sentiment_label': self._get_sentiment_label(avg_sentiment),
            'consistency': consistency,
            'trend': trend,
            'key_takeaway': self._generate_social_takeaway(avg_sentiment, consistency, trend)
        }
    
    def _generate_social_takeaway(self, sentiment, consistency, trend):
        """生成社交媒体核心观点"""
        if sentiment > 0.3 and trend == '情绪改善中':
            return '社交媒体情绪积极且改善，短期可能获得支撑'
        elif sentiment < -0.3 and trend == '情绪恶化中':
            return '社交媒体情绪低迷且恶化，短期可能继续承压'
        elif consistency == '低':
            return '各平台情绪分歧较大，市场存在争议，等待方向明确'
        else:
            return '社交媒体情绪中性，观望氛围浓厚'
    
    def generate_contrarian_signals(self, sentiment_data):
        """
        生成逆向投资信号
        
        Args:
            sentiment_data: 情绪数据
            
        Returns:
            dict: 逆向投资信号
        """
        signals = []
        
        # 极度悲观 - 买入信号
        if sentiment_data.get('overall_sentiment', 0) < -0.5:
            signals.append({
                'type': 'BUY',
                'strength': 'STRONG',
                'strategy': '逆向买入',
                'reason': '市场情绪极度悲观，恐慌情绪浓厚，可能是底部区域',
                'risk_management': '分批建仓，设置止损位-10%',
                'time_horizon': '中长期（3-6个月）'
            })
        
        # 极度乐观 - 卖出信号
        elif sentiment_data.get('overall_sentiment', 0) > 0.5:
            signals.append({
                'type': 'SELL',
                'strength': 'STRONG',
                'strategy': '逆向卖出/减仓',
                'reason': '市场情绪极度乐观，可能过热，警惕回调风险',
                'risk_management': '逐步减仓，保留核心仓位',
                'time_horizon': '短期（1-2周）'
            })
        
        # 情绪拐点 - 买入信号
        shifts = sentiment_data.get('sentiment_shift_analysis', [])
        positive_shifts = [s for s in shifts if '转向乐观' in s.get('direction', '')]
        
        if len(positive_shifts) >= 2:
            signals.append({
                'type': 'BUY',
                'strength': 'MEDIUM',
                'strategy': '趋势跟随',
                'reason': '多个平台情绪同时转向乐观，可能形成情绪拐点',
                'risk_management': '适度建仓，确认趋势后加仓',
                'time_horizon': '中期（1-3个月）'
            })
        
        # 机构-散户分歧 - 跟随机构
        retail_vs_inst = sentiment_data.get('retail_vs_institutional', {})
        if retail_vs_inst.get('sentiment_gap', 0) > 0.3:
            signals.append({
                'type': 'BUY',
                'strength': 'MEDIUM',
                'strategy': '跟随机构',
                'reason': '机构情绪明显好于散户，可能存在信息优势',
                'risk_management': '参考机构观点，但独立判断',
                'time_horizon': '中期（1-3个月）'
            })
        
        if not signals:
            signals.append({
                'type': 'HOLD',
                'strength': 'WEAK',
                'strategy': '观望',
                'reason': '情绪信号不明确，等待更清晰的信号',
                'risk_management': '保持现有仓位',
                'time_horizon': '短期（1周内）'
            })
        
        return signals
    
    def generate_comprehensive_report(self, social_data=None, news_data=None):
        """生成综合分析报告"""
        report = {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'report_type': '市场信息深度解读',
            'executive_summary': self._generate_executive_summary(social_data, news_data),
            'news_analysis': self.analyze_key_news(news_data) if news_data else {},
            'social_analysis': self.analyze_social_sentiment(social_data) if social_data else {},
            'contrarian_signals': self.generate_contrarian_signals(
                self.analyze_social_sentiment(social_data) if social_data else {}
            ),
            'action_items': self._generate_action_items(social_data, news_data)
        }
        
        return report
    
    def _generate_executive_summary(self, social_data, news_data):
        """生成执行摘要"""
        summary_parts = []
        
        if social_data:
            sentiment = social_data.get('composite_sentiment', 0)
            summary_parts.append(f'社交媒体情绪：{self._get_sentiment_label(sentiment)} ({sentiment})')
        
        if news_data:
            sentiment = news_data.get('composite_sentiment', 0)
            summary_parts.append(f'新闻情绪：{self._get_sentiment_label(sentiment)} ({sentiment})')
        
        return ' | '.join(summary_parts) if summary_parts else '数据不足'
    
    def _generate_action_items(self, social_data, news_data):
        """生成行动建议"""
        items = []
        
        if social_data:
            items.append('持续监控社交媒体情绪变化，特别是Twitter和Reddit')
            items.append('关注散户与机构情绪差异，寻找信息差机会')
        
        if news_data:
            items.append('跟踪权威媒体对公司的报道，特别是财报和监管动态')
            items.append('关注分析师评级变化，了解机构观点')
        
        items.append('结合技术分析确认入场时机')
        items.append('设置止损位，控制情绪交易风险')
        
        return items
    
    def _get_sentiment_label(self, sentiment):
        """获取情绪标签"""
        if sentiment >= 0.3:
            return '乐观'
        elif sentiment >= 0.1:
            return '偏乐观'
        elif sentiment >= -0.1:
            return '中性'
        elif sentiment >= -0.3:
            return '偏悲观'
        else:
            return '悲观'


def main():
    parser = argparse.ArgumentParser(description='市场信息深度解读分析工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--data-file', help='已有数据文件路径')
    parser.add_argument('--report-type', default='comprehensive',
                       choices=['comprehensive', 'news', 'social'],
                       help='报告类型')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = MarketIntelligenceAnalyzer(args.symbol, args.data_file)
    
    # 加载数据（如果提供了数据文件）
    social_data = None
    news_data = None
    
    if args.data_file:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            social_data = data.get('detailed_results', {}).get('social_media')
            news_data = data.get('detailed_results', {}).get('authority_news')
    
    # 生成报告
    report = analyzer.generate_comprehensive_report(social_data, news_data)
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_intelligence_analysis.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print_comprehensive_report(report)
    
    print(f'\n完整报告已保存: {output_file}')


def print_comprehensive_report(report):
    """打印综合报告"""
    print('\n' + '=' * 80)
    print(f'市场信息深度解读报告 - {report["symbol"]}')
    print('=' * 80)
    
    print(f'\n【执行摘要】')
    print(f'  {report["executive_summary"]}')
    
    # 重点资讯分析
    if report.get('news_analysis'):
        news = report['news_analysis']
        print(f'\n【重点资讯深度解读】')
        
        if news.get('key_news'):
            print(f'\n  关键新闻（按影响力排序）:')
            for i, item in enumerate(news['key_news'][:3], 1):
                print(f'\n  {i}. {item["title"]}')
                print(f'     来源: {item["source"]} | 情绪: {item["sentiment"]} | 影响: {item["impact_score"]}')
                print(f'     解读: {item["interpretation"]}')
        
        if news.get('category_analysis'):
            print(f'\n  分类别分析:')
            for cat, analysis in news['category_analysis'].items():
                print(f'    • {analysis["name"]}: {analysis["sentiment_label"]} | {analysis["impact_assessment"]}')
                for insight in analysis.get('key_points', []):
                    print(f'      - {insight}')
        
        if news.get('narrative_analysis'):
            print(f'\n  市场主线/叙事:')
            for narrative in news['narrative_analysis']:
                print(f'    • {narrative["theme"]} (提及{narrative["mentions"]}次) - 重要性: {narrative["significance"]}')
    
    # 社交媒体分析
    if report.get('social_analysis'):
        social = report['social_analysis']
        print(f'\n【社交媒体情绪深度解读】')
        
        if social.get('platform_comparison'):
            print(f'\n  平台情绪对比:')
            for platform in social['platform_comparison']:
                print(f'    • {platform["platform"]}: {platform["sentiment_label"]} | 活跃度: {platform["activity_level"]}')
                print(f'      特征: {platform["characteristics"]}')
        
        if social.get('sentiment_shift_analysis'):
            print(f'\n  情绪变化分析:')
            for shift in social['sentiment_shift_analysis']:
                print(f'    • {shift["platform"]}: {shift["direction"]} ({shift["magnitude"]})')
                print(f'      解读: {shift["interpretation"]}')
        
        if social.get('retail_vs_institutional'):
            retail = social['retail_vs_institutional']
            print(f'\n  散户 vs 机构情绪:')
            print(f'    • 散户情绪: {retail["retail_sentiment"]}')
            print(f'    • 机构情绪: {retail["institutional_sentiment"]}')
            print(f'    • 差异分析: {retail["divergence_analysis"]}')
        
        if social.get('overall_interpretation'):
            overall = social['overall_interpretation']
            print(f'\n  整体解读:')
            print(f'    • 情绪水平: {overall["sentiment_label"]}')
            print(f'    • 一致性: {overall["consistency"]}')
            print(f'    • 趋势: {overall["trend"]}')
            print(f'    • 核心观点: {overall["key_takeaway"]}')
    
    # 逆向投资信号
    if report.get('contrarian_signals'):
        print(f'\n【逆向投资信号】')
        for i, signal in enumerate(report['contrarian_signals'], 1):
            print(f'\n  信号 {i}: {signal["type"]} (强度: {signal["strength"]})')
            print(f'    策略: {signal["strategy"]}')
            print(f'    理由: {signal["reason"]}')
            print(f'    风险管理: {signal["risk_management"]}')
            print(f'    时间周期: {signal["time_horizon"]}')
    
    # 行动建议
    if report.get('action_items'):
        print(f'\n【行动建议】')
        for i, item in enumerate(report['action_items'], 1):
            print(f'  {i}. {item}')
    
    print('\n' + '=' * 80)


if __name__ == '__main__':
    main()
