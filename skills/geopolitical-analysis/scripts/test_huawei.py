#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
import requests

class GDELTClient:
    GDELT_API = "https://api.gdeltproject.org/api/v2"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_events(self, countries=None, days=7):
        events = []
        try:
            start_date = datetime.now() - timedelta(days=days)
            end_date = datetime.now()
            query = "huawei OR huawei sanctions OR china tech OR china us trade"
            if countries:
                country_query = " OR ".join([f"country:{c}" for c in countries])
                query = f"({query}) AND ({country_query})"
            params = {
                "query": query, "mode": "ArtList", "maxrecords": 100,
                "format": "json",
                "startdatetime": start_date.strftime("%Y%m%d%H%M%S"),
                "enddatetime": end_date.strftime("%Y%m%d%H%M%S")
            }
            response = self.session.get(f"{self.GDELT_API}/doc/doc", params=params, timeout=30)
            if response.status_code == 200:
                events = self._parse_response(response.json())
        except Exception as e:
            print(f"  GDELT错误: {e}")
        return events
    
    def _parse_response(self, data):
        events = []
        for article in data.get("articles", []):
            try:
                events.append({
                    "title": article.get("title", "Unknown"),
                    "source": article.get("domain", "Unknown"),
                    "event_type": self._classify_type(article),
                    "severity": self._assess_severity(article)
                })
            except Exception:
                continue
        return events
    
    def _classify_type(self, article):
        title = article.get("title", "").lower()
        if any(kw in title for kw in ["sanction", "ban", "blacklist"]):
            return "sanction"
        elif any(kw in title for kw in ["trade", "tariff"]):
            return "trade"
        elif any(kw in title for kw in ["cyber", "security"]):
            return "cyber"
        elif any(kw in title for kw in ["tech", "5g", "chip"]):
            return "tech"
        return "other"
    
    def _assess_severity(self, article):
        title = article.get("title", "").lower()
        if any(kw in title for kw in ["ban", "sanction", "blacklist"]):
            return "CRITICAL"
        elif any(kw in title for kw in ["restrict", "probe"]):
            return "HIGH"
        return "MEDIUM"

def main():
    print("\n" + "=" * 70)
    print("地缘政治分析报告 - 华为 (HUAWEI)")
    print("=" * 70)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n【资产地缘政治暴露】")
    print("  公司: 华为技术有限公司")
    print("  总部: 中国深圳")
    print("  核心暴露:")
    print("    • 中美科技竞争核心标的")
    print("    • 5G/芯片/半导体供应链")
    print("    • 美国实体清单制裁对象")
    
    print("\n【获取地缘政治事件...】")
    client = GDELTClient()
    events = client.fetch_events(countries=["USA", "CHN"], days=30)
    
    print(f"  获取到 {len(events)} 条相关事件")
    
    critical = sum(1 for e in events if e["severity"] == "CRITICAL")
    high = sum(1 for e in events if e["severity"] == "HIGH")
    medium = sum(1 for e in events if e["severity"] == "MEDIUM")
    
    print(f"\n  严重程度: CRITICAL={critical}, HIGH={high}, MEDIUM={medium}")
    
    print("\n  关键事件:")
    for i, e in enumerate([e for e in events if e["severity"] in ["CRITICAL", "HIGH"]][:5], 1):
        print(f"    {i}. [{e['severity']}] {e['title'][:55]}...")
    
    risk_score = (critical * 1.0 + high * 0.6 + medium * 0.3) / max(len(events), 1)
    print(f"\n  风险分数: {risk_score:.2f}")
    
    if risk_score >= 0.7:
        risk_level = "🔴 CRITICAL"
    elif risk_score >= 0.4:
        risk_level = "🟠 HIGH"
    elif risk_score >= 0.2:
        risk_level = "🟡 MEDIUM"
    else:
        risk_level = "🟢 LOW"
    print(f"  风险级别: {risk_level}")
    
    print("\n【情景分析】")
    print("  基准情景 (50%): 现有制裁维持，业务持续承压")
    print("  悲观情景 (30%): 制裁升级，更多国家加入禁令")
    print("  极端情景 (10%): 台海冲突，华为被完全孤立")
    print("  乐观情景 (10%): 中美关系缓和，部分制裁解除")
    
    print("\n【投资建议】")
    print("  🔴 紧急: 地缘政治风险极高，建议立即避险")
    print("  📊 监控: 持续跟踪中美科技政策变化")
    print("  🛡️ 对冲: 配置非中美科技供应链相关资产")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
