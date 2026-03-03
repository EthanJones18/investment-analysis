#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章快速爬取脚本
基于抓包获取的token，快速爬取公众号文章

使用方法:
    python quick_spider.py --biz MzIxNzg1ODQ0MQ== --token "your_token" --pages 10
"""

import argparse
import json
import os
import re
import time
import urllib.parse
from datetime import datetime
from urllib.parse import urlencode

import pandas as pd
import requests
from bs4 import BeautifulSoup


class WechatQuickSpider:
    """微信公众号快速爬取器"""
    
    def __init__(self, biz, token=None, cookie=None, output_dir="./wechat_data"):
        """
        初始化爬虫
        
        Args:
            biz: 公众号biz标识
            token: 从抓包获取的token（可选，可从环境变量获取）
            cookie: 请求cookie（可选）
            output_dir: 输出目录
        """
        self.biz = biz
        self.token = token or os.getenv("WECHAT_TOKEN")
        self.cookie = cookie or os.getenv("WECHAT_COOKIE")
        self.output_dir = output_dir
        self.session = requests.Session()
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}",
        }
        
        if self.cookie:
            self.headers["Cookie"] = self.cookie
    
    def get_article_list(self, offset=0, count=10):
        """
        获取文章列表
        
        Args:
            offset: 偏移量
            count: 每页数量
            
        Returns:
            list: 文章列表
        """
        if not self.token:
            raise ValueError("Token不能为空，请通过抓包获取或设置环境变量 WECHAT_TOKEN")
        
        url = "https://mp.weixin.qq.com/mp/profile_ext"
        params = {
            "action": "getmsg",
            "__biz": self.biz,
            "f": "json",
            "offset": offset,
            "count": count,
            "is_ok": 1,
            "scene": 124,
            "uin": "777",
            "key": "777",
            "pass_ticket": "",
            "wxtoken": "",
            "appmsg_token": self.token,
            "x5": 0,
        }
        
        try:
            response = self.session.get(url, params=params, headers=self.headers, timeout=30)
            data = response.json()
            
            if data.get("ret") == 0:
                general_msg_list = json.loads(data.get("general_msg_list", "{}"))
                return general_msg_list.get("list", [])
            else:
                print(f"获取文章列表失败: {data.get('errmsg', '未知错误')}")
                return []
                
        except Exception as e:
            print(f"请求异常: {e}")
            return []
    
    def parse_article(self, article_data):
        """
        解析文章数据
        
        Args:
            article_data: 原始文章数据
            
        Returns:
            list: 解析后的文章信息列表
        """
        comm_msg_info = article_data.get("comm_msg_info", {})
        app_msg_ext_info = article_data.get("app_msg_ext_info", {})
        
        # 处理多文章消息
        articles = []
        
        # 主文章
        if app_msg_ext_info:
            article = {
                "title": app_msg_ext_info.get("title", ""),
                "digest": app_msg_ext_info.get("digest", ""),
                "author": app_msg_ext_info.get("author", ""),
                "content_url": app_msg_ext_info.get("content_url", "").replace("&amp;", "&"),
                "source_url": app_msg_ext_info.get("source_url", ""),
                "cover_url": app_msg_ext_info.get("cover", ""),
                "publish_time": datetime.fromtimestamp(comm_msg_info.get("datetime", 0)).strftime("%Y-%m-%d %H:%M:%S"),
                "msg_id": comm_msg_info.get("id", ""),
            }
            articles.append(article)
        
        # 子文章（多图文消息）
        multi_app_msg_item_list = app_msg_ext_info.get("multi_app_msg_item_list", [])
        for item in multi_app_msg_item_list:
            article = {
                "title": item.get("title", ""),
                "digest": item.get("digest", ""),
                "author": item.get("author", ""),
                "content_url": item.get("content_url", "").replace("&amp;", "&"),
                "source_url": item.get("source_url", ""),
                "cover_url": item.get("cover", ""),
                "publish_time": datetime.fromtimestamp(comm_msg_info.get("datetime", 0)).strftime("%Y-%m-%d %H:%M:%S"),
                "msg_id": comm_msg_info.get("id", ""),
            }
            articles.append(article)
        
        return articles
    
    def fetch_articles(self, pages=10, delay=3):
        """
        批量获取文章
        
        Args:
            pages: 要获取的页数
            delay: 每页请求间隔（秒）
            
        Returns:
            list: 所有文章列表
        """
        all_articles = []
        
        for page in range(pages):
            offset = page * 10
            print(f"正在获取第 {page + 1}/{pages} 页文章...")
            
            raw_list = self.get_article_list(offset=offset, count=10)
            
            if not raw_list:
                print(f"第 {page + 1} 页无数据，可能已到达末尾")
                break
            
            for item in raw_list:
                articles = self.parse_article(item)
                all_articles.extend(articles)
            
            print(f"第 {page + 1} 页获取完成，当前共 {len(all_articles)} 篇文章")
            
            # 延时防止被封
            if page < pages - 1:
                time.sleep(delay)
        
        return all_articles
    
    def save_to_excel(self, articles, filename="article_list.xlsx"):
        """
        保存文章列表到Excel
        
        Args:
            articles: 文章列表
            filename: 文件名
        """
        if not articles:
            print("没有文章可保存")
            return
        
        df = pd.DataFrame(articles)
        filepath = os.path.join(self.output_dir, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"文章列表已保存: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="微信公众号文章快速爬取工具")
    parser.add_argument("--biz", required=True, help="公众号biz标识（从文章链接中获取）")
    parser.add_argument("--token", help="抓包获取的token（也可设置环境变量 WECHAT_TOKEN）")
    parser.add_argument("--cookie", help="请求cookie（也可设置环境变量 WECHAT_COOKIE）")
    parser.add_argument("--pages", type=int, default=10, help="要爬取的页数（默认10页，每页约10-15篇文章）")
    parser.add_argument("--delay", type=float, default=3, help="请求间隔秒数（默认3秒）")
    parser.add_argument("--output", default="./wechat_data", help="输出目录（默认./wechat_data）")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("微信公众号文章快速爬取工具")
    print("=" * 60)
    print(f"目标公众号biz: {args.biz}")
    print(f"计划爬取页数: {args.pages}")
    print(f"请求间隔: {args.delay}秒")
    print(f"输出目录: {args.output}")
    print("=" * 60)
    
    # 初始化爬虫
    spider = WechatQuickSpider(
        biz=args.biz,
        token=args.token,
        cookie=args.cookie,
        output_dir=args.output
    )
    
    # 获取文章列表
    articles = spider.fetch_articles(pages=args.pages, delay=args.delay)
    
    if articles:
        # 保存到Excel
        spider.save_to_excel(articles)
        print(f"\n爬取完成！共获取 {len(articles)} 篇文章")
    else:
        print("\n未获取到任何文章，请检查token是否有效")


if __name__ == "__main__":
    main()
