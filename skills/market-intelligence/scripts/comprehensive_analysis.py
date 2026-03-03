#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合市场信息分析脚本
整合社交媒体监控、权威资讯爬取、情绪分析等模块

使用方法:
    python comprehensive_analysis.py --symbol AAPL --days 7
"""

import argparse
import json
import os
import subprocess
from datetime import datetime

import pandas as pd


class ComprehensiveMarketAnalysis:
    """综合市场信息分析器"""
    
    def __init__(self, symbol, days=7):
        """
        初始化
        
        Args:
            symbol: 股票代码
            days: 分析天数
        """
        self.symbol = symbol
        self.days = days
        self.output_dir = './output'
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
    
    def run_social_media_analysis(self):
        """执行社交媒体分析"""
        print('=' * 60)
        print(f'步骤 1/3: 社交媒体监控 - {self.symbol}')
        print('=' * 60)
        
        try:
            result = subprocess.run([
                'python', 'scripts/social_media_monitor.py',
                '--symbol', self.symbol,
                '--platform', 'twitter,reddit,xueqiu,guba',
                '--hours', str(self.days * 24),
                '--output', self.output_dir
            ], capture_output=True, text=True, check=True)
            
            print(result.stdout)
            
            # 读取结果
            output_file = os.path.join(self.output_dir, f'{self.symbol}_social_media.json')
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
        except subprocess.CalledProcessError as e:
            print(f'社交媒体分析失败: {e}')
            print(f'错误输出: {e.stderr}')
            return None
        except Exception as e:
            print(f'社交媒体分析异常: {e}')
            return None
    
    def run_authority_news_analysis(self):
        """执行权威资讯分析"""
        print('\n' + '=' * 60)
        print(f'步骤 2/3: 权威资讯爬取 - {self.symbol}')
        print('=' * 60)
        
        try:
            result = subprocess.run([
                'python', 'scripts/authority_news_crawler.py',
                '--symbol', self.symbol,
                '--sources', 'bloomberg,reuters,cnbc,seekingalpha,caixin,yicai',
                '--days', str(self.days),
                '--output', self.output_dir
            ], capture_output=True, text=True, check=True)
            
            print(result.stdout)
            
            # 读取结果
            output_file = os.path.join(self.output_dir, f'{self.symbol}_authority_news.json')
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
        except subprocess.CalledProcessError as e:
            print(f'权威资讯分析失败: {e}')
            print(f'错误输出: {e.stderr}')
            return None
        except Exception as e:
            print(f'权威资讯分析异常: {e}')
            return None
    
    def run_sentiment_index_building(self, social_data, news_data):
        """执行情绪指数构建"""
        print('\n' + '=' * 60)
        print(f'步骤 3/3: 情绪指数构建 - {self.symbol}')
        print('=' * 60)
        
        try:
            result = subprocess.run([
                'python', 'scripts/sentiment_index.py',
                '--symbol', self.symbol,
                '--components', 'news,social,options,analyst',
                '--output', self.output_dir
            ], capture_output=True, text=True, check=True)
            
            print(result.stdout)
            
            # 读取结果
            output_file = os.path.join(self.output_dir, f'{self.symbol}_sentiment_index.json')
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
        except subprocess.CalledProcessError as e:
            print(f'情绪指数构建失败: {e}')
            print(f'错误输出: {e.stderr}')
            return None
        except Exception as e:
            print(f'情绪指数构建异常: {e}')
            return None
    
    def integrate_analysis(self, social_data, news_data, sentiment_index):
        """整合所有分析结果"""
        
        # 计算综合情绪
        sentiments = []
        
        if social_data and 'composite_sentiment' in social_data:
            sentiments.append(('社交媒体', social_data['composite_sentiment']))
        
        if news_data and 'composite_sentiment' in news_data:
            sentiments.append(('权威资讯', news_data['composite_sentiment']))
        
        if sentiment_index and 'composite_sentiment_index' in sentiment_index:
            sentiments.append(('情绪指数', sentiment_index['composite_sentiment_index']['index_value'] / 50 - 1))
        
        # 计算加权平均
        if sentiments:
            avg_sentiment = sum([s[1] for s in sentiments]) / len(sentiments)
        else:
            avg_sentiment = 0
        
        # 生成综合评估
        if avg_sentiment >= 0.3:
            overall_assessment = '市场情绪积极，关注潜在过热风险'
            trading_signal = '偏多，但注意控制仓位'
        elif avg_sentiment >= 0.1:
            overall_assessment = '市场情绪偏积极，可适度参与'
            trading_signal = '轻度偏多'
        elif avg_sentiment >= -0.1:
            overall_assessment = '市场情绪中性，观望为主'
            trading_signal = '观望'
        elif avg_sentiment >= -0.3:
            overall_assessment = '市场情绪偏消极，谨慎操作'
            trading_signal = '轻度偏空'
        else:
            overall_assessment = '市场情绪消极，可能存在超卖机会'
            trading_signal = '偏空，但关注反弹机会'
        
        return {
            'symbol': self.symbol,
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'analysis_period_days': self.days,
            'overall_sentiment': round(avg_sentiment, 4),
            'overall_assessment': overall_assessment,
            'trading_signal': trading_signal,
            'sentiment_breakdown': sentiments,
            'data_sources': {
                'social_media': {
                    'status': '成功' if social_data else '失败',
                    'posts_count': social_data.get('total_posts', 0) if social_data else 0,
                    'sentiment': social_data.get('sentiment_label', 'N/A') if social_data else 'N/A'
                },
                'authority_news': {
                    'status': '成功' if news_data else '失败',
                    'articles_count': news_data.get('news_count', 0) if news_data else 0,
                    'sentiment': news_data.get('sentiment_label', 'N/A') if news_data else 'N/A'
                },
                'sentiment_index': {
                    'status': '成功' if sentiment_index else '失败',
                    'index_value': sentiment_index.get('composite_sentiment_index', {}).get('index_value', 'N/A') if sentiment_index else 'N/A'
                }
            },
            'detailed_results': {
                'social_media': social_data,
                'authority_news': news_data,
                'sentiment_index': sentiment_index
            }
        }
    
    def generate_comprehensive_report(self):
        """生成综合分析报告"""
        print('\n' + '=' * 60)
        print(f'开始综合市场信息分析 - {self.symbol}')
        print(f'分析周期: {self.days} 天')
        print('=' * 60)
        
        # 执行三个核心分析模块
        social_data = self.run_social_media_analysis()
        news_data = self.run_authority_news_analysis()
        sentiment_index = self.run_sentiment_index_building(social_data, news_data)
        
        # 整合分析结果
        comprehensive_report = self.integrate_analysis(social_data, news_data, sentiment_index)
        
        # 执行深度解读分析
        print('\n' + '=' * 60)
        print(f'步骤 4/4: 深度解读分析 - {self.symbol}')
        print('=' * 60)
        
        try:
            # 保存临时数据文件供深度分析使用
            temp_data_file = os.path.join(self.output_dir, f'{self.symbol}_temp_data.json')
            with open(temp_data_file, 'w', encoding='utf-8') as f:
                json.dump(comprehensive_report, f, ensure_ascii=False)
            
            # 调用深度解读分析
            result = subprocess.run([
                'python', 'scripts/market_intelligence_analysis.py',
                '--symbol', self.symbol,
                '--data-file', temp_data_file,
                '--report-type', 'comprehensive',
                '--output', self.output_dir
            ], capture_output=True, text=True, check=True)
            
            print(result.stdout)
            
            # 清理临时文件
            if os.path.exists(temp_data_file):
                os.remove(temp_data_file)
                
        except subprocess.CalledProcessError as e:
            print(f'深度解读分析失败: {e}')
            print(f'错误输出: {e.stderr}')
        except Exception as e:
            print(f'深度解读分析异常: {e}')
        
        # 保存综合报告
        output_file = os.path.join(self.output_dir, f'{self.symbol}_comprehensive_analysis.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_report, f, ensure_ascii=False, indent=2)
        
        # 打印综合报告
        self._print_comprehensive_report(comprehensive_report)
        
        return comprehensive_report
    
    def _print_comprehensive_report(self, report):
        """打印综合报告"""
        print('\n' + '=' * 60)
        print(f'综合市场信息分析报告 - {report["symbol"]}')
        print('=' * 60)
        
        print(f'\n【分析概览】')
        print(f'  分析日期: {report["analysis_date"]}')
        print(f'  分析周期: {report["analysis_period_days"]} 天')
        
        print(f'\n【综合情绪评估】')
        print(f'  整体情绪分数: {report["overall_sentiment"]}')
        print(f'  市场评估: {report["overall_assessment"]}')
        print(f'  交易信号: {report["trading_signal"]}')
        
        print(f'\n【情绪来源分解】')
        for source, sentiment in report['sentiment_breakdown']:
            print(f'  {source}: {sentiment}')
        
        print(f'\n【数据源状态】')
        for source, status in report['data_sources'].items():
            print(f'  {source}: {status["status"]}')
            if 'posts_count' in status:
                print(f'    - 帖子数: {status["posts_count"]}')
            if 'articles_count' in status:
                print(f'    - 文章数: {status["articles_count"]}')
            if 'sentiment' in status:
                print(f'    - 情绪: {status["sentiment"]}')
        
        print('\n' + '=' * 60)
        print(f'完整报告已保存: ./output/{report["symbol"]}_comprehensive_analysis.json')
        print('=' * 60)


def main():
    parser = argparse.ArgumentParser(description='综合市场信息分析工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--days', type=int, default=7, help='分析天数')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 初始化分析器
    analyzer = ComprehensiveMarketAnalysis(args.symbol, args.days)
    analyzer.output_dir = args.output
    
    # 执行综合分析
    analyzer.generate_comprehensive_report()


if __name__ == '__main__':
    main()
