#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章详情爬取脚本
获取文章的阅读量、点赞数、评论等详细信息

使用方法:
    python article_detail.py --url "文章链接" --token "your_token"
"""

import argparse
import json
import os
import re
import time
from urllib.parse import parse_qs, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


class WechatArticleDetail:
    """微信公众号文章详情获取器"""
    
    def __init__(self, token=None, cookie=None):
        """
        初始化
        
        Args:
            token: 从抓包获取的token
            cookie: 请求cookie
        """
        self.token = token or os.getenv("WECHAT_TOKEN")
        self.cookie = cookie or os.getenv("WECHAT_COOKIE")
        self.session = requests.Session()
        
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://mp.weixin.qq.com/",
        }
        
        if self.cookie:
            self.headers["Cookie"] = self.cookie
    
    def extract_params_from_url(self, url):
        """
        从文章链接中提取参数
        
        Args:
            url: 文章链接
            
        Returns:
            dict: 包含biz、mid、idx、sn等参数
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        return {
            "biz": params.get("__biz", [""])[0],
            "mid": params.get("mid", [""])[0],
            "idx": params.get("idx", [""])[0],
            "sn": params.get("sn", [""])[0],
        }
    
    def get_read_like_data(self, url):
        """
        获取文章阅读量和点赞数
        
        Args:
            url: 文章链接
            
        Returns:
            dict: 包含read_num、like_num等数据
        """
        params = self.extract_params_from_url(url)
        
        if not all([params["biz"], params["mid"], params["sn"]]):
            print(f"无法从URL提取必要参数: {url}")
            return {}
        
        # 构造阅读量接口URL
        read_url = "https://mp.weixin.qq.com/mp/getappmsgext"
        
        data = {
            "__biz": params["biz"],
            "mid": params["mid"],
            "sn": params["sn"],
            "idx": params["idx"] or "1",
            "appmsg_token": self.token,
            "x5": "0",
        }
        
        try:
            response = self.session.post(read_url, data=data, headers=self.headers, timeout=30)
            result = response.json()
            
            if result.get("appmsgstat"):
                stat = result["appmsgstat"]
                return {
                    "read_count": stat.get("read_num", 0),
                    "like_count": stat.get("like_num", 0),
                    "old_like_count": stat.get("old_like_num", 0),
                    "is_login": result.get("is_login", False),
                }
            else:
                return {"error": result.get("errmsg", "获取失败")}
                
        except Exception as e:
            print(f"获取阅读数据异常: {e}")
            return {"error": str(e)}
    
    def get_comments(self, url, offset=0, limit=100):
        """
        获取文章评论
        
        Args:
            url: 文章链接
            offset: 评论偏移量
            limit: 每页评论数
            
        Returns:
            list: 评论列表
        """
        params = self.extract_params_from_url(url)
        
        if not all([params["biz"], params["mid"]]):
            return []
        
        comment_url = "https://mp.weixin.qq.com/mp/appmsg_comment"
        
        get_params = {
            "action": "getcomment",
            "__biz": params["biz"],
            "mid": params["mid"],
            "sn": params["sn"],
            "idx": params["idx"] or "1",
            "offset": offset,
            "limit": limit,
            "appmsg_token": self.token,
        }
        
        try:
            response = self.session.get(comment_url, params=get_params, headers=self.headers, timeout=30)
            result = response.json()
            
            if result.get("base_resp", {}).get("ret") == 0:
                comment_list = result.get("comment", [])
                comments = []
                
                for item in comment_list:
                    comment = {
                        "nick_name": item.get("nick_name", ""),
                        "content": item.get("content", ""),
                        "like_count": item.get("like_num", 0),
                        "reply": item.get("reply", {}).get("content", "") if item.get("reply") else "",
                        "create_time": item.get("create_time", ""),
                    }
                    comments.append(comment)
                
                return comments
            else:
                return []
                
        except Exception as e:
            print(f"获取评论异常: {e}")
            return []
    
    def get_article_content(self, url):
        """
        获取文章内容
        
        Args:
            url: 文章链接
            
        Returns:
            dict: 包含标题、作者、内容等信息
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            response = self.session.get(url, headers=headers, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取标题
            title = soup.find("h1", class_="rich_media_title")
            title = title.get_text(strip=True) if title else ""
            
            # 获取作者
            author = soup.find("span", class_="profile_nickname")
            author = author.get_text(strip=True) if author else ""
            
            # 获取发布时间
            publish_time = soup.find("em", id="publish_time")
            publish_time = publish_time.get_text(strip=True) if publish_time else ""
            
            # 获取内容
            content_div = soup.find(id="js_content")
            content = str(content_div) if content_div else ""
            
            # 获取纯文本内容
            content_text = content_div.get_text(strip=True) if content_div else ""
            
            return {
                "title": title,
                "author": author,
                "publish_time": publish_time,
                "content_html": content,
                "content_text": content_text,
            }
            
        except Exception as e:
            print(f"获取文章内容异常: {e}")
            return {}
    
    def get_full_article_info(self, url):
        """
        获取文章完整信息
        
        Args:
            url: 文章链接
            
        Returns:
            dict: 文章完整信息
        """
        print(f"正在获取文章详情: {url[:50]}...")
        
        # 获取基础内容
        content_info = self.get_article_content(url)
        
        # 获取阅读点赞数据
        read_like_info = self.get_read_like_data(url)
        
        # 获取评论
        comments = self.get_comments(url)
        
        # 合并数据
        result = {
            "url": url,
            **content_info,
            **read_like_info,
            "comments": comments,
            "comment_count": len(comments),
        }
        
        return result


def main():
    parser = argparse.ArgumentParser(description="微信公众号文章详情获取工具")
    parser.add_argument("--url", required=True, help="文章链接")
    parser.add_argument("--token", help="抓包获取的token（也可设置环境变量 WECHAT_TOKEN）")
    parser.add_argument("--cookie", help="请求cookie")
    parser.add_argument("--output", help="输出文件路径（JSON格式）")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("微信公众号文章详情获取工具")
    print("=" * 60)
    
    # 初始化
    detail_getter = WechatArticleDetail(token=args.token, cookie=args.cookie)
    
    # 获取文章详情
    article_info = detail_getter.get_full_article_info(args.url)
    
    # 打印结果
    print("\n文章信息:")
    print(f"  标题: {article_info.get('title', 'N/A')}")
    print(f"  作者: {article_info.get('author', 'N/A')}")
    print(f"  发布时间: {article_info.get('publish_time', 'N/A')}")
    print(f"  阅读量: {article_info.get('read_count', 'N/A')}")
    print(f"  点赞数: {article_info.get('like_count', 'N/A')}")
    print(f"  评论数: {article_info.get('comment_count', 0)}")
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(article_info, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存: {args.output}")


if __name__ == "__main__":
    main()
