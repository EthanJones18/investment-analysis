#!/usr/bin/env python3
"""
激进型风险分析脚本
"""

import argparse
import json
from datetime import datetime

def analyze_aggressive(symbol: str) -> dict:
    """
    激进型风险分析
    追求高风险高收益，愿意承担较大波动换取超额回报
    """
    analysis = {
        "symbol": symbol,
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "risk_profile": "aggressive",
        "risk_parameters": {
            "max_drawdown_tolerance": "30-50%",
            "stop_loss": "-10%至-15%",
            "target_return": "+50%以上",
            "max_position_size": "30%",
            "cash_reserve": "20%"
        },
        "analysis_framework": {
            "upside_potential": {
                "weight": 0.30,
                "factors": [
                    "营收增长率 >30%",
                    "净利润增长率 >40%",
                    "市场份额持续提升",
                    "TAM扩张机会",
                    "突破性产品创新"
                ]
            },
            "momentum": {
                "weight": 0.25,
                "indicators": [
                    "RSI(14) 50-70区间向上突破",
                    "MACD金叉且柱状线扩大",
                    "股价站上所有均线",
                    "成交量放量上涨",
                    "突破前期高点"
                ]
            },
            "beta": {
                "weight": 0.15,
                "preference": ">1.5",
                "rationale": "高弹性，市场上涨时涨幅更大"
            },
            "liquidity": {
                "weight": 0.10,
                "requirements": [
                    "日均成交量充足",
                    "买卖价差小",
                    "大宗交易不影响价格"
                ]
            },
            "catalysts": {
                "weight": 0.15,
                "events": [
                    "业绩超预期",
                    "重大合同签订",
                    "技术突破",
                    "政策支持",
                    "并购重组",
                    "重磅产品发布"
                ]
            },
            "valuation": {
                "weight": 0.05,
                "note": "激进策略对估值容忍度较高"
            }
        },
        "risk_management": {
            "stop_loss": {
                "initial": "-10%至-15%",
                "time_based": "30天未达预期减半",
                "trailing": {
                    "profit_20%": "止损上移至成本价",
                    "profit_30%": "止损上移至盈利10%",
                    "profit_50%": "止损上移至盈利25%"
                }
            },
            "position_sizing": {
                "pyramiding": [
                    {"order": 1, "size": "30%", "trigger": "达到入场条件"},
                    {"order": 2, "size": "20%", "trigger": "盈利10%后"},
                    {"order": 3, "size": "15%", "trigger": "盈利20%后"},
                    {"order": 4, "size": "10%", "trigger": "盈利30%后"}
                ]
            },
            "risk_budget": {
                "single_position": "不超过账户5%",
                "single_industry": "不超过账户20%",
                "total_risk": "不超过账户30%"
            }
        },
        "scoring_criteria": {
            "90-100": {"rating": "强烈推荐", "action": "重仓配置20-30%"},
            "80-89": {"rating": "推荐", "action": "积极配置15-20%"},
            "70-79": {"rating": "中性偏多", "action": "适度配置10-15%"},
            "60-69": {"rating": "中性", "action": "观望或轻仓5%"},
            "<60": {"rating": "回避", "action": "不建议参与"}
        },
        "key_factors": [
            "高Beta值，市场上涨时弹性大",
            "催化剂事件密集，短期爆发力强",
            "机构持仓增加，资金关注度高",
            "技术形态突破，动量强劲"
        ],
        "warnings": [
            "波动率较高，需严格止损",
            "流动性风险需关注",
            "估值偏高，依赖情绪推动"
        ]
    }
    return analysis

def main():
    parser = argparse.ArgumentParser(description='激进型风险分析')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    print(f"开始激进型风险分析: {args.symbol}")
    
    result = analyze_aggressive(args.symbol)
    
    output_file = f"{args.output}/{args.symbol}_aggressive.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n激进型分析完成！")
    print(f"报告已保存至: {output_file}")
    print(f"\n风险偏好参数:")
    print(f"  最大回撤容忍: {result['risk_parameters']['max_drawdown_tolerance']}")
    print(f"  止损设置: {result['risk_parameters']['stop_loss']}")
    print(f"  目标收益: {result['risk_parameters']['target_return']}")
    print(f"  最大仓位: {result['risk_parameters']['max_position_size']}")

if __name__ == "__main__":
    main()
