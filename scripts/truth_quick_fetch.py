#!/usr/bin/env python3
"""
快速获取 Truth Social 最新 5 条资讯
"""

import requests
import json
import re
import html
from datetime import datetime

def get_latest_truths(limit=5):
    """获取特朗普最新 Truth 帖子"""
    
    base_url = "https://truthsocial.com/api/v1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        url = f"{base_url}/accounts/realDonaldTrump/statuses"
        params = {
            "limit": limit,
            "exclude_replies": "false",
            "exclude_reblogs": "false"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            truths = []
            
            for item in data:
                content = item.get("content", "")
                content = html.unescape(content)
                content = re.sub(r'<[^>]+>', '', content)
                
                truth = {
                    "时间": item.get("created_at", "Unknown"),
                    "内容": content.strip(),
                    "回复": item.get("replies_count", 0),
                    "转发": item.get("reblogs_count", 0),
                    "点赞": item.get("favourites_count", 0),
                    "链接": item.get("url", "N/A"),
                }
                truths.append(truth)
            
            return truths
        else:
            print(f"请求失败，状态码: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            return []
            
    except Exception as e:
        print(f"获取数据时出错: {str(e)}")
        return []

def main():
    print("=" * 70)
    print("Truth Social - @realDonaldTrump 最新 5 条资讯")
    print("=" * 70)
    print(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    truths = get_latest_truths(limit=5)
    
    if truths:
        for i, truth in enumerate(truths, 1):
            print(f"\n{'─' * 70}")
            print(f"【{i}】{truth['时间']}")
            print(f"{'─' * 70}")
            print(f"{truth['内容']}")
            print(f"\n💬 {truth['回复']} | 🔄 {truth['转发']} | ❤️ {truth['点赞']}")
            print(f"🔗 {truth['链接']}")
        
        # 保存到文件
        filename = f"trump_latest_5_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(truths, f, ensure_ascii=False, indent=2)
        print(f"\n{'=' * 70}")
        print(f"数据已保存到: {filename}")
    else:
        print("\n未能获取数据，可能是：")
        print("1. API 限制或需要认证")
        print("2. 网络连接问题")
        print("3. Truth Social 服务异常")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
