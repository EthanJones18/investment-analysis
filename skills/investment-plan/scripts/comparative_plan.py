#!/usr/bin/env python3
"""
投资计划对比分析脚本
对比多个标的投资计划，生成对比报告
"""

import argparse
import json
from datetime import datetime
from typing import List, Dict

def compare_plans(symbols: List[str], plans: List[Dict]) -> Dict:
    """
    对比多个标的投资计划
    """
    comparison = {
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbols": symbols,
        "comparison_summary": {},
        "rankings": {},
        "recommendations": {}
    }
    
    # 提取关键指标
    metrics = []
    for symbol, plan in zip(symbols, plans):
        metric = {
            "symbol": symbol,
            "risk_profile": plan.get("risk_profile", "neutral"),
            "risk_level": plan.get("risk_management", {}).get("risk_level", "中等"),
            "expected_return": plan.get("risk_management", {}).get("expected_return", ""),
            "max_drawdown": plan.get("risk_management", {}).get("max_drawdown", ""),
            "position_size": plan.get("trading_strategy", {}).get("position", {}).get("initial_size", ""),
            "stop_loss": plan.get("trading_strategy", {}).get("exit", {}).get("stop_loss", ""),
            "take_profit": plan.get("trading_strategy", {}).get("exit", {}).get("take_profit", ""),
            "recommendation": plan.get("summary", {}).get("recommendation", "")
        }
        metrics.append(metric)
    
    comparison["metrics"] = metrics
    
    # 生成对比表格
    comparison["comparison_table"] = {
        "headers": ["标的", "风险等级", "预期收益", "最大回撤", "建议仓位", "止损", "止盈", "建议"],
        "rows": [
            [
                m["symbol"],
                m["risk_level"],
                m["expected_return"],
                m["max_drawdown"],
                m["position_size"],
                m["stop_loss"],
                m["take_profit"],
                m["recommendation"]
            ]
            for m in metrics
        ]
    }
    
    # 排序和推荐
    # 这里简化处理，实际应该基于综合评分
    comparison["rankings"] = {
        "by_risk": sorted(metrics, key=lambda x: {"低": 1, "中等": 2, "高": 3}.get(x["risk_level"], 2)),
        "by_return": sorted(metrics, key=lambda x: x["expected_return"], reverse=True)
    }
    
    # 投资组合建议
    comparison["portfolio_recommendation"] = {
        "allocation_strategy": "根据风险偏好分散配置",
        "suggested_allocation": [
            {"symbol": symbols[0], "allocation": "40%", "reason": "主要配置"},
            {"symbol": symbols[1] if len(symbols) > 1 else symbols[0], "allocation": "35%", "reason": "次要配置"},
            {"symbol": symbols[2] if len(symbols) > 2 else symbols[0], "allocation": "25%", "reason": "补充配置"}
        ],
        "risk_management": {
            "total_exposure": "不超过账户80%",
            "hedge_strategy": "考虑使用期权保护",
            "rebalancing": "月度再平衡"
        }
    }
    
    return comparison

def generate_markdown_report(comparison: Dict, output_file: str):
    """生成Markdown对比报告"""
    
    report = f"""# 投资计划对比分析报告

**分析日期**: {comparison['analysis_date']}

**对比标的**: {', '.join(comparison['symbols'])}

---

## 1. 对比概览

| 标的 | 风险等级 | 预期收益 | 最大回撤 | 建议仓位 | 止损 | 止盈 | 建议 |
|------|---------|---------|---------|---------|------|------|------|
"""
    
    for row in comparison['comparison_table']['rows']:
        report += f"| {' | '.join(row)} |\n"
    
    report += """
---

## 2. 详细分析

"""
    
    for metric in comparison['metrics']:
        report += f"""### {metric['symbol']}

- **风险等级**: {metric['risk_level']}
- **预期收益**: {metric['expected_return']}
- **最大回撤**: {metric['max_drawdown']}
- **建议仓位**: {metric['position_size']}
- **止损设置**: {metric['stop_loss']}
- **止盈目标**: {metric['take_profit']}
- **投资建议**: {metric['recommendation']}

"""
    
    report += f"""
---

## 3. 投资组合建议

### 配置策略

{comparison['portfolio_recommendation']['allocation_strategy']}

### 建议配置比例

"""
    
    for alloc in comparison['portfolio_recommendation']['suggested_allocation']:
        report += f"- **{alloc['symbol']}**: {alloc['allocation']} - {alloc['reason']}\n"
    
    report += f"""
### 风险管理

- **总敞口**: {comparison['portfolio_recommendation']['risk_management']['total_exposure']}
- **对冲策略**: {comparison['portfolio_recommendation']['risk_management']['hedge_strategy']}
- **再平衡**: {comparison['portfolio_recommendation']['risk_management']['rebalancing']}

---

## 4. 风险提示

本对比分析基于各标的投资计划生成，不构成投资建议。
投资有风险，入市需谨慎。请根据自身风险承受能力做出投资决策。

---

*报告由投资计划对比分析系统自动生成*
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

def main():
    parser = argparse.ArgumentParser(description='投资计划对比分析')
    parser.add_argument('--symbols', required=True, help='股票代码，逗号分隔')
    parser.add_argument('--plan-files', help='计划文件路径，逗号分隔')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    symbols = [s.strip() for s in args.symbols.split(',')]
    
    print(f"投资计划对比分析")
    print(f"对比标的: {', '.join(symbols)}")
    print("-" * 50)
    
    # 加载计划文件
    plans = []
    if args.plan_files:
        files = [f.strip() for f in args.plan_files.split(',')]
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    plans.append(json.load(f))
            except:
                print(f"警告: 无法加载文件 {file}")
                plans.append({})
    else:
        # 生成默认计划
        from quick_plan import generate_quick_plan
        for symbol in symbols:
            plans.append(generate_quick_plan(symbol, 'neutral'))
    
    # 对比分析
    comparison = compare_plans(symbols, plans)
    
    import os
    os.makedirs(args.output, exist_ok=True)
    
    # 导出JSON
    json_file = f"{args.output}/comparison_{'_'.join(symbols)}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(comparison, f, ensure_ascii=False, indent=2)
    
    # 导出Markdown
    md_file = f"{args.output}/comparison_{'_'.join(symbols)}.md"
    generate_markdown_report(comparison, md_file)
    
    print("\n对比分析完成!")
    print(f"JSON: {json_file}")
    print(f"Markdown: {md_file}")
    
    print("\n对比摘要:")
    print("-" * 80)
    print(f"{'标的':<10} {'风险':<8} {'预期收益':<12} {'仓位':<10} {'建议':<10}")
    print("-" * 80)
    for m in comparison['metrics']:
        print(f"{m['symbol']:<10} {m['risk_level']:<8} {m['expected_return']:<12} {m['position_size']:<10} {m['recommendation']:<10}")

if __name__ == "__main__":
    main()
