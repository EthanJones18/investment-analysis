#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号自动化监控脚本
定时监控多个公众号的新文章

使用方法:
    python monitor.py --accounts accounts.txt --interval 3600
"""

import argparse
import json
import os
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


class WechatMonitor:
    """微信公众号监控器"""
    
    def __init__(self, accounts_file, token=None, output_dir="./wechat_monitor"):
        """
        初始化监控器
        
        Args:
            accounts_file: 公众号列表文件路径
            token: 抓包获取的token
            output_dir: 输出目录
        """
        self.accounts = self.load_accounts(accounts_file)
        self.token = token or os.getenv("WECHAT_TOKEN")
        self.output_dir = output_dir
        self.session = requests.Session()
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 加载历史记录
        self.history_file = os.path.join(output_dir, "history.json")
        self.history = self.load_history()
        
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        }
    
    def load_accounts(self, filepath):
        """加载公众号列表"""
        accounts = []
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) >= 2:
                            accounts.append({
                                "name": parts[0].strip(),
                                "biz": parts[1].strip(),
                            })
        return accounts
    
    def load_history(self):
        """加载历史记录"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_history(self):
        """保存历史记录"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def get_latest_articles(self, biz, count=5):
        """
        获取公众号最新文章
        
        Args:
            biz: 公众号biz
            count: 获取数量
            
        Returns:
            list: 文章列表
        """
        url = "https://mp.weixin.qq.com/mp/profile_ext"
        params = {
            "action": "getmsg",
            "__biz": biz,
            "f": "json",
            "offset": 0,
            "count": count,
            "is_ok": 1,
            "scene": 124,
            "appmsg_token": self.token,
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=30)
            data = response.json()
            
            if data.get("ret") == 0:
                general_msg_list = json.loads(data.get("general_msg_list", "{}"))
                return general_msg_list.get("list", [])
            return []
        except Exception as e:
            print(f"获取文章失败 [{biz}]: {e}")
            return []
    
    def check_new_articles(self, account):
        """
        检查公众号新文章
        
        Args:
            account: 公众号信息
            
        Returns:
            list: 新文章列表
        """
        biz = account["biz"]
        name = account["name"]
        
        print(f"正在检查: {name} ({biz})")
        
        # 获取最新文章
        articles = self.get_latest_articles(biz, count=10)
        
        # 获取历史记录
        account_history = self.history.get(biz, [])
        history_ids = set(account_history)
        
        # 找出新文章
        new_articles = []
        for item in articles:
            msg_id = item.get("comm_msg_info", {}).get("id", "")
            if msg_id and msg_id not in history_ids:
                new_articles.append(item)
                account_history.append(msg_id)
        
        # 更新历史记录
        self.history[biz] = account_history[-100:]  # 只保留最近100条
        
        return new_articles
    
    def parse_article_info(self, article_data):
        """解析文章信息"""
        comm_msg_info = article_data.get("comm_msg_info", {})
        app_msg_ext_info = article_data.get("app_msg_ext_info", {})
        
        articles = []
        
        # 主文章
        if app_msg_ext_info:
            article = {
                "title": app_msg_ext_info.get("title", ""),
                "author": app_msg_ext_info.get("author", ""),
                "content_url": app_msg_ext_info.get("content_url", "").replace("&amp;", "&"),
                "publish_time": datetime.fromtimestamp(comm_msg_info.get("datetime", 0)).strftime("%Y-%m-%d %H:%M:%S"),
            }
            articles.append(article)
        
        # 子文章
        for item in app_msg_ext_info.get("multi_app_msg_item_list", []):
            article = {
                "title": item.get("title", ""),
                "author": item.get("author", ""),
                "content_url": item.get("content_url", "").replace("&amp;", "&"),
                "publish_time": datetime.fromtimestamp(comm_msg_info.get("datetime", 0)).strftime("%Y-%m-%d %H:%M:%S"),
            }
            articles.append(article)
        
        return articles
    
    def save_new_articles(self, account, new_articles):
        """保存新文章到文件"""
        if not new_articles:
            return
        
        # 解析文章信息
        all_articles = []
        for item in new_articles:
            articles = self.parse_article_info(item)
            all_articles.extend(articles)
        
        if not all_articles:
            return
        
        # 创建DataFrame
        df = pd.DataFrame(all_articles)
        df['account_name'] = account['name']
        df['account_biz'] = account['biz']
        df['crawl_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 保存到Excel
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"new_articles_{date_str}.xlsx"
        filepath = os.path.join(self.output_dir, filename)
        
        if os.path.exists(filepath):
            # 追加到现有文件
            existing_df = pd.read_excel(filepath)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"  新文章已保存: {filepath}")
    
    def run_once(self):
        """执行一次监控"""
        print(f"\n{'='*60}")
        print(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        total_new = 0
        
        for account in self.accounts:
            new_articles = self.check_new_articles(account)
            
            if new_articles:
                articles_info = []
                for item in new_articles:
                    articles_info.extend(self.parse_article_info(item))
                
                print(f"  发现 {len(articles_info)} 篇新文章:")
                for article in articles_info:
                    print(f"    - {article['title'][:50]}...")
                
                self.save_new_articles(account, new_articles)
                total_new += len(articles_info)
            else:
                print(f"  无新文章")
            
            time.sleep(2)  # 间隔请求
        
        # 保存历史记录
        self.save_history()
        
        print(f"\n监控完成，共发现 {total_new} 篇新文章")
        return total_new
    
    def run_loop(self, interval=3600):
        """
        持续监控循环
        
        Args:
            interval: 检查间隔（秒）
        """
        print(f"开始监控 {len(self.accounts)} 个公众号")
        print(f"检查间隔: {interval}秒 ({interval/60:.1f}分钟)")
        print("按 Ctrl+C 停止监控\n")
        
        try:
            while True:
                self.run_once()
                print(f"\n下次检查时间: {(datetime.now().timestamp() + interval)}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n监控已停止")


def main():
    parser = argparse.ArgumentParser(description="微信公众号自动化监控工具")
    parser.add_argument("--accounts", required=True, help="公众号列表文件路径（格式：名称,biz）")
    parser.add_argument("--token", help="抓包获取的token")
    parser.add_argument("--interval", type=int, default=3600, help="检查间隔秒数（默认3600秒=1小时）")
    parser.add_argument("--output", default="./wechat_monitor", help="输出目录")
    parser.add_argument("--once", action="store_true", help="只执行一次，不进入循环")
    
    args = parser.parse_args()
    
    # 初始化监控器
    monitor = WechatMonitor(
        accounts_file=args.accounts,
        token=args.token,
        output_dir=args.output
    )
    
    if args.once:
        monitor.run_once()
    else:
        monitor.run_loop(interval=args.interval)


if __name__ == "__main__":
    main()
