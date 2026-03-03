#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易信号生成脚本
基于技术指标生成买入/卖出信号

使用方法:
    python trading_signals.py --symbol AAPL --strategy multi_indicator
"""

import argparse
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd

from technical_indicators import TechnicalIndicators


class TradingSignals:
    """交易信号生成器"""
    
    def __init__(self, df):
        """
        初始化
        
        Args:
            df: DataFrame包含OHLCV数据
        """
        self.df = df.copy()
        self.ti = TechnicalIndicators(df)
    
    def macd_signal(self):
        """
        MACD金叉死叉信号
        
        Returns:
            Series: 1买入, -1卖出, 0无信号
        """
        macd_df = self.ti.macd()
        dif = macd_df['dif']
        dea = macd_df['dea']
        
        # 金叉：DIF上穿DEA
        golden_cross = (dif > dea) & (dif.shift(1) <= dea.shift(1))
        # 死叉：DIF下穿DEA
        death_cross = (dif < dea) & (dif.shift(1) >= dea.shift(1))
        
        signal = pd.Series(0, index=self.df.index)
        signal[golden_cross] = 1
        signal[death_cross] = -1
        
        return signal
    
    def rsi_signal(self, overbought=70, oversold=30):
        """
        RSI超买超卖信号
        
        Args:
            overbought: 超买阈值
            oversold: 超卖阈值
            
        Returns:
            Series: 1买入, -1卖出, 0无信号
        """
        rsi = self.ti.rsi()
        
        # 超卖区反弹：RSI从低于oversold上升到高于oversold
        buy_signal = (rsi > oversold) & (rsi.shift(1) <= oversold)
        # 超买区回落：RSI从高于overbought下降到低于overbought
        sell_signal = (rsi < overbought) & (rsi.shift(1) >= overbought)
        
        signal = pd.Series(0, index=self.df.index)
        signal[buy_signal] = 1
        signal[sell_signal] = -1
        
        return signal
    
    def ma_cross_signal(self, short=20, long=50):
        """
        均线金叉死叉信号
        
        Args:
            short: 短期均线周期
            long: 长期均线周期
            
        Returns:
            Series: 1买入, -1卖出, 0无信号
        """
        ma_short = self.ti.sma(short)
        ma_long = self.ti.sma(long)
        
        # 金叉
        golden_cross = (ma_short > ma_long) & (ma_short.shift(1) <= ma_long.shift(1))
        # 死叉
        death_cross = (ma_short < ma_long) & (ma_short.shift(1) >= ma_long.shift(1))
        
        signal = pd.Series(0, index=self.df.index)
        signal[golden_cross] = 1
        signal[death_cross] = -1
        
        return signal
    
    def bollinger_signal(self):
        """
        布林带信号
        
        Returns:
            Series: 1买入(触及下轨反弹), -1卖出(触及上轨回落), 0无信号
        """
        bb = self.ti.bollinger_bands()
        close = self.df['close']
        
        # 触及下轨后反弹
        touch_lower = (close <= bb['lower']) & (close.shift(1) > bb['lower'].shift(1))
        # 触及上轨后回落
        touch_upper = (close >= bb['upper']) & (close.shift(1) < bb['upper'].shift(1))
        
        signal = pd.Series(0, index=self.df.index)
        signal[touch_lower] = 1
        signal[touch_upper] = -1
        
        return signal
    
    def kdj_signal(self):
        """
        KDJ金叉死叉信号
        
        Returns:
            Series: 1买入, -1卖出, 0无信号
        """
        kdj = self.ti.kdj()
        k = kdj['k']
        d = kdj['d']
        
        # K上穿D（金叉）
        golden_cross = (k > d) & (k.shift(1) <= d.shift(1))
        # K下穿D（死叉）
        death_cross = (k < d) & (k.shift(1) >= d.shift(1))
        
        signal = pd.Series(0, index=self.df.index)
        signal[golden_cross] = 1
        signal[death_cross] = -1
        
        return signal
    
    def multi_indicator_signal(self):
        """
        多指标共振信号
        综合MACD、RSI、均线、布林带生成信号
        
        Returns:
            DataFrame: 包含各指标信号和综合信号
        """
        signals = pd.DataFrame(index=self.df.index)
        signals['close'] = self.df['close']
        
        # 各指标信号
        signals['macd'] = self.macd_signal()
        signals['rsi'] = self.rsi_signal()
        signals['ma_cross'] = self.ma_cross_signal()
        signals['bollinger'] = self.bollinger_signal()
        signals['kdj'] = self.kdj_signal()
        
        # 综合信号（多数指标同向时产生信号）
        signals['combined'] = signals[['macd', 'rsi', 'ma_cross', 'bollinger', 'kdj']].sum(axis=1)
        
        # 最终信号：3个及以上指标同向
        signals['final'] = 0
        signals.loc[signals['combined'] >= 3, 'final'] = 1  # 强烈买入
        signals.loc[signals['combined'] <= -3, 'final'] = -1  # 强烈卖出
        signals.loc[(signals['combined'] > 0) & (signals['combined'] < 3), 'final'] = 0.5  # 弱买入
        signals.loc[(signals['combined'] < 0) & (signals['combined'] > -3), 'final'] = -0.5  # 弱卖出
        
        return signals
    
    def generate_report(self, strategy='multi_indicator'):
        """
        生成交易信号报告
        
        Args:
            strategy: 策略名称
            
        Returns:
            dict: 报告数据
        """
        if strategy == 'multi_indicator':
            signals = self.multi_indicator_signal()
        elif strategy == 'macd':
            sig = self.macd_signal()
            signals = pd.DataFrame({'final': sig, 'close': self.df['close']})
        elif strategy == 'rsi':
            sig = self.rsi_signal()
            signals = pd.DataFrame({'final': sig, 'close': self.df['close']})
        elif strategy == 'ma_cross':
            sig = self.ma_cross_signal()
            signals = pd.DataFrame({'final': sig, 'close': self.df['close']})
        else:
            raise ValueError(f'未知策略: {strategy}')
        
        # 统计信号
        buy_signals = (signals['final'] > 0).sum()
        sell_signals = (signals['final'] < 0).sum()
        
        # 最新信号
        latest_signal = signals['final'].iloc[-1]
        latest_price = signals['close'].iloc[-1]
        
        report = {
            'strategy': strategy,
            'symbol': 'AAPL',
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'latest_price': round(latest_price, 2),
            'latest_signal': '买入' if latest_signal > 0 else ('卖出' if latest_signal < 0 else '观望'),
            'signal_strength': abs(latest_signal),
            'total_buy_signals': int(buy_signals),
            'total_sell_signals': int(sell_signals),
            'recent_signals': []
        }
        
        # 最近5个信号
        signal_days = signals[signals['final'] != 0].tail(5)
        for idx, row in signal_days.iterrows():
            report['recent_signals'].append({
                'date': idx.strftime('%Y-%m-%d') if isinstance(idx, pd.Timestamp) else str(idx),
                'price': round(row['close'], 2),
                'signal': '买入' if row['final'] > 0 else '卖出',
                'strength': abs(row['final'])
            })
        
        return report


def main():
    parser = argparse.ArgumentParser(description='交易信号生成工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--strategy', default='multi_indicator', 
                       choices=['multi_indicator', 'macd', 'rsi', 'ma_cross'],
                       help='交易策略')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建模拟数据
    dates = pd.date_range(end=datetime.now(), periods=200, freq='D')
    np.random.seed(42)
    
    close = 100 + np.cumsum(np.random.randn(200) * 2)
    df = pd.DataFrame({
        'date': dates,
        'open': close + np.random.randn(200),
        'high': close + abs(np.random.randn(200)) + 1,
        'low': close - abs(np.random.randn(200)) - 1,
        'close': close,
        'volume': np.random.randint(1000000, 10000000, 200)
    })
    df.set_index('date', inplace=True)
    
    # 生成信号
    ts = TradingSignals(df)
    report = ts.generate_report(args.strategy)
    
    # 保存报告
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_signals.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 打印报告
    print('=' * 60)
    print(f'交易信号报告 - {args.symbol}')
    print('=' * 60)
    print(f'策略: {report["strategy"]}')
    print(f'最新价格: {report["latest_price"]}')
    print(f'最新信号: {report["latest_signal"]} (强度: {report["signal_strength"]})')
    print(f'历史买入信号: {report["total_buy_signals"]} 次')
    print(f'历史卖出信号: {report["total_sell_signals"]} 次')
    print('\n最近信号:')
    for sig in report['recent_signals']:
        print(f'  {sig["date"]}: {sig["signal"]} @ {sig["price"]}')
    print('=' * 60)
    print(f'报告已保存: {output_file}')


if __name__ == '__main__':
    main()
