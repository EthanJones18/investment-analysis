#!/usr/bin/env python3
"""
Binance 公告抓取脚本
抓取最新上线的合约交易对信息
"""

import requests
import json
import re
from datetime import datetime
from urllib.parse import urljoin

# Binance 公告中心 API
ANNOUNCEMENT_API = "https://www.binance.com/bapi/composite/v1/public/cms/article/catalog/list/query"

# 代理设置
PROXIES = {
    "http": "http://127.0.0.1:1081",
    "https": "http://127.0.0.1:1081"
}

# 合约相关关键词
FUTURES_KEYWORDS = [
    "perpetual", "futures", "contract", "USDT", "USDC", "USDS-M", "COIN-M"
]

def fetch_binance_announcements(category_id=48, page_no=1, page_size=20):
    """
    抓取 Binance 公告
    category_id: 48 是新币上线/合约公告分类
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    params = {
        "catalogId": category_id,
        "pageNo": page_no,
        "pageSize": page_size,
    }
    
    try:
        response = requests.get(
            ANNOUNCEMENT_API,
            headers=headers,
            params=params,
            proxies=PROXIES,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching announcements: {e}")
        return None

def extract_contract_info(title, content=None):
    """
    从标题和内容中提取合约信息
    """
    info = {
        "is_contract": False,
        "contract_type": None,
        "trading_pairs": [],
        "launch_date": None,
        "leverage": None
    }
    
    # 检查是否是合约相关公告
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in ["perpetual", "futures", "contract"]):
        info["is_contract"] = True
        
        # 判断合约类型
        if "usds-m" in title_lower or "usdⓈ-m" in title_lower:
            info["contract_type"] = "USDS-M Perpetual"
        elif "coin-m" in title_lower:
            info["contract_type"] = "COIN-M Perpetual"
        elif "usdt" in title_lower:
            info["contract_type"] = "USDT Perpetual"
        elif "usdc" in title_lower:
            info["contract_type"] = "USDC Perpetual"
        else:
            info["contract_type"] = "Perpetual"
    
    # 提取交易对（匹配类似 BTCUSDT, ETHUSDT 的格式）
    pair_pattern = r'\b([A-Z]{2,})(USDT|USDC|BUSD)\b'
    pairs = re.findall(pair_pattern, title)
    info["trading_pairs"] = [f"{p[0]}{p[1]}" for p in pairs]
    
    # 提取杠杆倍数
    leverage_match = re.search(r'(\d+)x', title)
    if leverage_match:
        info["leverage"] = f"{leverage_match.group(1)}x"
    
    return info

def format_date(timestamp):
    """格式化时间戳"""
    if not timestamp:
        return "Unknown"
    try:
        # Binance 时间戳是毫秒
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except:
        return str(timestamp)

def main():
    print("=" * 60)
    print("📊 Binance 最新合约上线公告")
    print("=" * 60)
    print()
    
    data = fetch_binance_announcements(page_size=30)
    
    if not data or data.get("code") != "000000":
        print("❌ 获取公告失败")
        return
    
    articles = data.get("data", {}).get("articles", [])
    
    if not articles:
        print("❌ 没有找到公告")
        return
    
    contract_count = 0
    
    for article in articles:
        title = article.get("title", "")
        code = article.get("code", "")
        release_date = article.get("releaseDate", 0)
        
        # 提取合约信息
        info = extract_contract_info(title)
        
        if info["is_contract"]:
            contract_count += 1
            print(f"📌 {title}")
            print(f"   类型: {info['contract_type']}")
            if info["trading_pairs"]:
                print(f"   交易对: {', '.join(info['trading_pairs'])}")
            if info["leverage"]:
                print(f"   杠杆: {info['leverage']}")
            print(f"   时间: {format_date(release_date)}")
            print(f"   链接: https://www.binance.com/en/support/announcement/detail/{code}")
            print("-" * 60)
    
    if contract_count == 0:
        print("⚠️ 最近30条公告中没有找到合约上线信息")
    else:
        print(f"\n✅ 共找到 {contract_count} 条合约相关公告")

if __name__ == "__main__":
    main()
