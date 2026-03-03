#!/usr/bin/env python3
"""
快速投资计划生成脚本
基于风险偏好的快速投资计划生成
"""

import argparse
import json
from datetime import datetime

def generate_quick_plan(symbol: str, risk_profile: str) -> dict:
    """
    基于风险偏好的快速投资计划生成
    """
    
    # 根据风险偏好定义参数
    profiles = {
        "aggressive": {
            "position_size": "20-30%",
            "stop_loss": "-12%",
            "take_profit": "+50%以上",
            "entry_timing": "突破入场",
            "pyramiding": "激进金字塔",
            "risk_level": "高",
            "expected_return": "+50%以上",
            "max_drawdown": "30-50%"
        },
        "conservative": {
            "position_size": "5-10%",
            "stop_loss": "-7%",
            "take_profit": "+15%",
            "entry_timing": "回调入场",
            "pyramiding": "保守分批",
            "risk_level": "低",
            "expected_return": "+10%至+20%",
            "max_drawdown": "10-15%"
        },
        "neutral": {
            "position_size": "10-20%",
            "stop_loss": "-10%",
            "take_profit": "+30%",
            "entry_timing": "趋势确认后入场",
            "pyramiding": "标准金字塔",
            "risk_level": "中等",
            "expected_return": "+20%至+35%",
            "max_drawdown": "15-25%"
        }
    }
    
    profile = profiles.get(risk_profile, profiles["neutral"])
    
    plan = {
        "symbol": symbol,
        "plan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_profile": risk_profile,
        "quick_plan": True,
        
        "investment_thesis": {
            "core_logic": f"基于{risk_profile}风险偏好，{symbol}具备符合该风险偏好的投资机会。",
            "key_points": [
                "基本面分析支持投资逻辑",
                "技术面呈现有利形态",
                "风险收益比符合要求"
            ]
        },
        
        "trading_strategy": {
            "entry": {
                "timing": profile["entry_timing"],
                "conditions": [
                    "价格进入目标区间",
                    "技术形态确认",
                    "市场环境适宜"
                ]
            },
            "position": {
                "initial_size": profile["position_size"],
                "pyramiding": profile["pyramiding"],
                "max_size": profile["position_size"]
            },
            "exit": {
                "take_profit": profile["take_profit"],
                "stop_loss": profile["stop_loss"],
                "time_stop": "60天未达预期评估退出"
            }
        },
        
        "risk_management": {
            "risk_level": profile["risk_level"],
            "expected_return": profile["expected_return"],
            "max_drawdown": profile["max_drawdown"],
            "position_limits": {
                "single_stock": profile["position_size"],
                "risk_per_trade": "2%"
            }
        },
        
        "execution": {
            "immediate_actions": [
                "确认资金到位",
                "设置价格预警",
                "准备交易指令"
            ],
            "monitoring": [
                "每日价格监控",
                "新闻事件跟踪",
                "技术指标观察"
            ]
        },
        
        "summary": {
            "recommendation": "执行" if risk_profile != "aggressive" else "谨慎执行",
            "priority": "中",
            "next_steps": [
                "等待入场时机",
                "执行建仓计划",
                "设置止损止盈"
            ]
        }
    }
    
    return plan

def main():
    parser = argparse.ArgumentParser(description='快速生成投资计划')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--risk-profile', default='neutral', 
                       choices=['aggressive', 'conservative', 'neutral'],
                       help='风险偏好')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    print(f"快速生成投资计划: {args.symbol}")
    print(f"风险偏好: {args.risk_profile}")
    print("-" * 50)
    
    plan = generate_quick_plan(args.symbol, args.risk_profile)
    
    import os
    os.makedirs(args.output, exist_ok=True)
    
    output_file = f"{args.output}/{args.symbol}_quick_plan.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print("\n快速投资计划生成完成!")
    print(f"输出文件: {output_file}")
    
    print("\n计划摘要:")
    print(f"  风险偏好: {plan['risk_profile']}")
    print(f"  风险等级: {plan['risk_management']['risk_level']}")
    print(f"  预期收益: {plan['risk_management']['expected_return']}")
    print(f"  最大回撤: {plan['risk_management']['max_drawdown']}")
    print(f"  初始仓位: {plan['trading_strategy']['position']['initial_size']}")
    print(f"  止损设置: {plan['trading_strategy']['exit']['stop_loss']}")
    print(f"  止盈目标: {plan['trading_strategy']['exit']['take_profit']}")
    print(f"  建议: {plan['summary']['recommendation']}")

if __name__ == "__main__":
    main()
