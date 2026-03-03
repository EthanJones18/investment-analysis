#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地缘政治事件监控与预警系统
实时监控全球地缘政治事件，评估对资产价格的潜在影响
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional
import requests


class EventSeverity(Enum):
    """事件严重程度"""
    CRITICAL = 5    # 战争、重大冲突
    HIGH = 4        # 制裁、军事对峙
    MEDIUM = 3      # 外交紧张、抗议
    LOW = 2         # 政策变化、谈判
    INFO = 1        # 一般新闻


class EventType(Enum):
    """事件类型"""
    CONFLICT = "conflict"
    SANCTION = "sanction"
    DIPLOMATIC = "diplomatic"
    ECONOMIC = "economic"
    TERRORISM = "terrorism"
    CYBER = "cyber"
    TRADE = "trade"
    ELECTION = "election"
    OTHER = "other"


@dataclass
class GeopoliticalEvent:
    """地缘政治事件"""
    id: str
    timestamp: datetime
    title: str
    description: str
    event_type: EventType
    severity: EventSeverity
    countries: List[str]
    regions: List[str]
    source: str
    url: Optional[str] = None
    
    def to_dict(self):
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['event_type'] = self.event_type.value
        data['severity'] = self.severity.name
        return data


class GDELTClient:
    """GDELT数据源客户端"""
    
    GDELT_API = "https://api.gdeltproject.org/api/v2"
    
    def __init__(self):
        self.session = requests.Session()
    
    def fetch_events(self, countries: List[str] = None, days: int = 7) -> List[GeopoliticalEvent]:
        """从GDELT获取事件数据"""
        events = []
        
        try:
            start_date = datetime.now() - timedelta(days=days)
            end_date = datetime.now()
            
            params = {
                "query": "*" if not countries else " OR ".join([f"country:{c}" for c in countries]),
                "mode": "ArtList",
                "maxrecords": 250,
                "format": "json",
                "startdatetime": start_date.strftime("%Y%m%d%H%M%S"),
                "enddatetime": end_date.strftime("%Y%m%d%H%M%S")
            }
            
            response = self.session.get(
                f"{self.GDELT_API}/doc/doc",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                events = self._parse_response(data)
            
        except Exception as e:
            print(f"GDELT API error: {e}")
        
        return events
    
    def _parse_response(self, data: dict) -> List[GeopoliticalEvent]:
        """解析GDELT响应"""
        events = []
        
        for article in data.get("articles", []):
            try:
                event = GeopoliticalEvent(
                    id=article.get("url", "")[-50:],
                    timestamp=datetime.strptime(
                        article.get("seendate", datetime.now().isoformat()),
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                    title=article.get("title", "Unknown"),
                    description=article.get("title", ""),
                    event_type=self._classify_type(article),
                    severity=self._assess_severity(article),
                    countries=[],
                    regions=[],
                    source=article.get("domain", "Unknown"),
                    url=article.get("url")
                )
                events.append(event)
            except Exception:
                continue
        
        return events
    
    def _classify_type(self, article: dict) -> EventType:
        """分类事件类型"""
        title = article.get("title", "").lower()
        
        if any(kw in title for kw in ["war", "attack", "military", "strike", "bomb"]):
            return EventType.CONFLICT
        elif any(kw in title for kw in ["sanction", "embargo", "ban"]):
            return EventType.SANCTION
        elif any(kw in title for kw in ["trade", "tariff", "wto"]):
            return EventType.TRADE
        elif any(kw in title for kw in ["cyber", "hack", "breach"]):
            return EventType.CYBER
        elif any(kw in title for kw in ["terror", "extremist"]):
            return EventType.TERRORISM
        elif any(kw in title for kw in ["election", "vote", "political"]):
            return EventType.ELECTION
        else:
            return EventType.OTHER
    
    def _assess_severity(self, article: dict) -> EventSeverity:
        """评估严重程度"""
        title = article.get("title", "").lower()
        
        critical_keywords = ["war", "invasion", "attack", "missile", "nuclear"]
        if any(kw in title for kw in critical_keywords):
            return EventSeverity.CRITICAL
        
        high_keywords = ["sanction", "embargo", "crisis", "conflict"]
        if any(kw in title for kw in high_keywords):
            return EventSeverity.HIGH
        
        return EventSeverity.MEDIUM


def main():
    parser = argparse.ArgumentParser(description='地缘政治事件监控')
    parser.add_argument('--countries', help='监控国家代码，逗号分隔')
    parser.add_argument('--days', type=int, default=7, help='监控天数')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    countries = args.countries.split(',') if args.countries else None
    
    client = GDELTClient()
    events = client.fetch_events(countries=countries, days=args.days)
    
    print(f"获取到 {len(events)} 条事件")
    
    # 保存结果
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'geopolitical_events.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([e.to_dict() for e in events], f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存: {output_file}")


if __name__ == '__main__':
    main()
