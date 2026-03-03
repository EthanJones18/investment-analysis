#!/usr/bin/env python3
"""
宏观数据检索脚本
用于检索和整理主要经济体的关键宏观数据
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

def get_default_focus_areas() -> List[str]:
    """返回默认关注领域"""
    return [
        "货币政策",
        "通胀数据",
        "就业数据",
        "GDP增长",
        "贸易数据",
        "财政政策"
    ]

def get_data_sources() -> Dict[str, Dict]:
    """返回主要数据源信息"""
    return {
        "美国": {
            "央行": "美联储 (Federal Reserve)",
            "关键指标": [
                "非农就业数据 (NFP)",
                "CPI/PCE通胀",
                "GDP增长率",
                "联邦基金利率",
                "PMI指数"
            ],
            "发布机构": "劳工统计局(BLS)、经济分析局(BEA)"
        },
        "中国": {
            "央行": "中国人民银行 (PBOC)",
            "关键指标": [
                "GDP增长率",
                "CPI/PPI",
                "PMI指数",
                "社会融资规模",
                "LPR利率",
                "外汇储备"
            ],
            "发布机构": "国家统计局、人民银行"
        },
        "欧元区": {
            "央行": "欧洲央行 (ECB)",
            "关键指标": [
                "GDP增长率",
                "HICP通胀",
                "失业率",
                "主要再融资利率",
                "PMI指数"
            ],
            "发布机构": "欧盟统计局、欧洲央行"
        },
        "日本": {
            "央行": "日本央行 (BOJ)",
            "关键指标": [
                "GDP增长率",
                "CPI通胀",
                "政策利率",
                "失业率"
            ],
            "发布机构": "日本总务省统计局、日本央行"
        }
    }

def get_calendar_reminders() -> List[Dict]:
    """返回重要经济数据发布日程提醒"""
    today = datetime.now()
    
    # 这里可以添加固定的数据发布日程
    # 实际使用时可以结合外部日历API
    reminders = [
        {
            "event": "美联储议息会议",
            "frequency": "每6-8周",
            "importance": "高",
            "market_impact": "利率决策、政策声明、经济预测"
        },
        {
            "event": "美国非农就业报告",
            "frequency": "每月第一个周五",
            "importance": "高",
            "market_impact": "就业市场状况、美联储政策预期"
        },
        {
            "event": "美国CPI数据",
            "frequency": "每月中旬",
            "importance": "高",
            "market_impact": "通胀水平、实际利率"
        },
        {
            "event": "中国PMI数据",
            "frequency": "每月最后一天",
            "importance": "中高",
            "market_impact": "制造业活动、经济景气度"
        },
        {
            "event": "中国LPR报价",
            "frequency": "每月20日",
            "importance": "中高",
            "market_impact": "贷款利率、货币政策取向"
        }
    ]
    return reminders

def main():
    """主函数 - 输出宏观数据检索指南"""
    
    output = {
        "meta": {
            "script": "macro_data_guide",
            "version": "1.0",
            "generated_at": datetime.now().isoformat()
        },
        "default_focus_areas": get_default_focus_areas(),
        "data_sources": get_data_sources(),
        "calendar_reminders": get_calendar_reminders(),
        "search_keywords": {
            "货币政策": ["利率", "央行", "QE", "量化宽松", "加息", "降息", "缩表"],
            "通胀": ["CPI", "PPI", "通胀率", "物价", "核心通胀"],
            "就业": ["非农就业", "失业率", "劳动力市场", "工资增长"],
            "增长": ["GDP", "经济增长", "PMI", "制造业", "服务业"],
            "贸易": ["贸易顺差", "贸易逆差", "关税", "汇率", "进出口"],
            "财政": ["财政政策", "政府支出", "赤字", "债务", "基建"]
        }
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
