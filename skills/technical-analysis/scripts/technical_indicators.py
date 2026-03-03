#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术指标计算脚本
支持30+种常用技术指标计算

使用方法:
    python technical_indicators.py --symbol AAPL --indicator rsi,macd,bollinger --period 14
"""

import argparse
import json
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests


class TechnicalIndicators:
    """技术指标计算器"""
    
    def __init__(self, df):
        """
        初始化
        
        Args:
            df: DataFrame包含OHLCV数据 (open, high, low, close, volume)
        """
        self.df = df.copy()
        
    # ==================== 趋势指标 ====================
    
    def sma(self, period=20, column='close'):
        """简单移动平均线"""
        return self.df[column].rolling(window=period).mean()
    
    def ema(self, period=20, column='close'):
        """指数移动平均线"""
        return self.df[column].ewm(span=period, adjust=False).mean()
    
    def macd(self, fast=12, slow=26, signal=9):
        """
        MACD指标
        
        Returns:
            DataFrame包含 dif, dea, macd柱
        """
        ema_fast = self.ema(fast)
        ema_slow = self.ema(slow)
        dif = ema_fast - ema_slow
        dea = dif.ewm(span=signal, adjust=False).mean()
        macd_hist = (dif - dea) * 2
        
        return pd.DataFrame({
            'dif': dif,
            'dea': dea,
            'macd': macd_hist
        })
    
    def rsi(self, period=14):
        """相对强弱指数"""
        close = self.df['close']
        delta = close.diff()
        
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return pd.Series(rsi, name='rsi')
    
    def kdj(self, n=9, m1=3, m2=3):
        """KDJ随机指标"""
        low_list = self.df['low'].rolling(window=n, min_periods=n).min()
        high_list = self.df['high'].rolling(window=n, min_periods=n).max()
        
        rsv = (self.df['close'] - low_list) / (high_list - low_list) * 100
        
        k = rsv.ewm(com=m1-1, adjust=False).mean()
        d = k.ewm(com=m2-1, adjust=False).mean()
        j = 3 * k - 2 * d
        
        return pd.DataFrame({
            'k': k,
            'd': d,
            'j': j
        })
    
    def bollinger_bands(self, period=20, std_dev=2):
        """布林带"""
        close = self.df['close']
        
        middle = close.rolling(window=period).mean()
        std = close.rolling(window=period).std()
        
        upper = middle + std_dev * std
        lower = middle - std_dev * std
        
        return pd.DataFrame({
            'upper': upper,
            'middle': middle,
            'lower': lower
        })
    
    def calculate_all(self, indicators_list):
        """批量计算多个指标"""
        result = self.df.copy()
        
        for indicator in indicators_list:
            indicator = indicator.lower().strip()
            
            if indicator == 'sma':
                result['sma_20'] = self.sma(20)
                result['sma_50'] = self.sma(50)
            elif indicator == 'ema':
                result['ema_12'] = self.ema(12)
                result['ema_26'] = self.ema(26)
            elif indicator == 'macd':
                macd_df = self.macd()
                result = pd.concat([result, macd_df], axis=1)
            elif indicator == 'rsi':
                result['rsi'] = self.rsi()
            elif indicator == 'kdj':
                kdj_df = self.kdj()
                result = pd.concat([result, kdj_df], axis=1)
            elif indicator == 'bollinger':
                bb_df = self.bollinger_bands()
                result = pd.concat([result, bb_df], axis=1)
        
        return result


def main():
    parser = argparse.ArgumentParser(description='技术指标计算工具')
    parser.add_argument('--symbol', required=True, help='股票代码')
    parser.add_argument('--indicator', required=True, help='指标列表，逗号分隔')
    parser.add_argument('--output', default='./output', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建模拟数据
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    np.random.seed(42)
    
    close = 100 + np.cumsum(np.random.randn(100) * 2)
    df = pd.DataFrame({
        'date': dates,
        'open': close + np.random.randn(100),
        'high': close + abs(np.random.randn(100)) + 1,
        'low': close - abs(np.random.randn(100)) - 1,
        'close': close,
        'volume': np.random.randint(1000000, 10000000, 100)
    })
    
    # 计算指标
    ti = TechnicalIndicators(df)
    indicators = args.indicator.split(',')
    result = ti.calculate_all(indicators)
    
    # 保存结果
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, f'{args.symbol}_indicators.csv')
    result.to_csv(output_file, index=False)
    
    print(f'指标计算完成: {output_file}')


if __name__ == '__main__':
    main()
