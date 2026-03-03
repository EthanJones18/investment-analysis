#!/usr/bin/env python3
import akshare as ak
import sys
from datetime import datetime

def get_hk_index_quote():
    """获取恒生科技指数实时行情"""
    try:
        # 获取港股指数行情
        df = ak.index_investing_global(country="香港", index_name="恒生科技指数", period="每日", start_date="20250301", end_date="20250303")
        if not df.empty:
            latest = df.iloc[-1]
            print(f"\n{'='*50}")
            print(f"📊 恒生科技指数 (HSTECH)")
            print(f"{'='*50}")
            print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📅 数据日期: {latest.get('日期', 'N/A')}")
            print(f"💰 收盘: {latest.get('收盘', 'N/A')}")
            print(f"📈 开盘: {latest.get('开盘', 'N/A')}")
            print(f"🔺 最高: {latest.get('最高', 'N/A')}")
            print(f"🔻 最低: {latest.get('最低', 'N/A')}")
            print(f"📊 涨跌幅: {latest.get('涨跌幅', 'N/A')}%")
            print(f"{'='*50}\n")
    except Exception as e:
        print(f"❌ 恒生科技指数查询失败: {e}")

def get_hk_stock_quote(code, name):
    """获取港股实时行情"""
    try:
        # 使用港股实时行情接口
        df = ak.stock_hk_spot_em()
        stock = df[df['代码'] == code]
        if not stock.empty:
            s = stock.iloc[0]
            print(f"\n{'='*50}")
            print(f"📊 {name} ({code})")
            print(f"{'='*50}")
            print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"💰 最新价: {s.get('最新价', 'N/A')}")
            print(f"📈 涨跌额: {s.get('涨跌额', 'N/A')}")
            print(f"📉 涨跌幅: {s.get('涨跌幅', 'N/A')}%")
            print(f"🔺 最高价: {s.get('最高价', 'N/A')}")
            print(f"🔻 最低价: {s.get('最低价', 'N/A')}")
            print(f"📊 今开: {s.get('今开', 'N/A')}")
            print(f"💹 成交量: {s.get('成交量', 'N/A')}")
            print(f"{'='*50}\n")
        else:
            print(f"❌ 未找到股票 {code}")
    except Exception as e:
        print(f"❌ {name}查询失败: {e}")

if __name__ == "__main__":
    print("🚀 正在查询实时行情...")
    
    # 查询恒生科技指数
    get_hk_index_quote()
    
    # 查询阿里巴巴
    get_hk_stock_quote("09988", "阿里巴巴-W")
    
    print("✅ 查询完成！")
