#!/usr/bin/env python3
"""
Truth Social 爬虫
爬取特朗普 Truth Social 媒体网站的最新资讯
"""

import requests
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
import html

class TruthSocialScraper:
    """Truth Social 爬虫类"""
    
    def __init__(self):
        self.base_url = "https://truthsocial.com"
        self.api_base = "https://truthsocial.com/api/v1"
        self.session = requests.Session()
        
        # 设置请求头模拟浏览器
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        
    def get_user_truths(self, username: str = "realDonaldTrump", limit: int = 20) -> List[Dict]:
        """
        获取指定用户的 Truth 帖子
        
        Args:
            username: 用户名，默认为 realDonaldTrump
            limit: 获取帖子数量
            
        Returns:
            帖子列表
        """
        try:
            # Truth Social API 端点
            url = f"{self.api_base}/accounts/{username}/statuses"
            params = {
                "limit": limit,
                "exclude_replies": "false",
                "exclude_reblogs": "false"
            }
            
            response = self.session.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_truths(data)
            else:
                print(f"请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text[:500]}")
                return []
                
        except Exception as e:
            print(f"获取数据时出错: {str(e)}")
            return []
    
    def _parse_truths(self, data: List[Dict]) -> List[Dict]:
        """解析 Truth 数据"""
        truths = []
        
        for item in data:
            try:
                truth = {
                    "id": item.get("id"),
                    "content": self._clean_content(item.get("content", "")),
                    "created_at": item.get("created_at"),
                    "replies_count": item.get("replies_count", 0),
                    "reblogs_count": item.get("reblogs_count", 0),
                    "favourites_count": item.get("favourites_count", 0),
                    "url": item.get("url"),
                    "media_attachments": [],
                }
                
                # 提取媒体附件
                if "media_attachments" in item:
                    for media in item["media_attachments"]:
                        truth["media_attachments"].append({
                            "type": media.get("type"),
                            "url": media.get("url"),
                            "preview_url": media.get("preview_url"),
                        })
                
                truths.append(truth)
                
            except Exception as e:
                print(f"解析单条 Truth 时出错: {str(e)}")
                continue
        
        return truths
    
    def _clean_content(self, content: str) -> str:
        """清理 HTML 内容"""
        if not content:
            return ""
        # 解码 HTML 实体
        content = html.unescape(content)
        # 移除 HTML 标签
        content = re.sub(r'<[^>]+>', '', content)
        return content.strip()
    
    def search_truths(self, query: str, limit: int = 20) -> List[Dict]:
        """
        搜索 Truth 内容
        
        Args:
            query: 搜索关键词
            limit: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        try:
            url = f"{self.api_base}/search"
            params = {
                "q": query,
                "limit": limit,
                "type": "statuses"
            }
            
            response = self.session.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_truths(data.get("statuses", []))
            else:
                print(f"搜索失败，状态码: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"搜索时出错: {str(e)}")
            return []
    
    def get_trending(self, limit: int = 20) -> List[Dict]:
        """
        获取热门 Truth
        
        Args:
            limit: 返回结果数量
            
        Returns:
            热门帖子列表
        """
        try:
            # 使用公共时间线获取热门内容
            url = f"{self.api_base}/timelines/public"
            params = {
                "limit": limit,
                "local": "false"
            }
            
            response = self.session.get(url, headers=self.headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_truths(data)
            else:
                print(f"获取热门内容失败，状态码: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"获取热门内容时出错: {str(e)}")
            return []
    
    def save_to_json(self, truths: List[Dict], filename: Optional[str] = None):
        """保存数据到 JSON 文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"truthsocial_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(truths, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {filename}")
    
    def save_to_markdown(self, truths: List[Dict], filename: Optional[str] = None):
        """保存数据到 Markdown 文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"truthsocial_data_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Truth Social 最新资讯\n\n")
            f.write(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"共 {len(truths)} 条内容\n\n")
            f.write("---\n\n")
            
            for i, truth in enumerate(truths, 1):
                f.write(f"## {i}. {truth.get('created_at', 'Unknown Date')}\n\n")
                f.write(f"**内容:**\n\n{truth.get('content', 'No content')}\n\n")
                f.write(f"- 🔗 链接: {truth.get('url', 'N/A')}\n")
                f.write(f"- 💬 回复: {truth.get('replies_count', 0)} | "
                       f"🔄 转发: {truth.get('reblogs_count', 0)} | "
                       f"❤️ 点赞: {truth.get('favourites_count', 0)}\n")
                
                if truth.get('media_attachments'):
                    f.write("- 📎 媒体附件:\n")
                    for media in truth['media_attachments']:
                        f.write(f"  - {media.get('type')}: {media.get('url')}\n")
                
                f.write("\n---\n\n")
        
        print(f"数据已保存到: {filename}")


def main():
    """主函数"""
    scraper = TruthSocialScraper()
    
    print("=" * 60)
    print("Truth Social 爬虫")
    print("=" * 60)
    
    # 1. 获取特朗普的最新帖子
    print("\n【1】获取 @realDonaldTrump 的最新帖子...")
    trump_truths = scraper.get_user_truths(username="realDonaldTrump", limit=10)
    
    if trump_truths:
        print(f"成功获取 {len(trump_truths)} 条帖子")
        for i, truth in enumerate(trump_truths[:3], 1):
            print(f"\n--- 帖子 {i} ---")
            print(f"时间: {truth.get('created_at')}")
            print(f"内容: {truth.get('content')[:200]}...")
            print(f"互动: 💬{truth.get('replies_count')} 🔄{truth.get('reblogs_count')} ❤️{truth.get('favourites_count')}")
    else:
        print("未能获取数据，可能是 API 限制或需要认证")
    
    # 2. 获取热门内容
    print("\n\n【2】获取热门 Truth...")
    trending = scraper.get_trending(limit=10)
    
    if trending:
        print(f"成功获取 {len(trending)} 条热门内容")
    else:
        print("未能获取热门内容")
    
    # 3. 搜索特定关键词
    print("\n\n【3】搜索关键词 'America'...")
    search_results = scraper.search_truths(query="America", limit=10)
    
    if search_results:
        print(f"成功获取 {len(search_results)} 条搜索结果")
    else:
        print("未能获取搜索结果")
    
    # 保存数据
    print("\n\n【4】保存数据...")
    if trump_truths:
        scraper.save_to_json(trump_truths, "trump_truths.json")
        scraper.save_to_markdown(trump_truths, "trump_truths.md")
    
    print("\n" + "=" * 60)
    print("爬虫执行完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
