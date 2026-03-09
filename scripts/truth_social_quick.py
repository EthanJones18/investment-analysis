#!/usr/bin/env python3
"""
快速获取 Truth Social 最新5条资讯
"""

import requests
import json
import re
import html
from datetime import datetime

def get_latest_truths(username="realDonaldTrump", limit=5):
    """获取最新 Truth 帖子"""
    
    base_url = "https://truthsocial.com/api/v1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        url = f"{base_url}/accounts/{username}/statuses"
        params = {
            "limit": limit,
            "exclude_replies": "false",
            "exclude_reblogs": "false"
        }
        
        print(f"正在获取 @{username} 的最新 {limit} 条帖子...")
        print("-" * 60)
        
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if not data:
                print("未获取到数据")
                return []
            
            truths = []
            for i, item in enumerate(data, 1):
                # 清理内容
                content = item.get("content", "")
                content = html.unescape(content)
                content = re.sub(r'<[^>]+>', '', content)
                
                truth = {
                    "序号": i,
                    "时间": item.get("created_at", "Unknown"),
                    "内容": content[:300] + "..." if len(content) > 300 else content,
                    "回复": item.get("replies_count", 0),
                    "转发": item.get("reblogs_count", 0),
                    "点赞": item.get("favourites_count", 0),
                    "链接": item.get("url", "N/A"),
                }
                truths.append(truth)
                
                # 打印输出
                print(f"\n【{i}】{truth['时间']}")
                print(f"内容: {truth['内容']}")
                print(f"互动: 💬{truth['回复']} | 🔄{truth['转发']} | ❤️{truth['点赞']}")
                print(f"链接: {truth['链接']}")
                print("-" * 60)
            
            # 保存到文件
            filename = f"truthsocial_latest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(truths, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 数据已保存到: {filename}")
            
            return truths
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            return []
            
    except Exception as e:
        print(f"❌ 出错: {str(e)}")
        return []

if __name__ == "__main__":
    print("=" * 60)
    print("Truth Social 最新资讯获取")
    print("=" * 60)
    get_latest_truths("realDonaldTrump", 5)
    print("=" * 60)
