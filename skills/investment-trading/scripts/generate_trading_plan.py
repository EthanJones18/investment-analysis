#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易计划生成脚本
根据投资决策制定详细的交易计划

使用方法:
    python generate_trading_plan.py --symbol BABA --account-size 100000 --risk-per-trade 0.02
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class EntryPlan:
    """入场计划"""
    entry_price: float
    entry_range: Tuple[float, float]
    entry_conditions: List[str]
    initial_position: int
    initial_capital: float


@dataclass
class ExitPlan:
    """出场计划"""
    stop_loss: float
    take_profit_1: float  # 第一目标位
    take_profit_2: float  # 第二目标位
    take_profit_3: float  # 第三目标位
    trailing_stop: bool
    time_stop: int  # 天数


@dataclass
class PositionPlan:
    """仓位计划"""
    total_position: int
    initial_entry: int
    add_position_1: int
    add_position_2: int
    add_trigger_1: float  # 加仓触发涨幅
    add_trigger_2: float
    risk_amount: float
    risk_percent: float


@dataclass
class RiskControl:
    """风险控制"""
    max_loss_per_trade: float
    max_loss_per_day: float
    max_drawdown: float
    position_limit: float
    emergency_exit: List[str]


@dataclass
class TradingPlan:
    """交易计划"""
    symbol: str
    plan_date: str
    decision_rating: str
    decision_score: float
    
    # 交易方向
    direction: str  # LONG/SHORT
    
    # 入场计划
    entry_plan: EntryPlan
    
    # 出场计划
    exit_plan: ExitPlan
    
    # 仓位计划
    position_plan: PositionPlan
    
    # 风险控制
    risk_control: RiskControl
    
    # 执行检查清单
    pre_trade_checklist: List[str]
    post_trade_checklist: List[str]
    
    # 交易日志模板
    journal_template: str
    
    # 心理管理提示
    psychology_tips: List[str]


class TradingPlanGenerator:
    """交易计划生成器"""
    
    # 模拟投资决策数据
    MOCK_DECISIONS = {
        "BABA": {
            "overall_score": 63.2,
            "investment_rating": "持有",
            "recommendation": "建议持有，观望",
            "position_size": "5-10%",
            "stop_loss": "-5%",
            "target_return": "+15%",
            "current_price": 85.50,
            "support_levels": [80.00, 75.00, 70.00],
            "resistance_levels": [95.00, 100.00, 110.00]
        },
        "NVDA": {
            "overall_score": 76.8,
            "investment_rating": "增持",
            "recommendation": "建议增持，适度配置",
            "position_size": "10-15%",
            "stop_loss": "-6%",
            "target_return": "+20%",
            "current_price": 875.00,
            "support_levels": [820.00, 780.00, 750.00],
            "resistance_levels": [950.00, 1000.00, 1100.00]
        },
        "TSLA": {
            "overall_score": 62.7,
            "investment_rating": "持有",
            "recommendation": "建议持有，观望",
            "position_size": "5-10%",
            "stop_loss": "-5%",
            "target_return": "+15%",
            "current_price": 175.00,
            "support_levels": [165.00, 155.00, 145.00],
            "resistance_levels": [190.00, 200.00, 220.00]
        }
    }
    
    def __init__(self, symbol: str, account_size: float, risk_per_trade: float,
                 output_dir: str = "./output"):
        self.symbol = symbol
        self.account_size = account_size
        self.risk_per_trade = risk_per_trade
        self.output_dir = output_dir
        
        # 获取投资决策数据
        self.decision = self.MOCK_DECISIONS.get(symbol, self.MOCK_DECISIONS["BABA"])
    
    def generate_plan(self) -> TradingPlan:
        """生成交易计划"""
        print(f"\n{'='*70}")
        print(f"交易计划生成 - {self.symbol}")
        print(f"{'='*70}")
        print(f"计划日期: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"账户规模: ${self.account_size:,.2f}")
        print(f"单笔风险: {self.risk_per_trade*100:.1f}%")
        
        # 生成各部分计划
        entry_plan = self._generate_entry_plan()
        exit_plan = self._generate_exit_plan()
        position_plan = self._generate_position_plan()
        risk_control = self._generate_risk_control()
        
        # 构建完整计划
        plan = TradingPlan(
            symbol=self.symbol,
            plan_date=datetime.now().isoformat(),
            decision_rating=self.decision["investment_rating"],
            decision_score=self.decision["overall_score"],
            direction="LONG",
            entry_plan=entry_plan,
            exit_plan=exit_plan,
            position_plan=position_plan,
            risk_control=risk_control,
            pre_trade_checklist=self._generate_pre_trade_checklist(),
            post_trade_checklist=self._generate_post_trade_checklist(),
            journal_template=self._generate_journal_template(),
            psychology_tips=self._generate_psychology_tips()
        )
        
        return plan
    
    def _generate_entry_plan(self) -> EntryPlan:
        """生成入场计划"""
        current_price = self.decision["current_price"]
        
        # 根据投资决策评分确定入场策略
        score = self.decision["overall_score"]
        
        if score >= 80:
            # 强烈买入 - 积极入场
            entry_range = (current_price * 0.98, current_price * 1.02)
            conditions = [
                "价格回调至5日均线附近",
                "成交量配合放大",
                "技术指标未超买(RSI < 70)",
                "市场情绪稳定"
            ]
        elif score >= 70:
            # 增持 - 分批入场
            entry_range = (current_price * 0.95, current_price)
            conditions = [
                "价格回调至支撑位附近",
                "出现企稳信号(如锤子线)",
                "成交量萎缩后放量",
                "大盘环境配合"
            ]
        elif score >= 60:
            # 持有/观望 - 谨慎入场
            entry_range = (current_price * 0.92, current_price * 0.97)
            conditions = [
                "价格跌至强支撑位",
                "出现明显反弹信号",
                "技术指标超卖(RSI < 30)",
                "负面消息已充分消化"
            ]
        else:
            # 不建议入场
            entry_range = (current_price * 0.90, current_price * 0.95)
            conditions = [
                "等待趋势明朗",
                "出现底部形态确认",
                "基本面出现改善信号",
                "市场情绪转暖"
            ]
        
        # 计算初始仓位
        risk_amount = self.account_size * self.risk_per_trade
        stop_loss_pct = abs(float(self.decision["stop_loss"].replace("%", ""))) / 100
        stop_price = current_price * (1 - stop_loss_pct)
        
        risk_per_share = current_price - stop_price
        initial_shares = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
        initial_capital = initial_shares * current_price
        
        return EntryPlan(
            entry_price=current_price,
            entry_range=entry_range,
            entry_conditions=conditions,
            initial_position=initial_shares,
            initial_capital=initial_capital
        )
    
    def _generate_exit_plan(self) -> ExitPlan:
        """生成出场计划"""
        current_price = self.decision["current_price"]
        target_return = float(self.decision["target_return"].replace("%", "")) / 100
        stop_loss_pct = abs(float(self.decision["stop_loss"].replace("%", ""))) / 100
        
        # 止损位
        stop_loss = current_price * (1 - stop_loss_pct)
        
        # 分批止盈目标
        take_profit_1 = current_price * (1 + target_return * 0.5)  # 50%目标
        take_profit_2 = current_price * (1 + target_return * 0.8)  # 80%目标
        take_profit_3 = current_price * (1 + target_return)        # 100%目标
        
        return ExitPlan(
            stop_loss=round(stop_loss, 2),
            take_profit_1=round(take_profit_1, 2),
            take_profit_2=round(take_profit_2, 2),
            take_profit_3=round(take_profit_3, 2),
            trailing_stop=True,
            time_stop=90  # 90天
        )
    
    def _generate_position_plan(self) -> PositionPlan:
        """生成仓位计划"""
        current_price = self.decision["current_price"]
        risk_amount = self.account_size * self.risk_per_trade
        
        stop_loss_pct = abs(float(self.decision["stop_loss"].replace("%", ""))) / 100
        stop_price = current_price * (1 - stop_loss_pct)
        risk_per_share = current_price - stop_price
        
        # 总仓位
        total_shares = int(risk_amount / risk_per_share) if risk_per_share > 0 else 0
        
        # 金字塔加仓
        initial_entry = int(total_shares * 0.4)  # 40%首次
        add_position_1 = int(total_shares * 0.3)  # 30%第二次
        add_position_2 = int(total_shares * 0.2)  # 20%第三次
        # 剩余10%作为机动
        
        return PositionPlan(
            total_position=total_shares,
            initial_entry=initial_entry,
            add_position_1=add_position_1,
            add_position_2=add_position_2,
            add_trigger_1=0.05,  # 盈利5%后加仓
            add_trigger_2=0.10,  # 盈利10%后加仓
            risk_amount=risk_amount,
            risk_percent=self.risk_per_trade * 100
        )
    
    def _generate_risk_control(self) -> RiskControl:
        """生成风险控制"""
        return RiskControl(
            max_loss_per_trade=self.account_size * self.risk_per_trade,
            max_loss_per_day=self.account_size * 0.05,  # 单日5%
            max_drawdown=self.account_size * 0.20,      # 最大回撤20%
            position_limit=self.account_size * 0.20,    # 单一标的20%
            emergency_exit=[
                "股价单日暴跌超过10%",
                "公司发布重大负面消息",
                "行业政策突然变化",
                "大盘系统性风险",
                "自身情绪失控"
            ]
        )
    
    def _generate_pre_trade_checklist(self) -> List[str]:
        """生成交易前检查清单"""
        return [
            "□ 投资决策已确认并理解",
            "□ 交易计划已制定并记录",
            "□ 风险预算已计算并可以接受",
            "□ 入场条件已明确",
            "□ 止损位已确定并设置",
            "□ 止盈目标已设定",
            "□ 仓位大小已计算合理",
            "□ 资金已到位可用",
            "□ 情绪稳定，无冲动交易倾向",
            "□ 市场环境与预期一致"
        ]
    
    def _generate_post_trade_checklist(self) -> List[str]:
        """生成交易后检查清单"""
        return [
            "□ 实际入场价与计划对比",
            "□ 实际仓位与计划对比",
            "□ 止损单已正确设置",
            "□ 交易信息已记录到日志",
            "□ 持仓状态已更新",
            "□ 下一步操作计划已准备",
            "□ 情绪状态已记录",
            "□ 计划执行度已评估"
        ]
    
    def _generate_journal_template(self) -> str:
        """生成交易日志模板"""
        return f"""
{'='*60}
交易日志 - {self.symbol}
{'='*60}

【基本信息】
交易日期: {{trade_date}}
交易标的: {self.symbol}
交易方向: 买入/卖出

【交易计划回顾】
计划入场价: {{planned_entry}}
计划止损价: {{planned_stop}}
计划止盈价: {{planned_target}}
计划仓位: {{planned_position}}

【实际执行】
实际入场价: {{actual_entry}}
实际仓位: {{actual_position}}
入场理由: {{entry_reason}}

【持仓管理】
止损调整记录:
  - 初始止损: {{initial_stop}}
  - 调整后1: {{adjusted_stop_1}}
  - 调整后2: {{adjusted_stop_2}}

加仓记录:
  - 加仓1: {{add_1_price}} @ {{add_1_shares}}
  - 加仓2: {{add_2_price}} @ {{add_2_shares}}

【交易结果】
出场价格: {{exit_price}}
出场原因: {{exit_reason}}
盈亏金额: {{pnl_amount}}
盈亏比例: {{pnl_percent}}
持仓时间: {{holding_days}}天

【复盘总结】
计划执行度: {{execution_score}}/10
情绪状态: {{emotional_state}}
做得好的: {{what_went_well}}
需要改进: {{what_to_improve}}
经验教训: {{lessons_learned}}

【后续行动】
下一步计划: {{next_steps}}
{'='*60}
"""
    
    def _generate_psychology_tips(self) -> List[str]:
        """生成心理管理提示"""
        return [
            "交易前深呼吸，确保情绪稳定",
            "严格按照计划执行，不临时改变策略",
            "接受亏损是交易的一部分，不要试图报复市场",
            "盈利时保持谦逊，亏损时保持冷静",
            "不要过度关注单笔交易，关注长期表现",
            "定期休息，避免过度交易",
            "记录情绪状态，识别自己的心理陷阱",
            "连续亏损3笔后强制停止交易",
            "盈利超过目标后不要贪婪，按计划止盈",
            "市场永远有机会，保护本金是第一要务"
        ]
    
    def save_plan(self, plan: TradingPlan):
        """保存交易计划"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(
            self.output_dir,
            f"{self.symbol}_trading_plan.json"
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(plan), f, ensure_ascii=False, indent=2)
        
        print(f"\n交易计划已保存: {output_file}")
        return output_file
    
    def print_plan(self, plan: TradingPlan):
        """打印交易计划"""
        print(f"\n{'='*70}")
        print("交易执行计划书")
        print(f"{'='*70}")
        
        # 基本信息
        print(f"\n【基本信息】")
        print(f"  标的代码: {plan.symbol}")
        print(f"  计划日期: {plan.plan_date}")
        print(f"  投资评级: {plan.decision_rating} ({plan.decision_score}分)")
        print(f"  交易方向: {'买入做多' if plan.direction == 'LONG' else '卖出做空'}")
        
        # 入场计划
        print(f"\n【入场计划】")
        e = plan.entry_plan
        print(f"  当前价格: ${e.entry_price:.2f}")
        print(f"  入场区间: ${e.entry_range[0]:.2f} - ${e.entry_range[1]:.2f}")
        print(f"  首次仓位: {e.initial_position}股 (${e.initial_capital:,.2f})")
        print(f"\n  入场条件:")
        for i, cond in enumerate(e.entry_conditions, 1):
            print(f"    {i}. {cond}")
        
        # 出场计划
        print(f"\n【出场计划】")
        x = plan.exit_plan
        print(f"  止损价格: ${x.stop_loss:.2f}")
        print(f"  止盈目标1 (50%): ${x.take_profit_1:.2f}")
        print(f"  止盈目标2 (80%): ${x.take_profit_2:.2f}")
        print(f"  止盈目标3 (100%): ${x.take_profit_3:.2f}")
        print(f"  移动止损: {'启用' if x.trailing_stop else '不启用'}")
        print(f"  时间止损: {x.time_stop}天")
        
        # 仓位计划
        print(f"\n【仓位管理计划】")
        p = plan.position_plan
        print(f"  总仓位: {p.total_position}股")
        print(f"  首次入场: {p.initial_entry}股 (40%)")
        print(f"  加仓1: {p.add_position_1}股 (30%) - 盈利{p.add_trigger_1*100:.0f}%后")
        print(f"  加仓2: {p.add_position_2}股 (20%) - 盈利{p.add_trigger_2*100:.0f}%后")
        print(f"  风险金额: ${p.risk_amount:,.2f} ({p.risk_percent:.1f}%)")
        
        # 风险控制
        print(f"\n【风险控制】")
        r = plan.risk_control
        print(f"  单笔最大亏损: ${r.max_loss_per_trade:,.2f}")
        print(f"  单日最大亏损: ${r.max_loss_per_day:,.2f}")
        print(f"  最大回撤限制: ${r.max_drawdown:,.2f}")
        print(f"  单一标的上限: ${r.position_limit:,.2f}")
        print(f"\n  紧急出场条件:")
        for i, cond in enumerate(r.emergency_exit, 1):
            print(f"    {i}. {cond}")
        
        # 执行清单
        print(f"\n【交易前检查清单】")
        for item in plan.pre_trade_checklist:
            print(f"  {item}")
        
        print(f"\n【交易后检查清单】")
        for item in plan.post_trade_checklist:
            print(f"  {item}")
        
        # 心理管理
        print(f"\n【心理管理提示】")
        for i, tip in enumerate(plan.psychology_tips, 1):
            print(f"  {i}. {tip}")
        
        # 风险提示
        print(f"\n{'='*70}")
        print("【风险提示】")
        print("  ⚠️ 本交易计划仅供参考，不构成投资建议")
        print("  ⚠️ 交易有风险，入市需谨慎")
        print("  ⚠️ 请根据自身情况调整交易计划")
        print("  ⚠️ 严格执行风险控制规则")
        print(f"{'='*70}")


def main():
    parser = argparse.ArgumentParser(description='生成交易计划')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--account-size', type=float, default=100000,
                       help='账户规模')
    parser.add_argument('--risk-per-trade', type=float, default=0.02,
                       help='单笔交易风险比例')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建生成器
    generator = TradingPlanGenerator(
        args.symbol,
        args.account_size,
        args.risk_per_trade,
        args.output
    )
    
    # 生成计划
    plan = generator.generate_plan()
    
    # 保存和打印计划
    generator.save_plan(plan)
    generator.print_plan(plan)


if __name__ == '__main__':
    main()
