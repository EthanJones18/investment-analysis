#!/usr/bin/env python3
import akshare as ak
import sys
from datetime import datetime

def get_hk_spot():
    """获取港股实时行情"""
    try:
        print("🚀 正在获取港股实时数据...")
        df = ak.stock_hk_spot_em()
        return df
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return None

def query_stock(df, keyword):
    """查询指定股票"""
    try:
        # 按名称或代码查询
        result = df[df['名称'].str.contains(keyword, case=False, na=False) | 
                   df['代码'].str.contains(keyword, na=False)]
        return result
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return None

if __name__ == "__main__":
    # 获取港股实时数据
    df = get_hk_spot()
    
    if df is not None and not df.empty:
        print(f"\n{'='*60}")
        print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # 查询阿里巴巴
        print("📊 查询: 阿里巴巴-W (09988)")
        ali = query_stock(df, "阿里")
        if not ali.empty:
            for _, row in ali.head(3).iterrows():
                print(f"\n{'='*50}")
                print(f"名称: {row.get('名称', 'N/A')}")
                print(f"代码: {row.get('代码', 'N/A')}")
                print(f"最新价: {row.get('最新价', 'N/A')}")
                print(f"涨跌额: {row.get('涨跌额', 'N/A')}")
                print(f"涨跌幅: {row.get('涨跌幅', 'N/A')}%")
                print(f"最高价: {row.get('最高价', 'N/A')}")
                print(f"最低价: {row.get('最低价', 'N/A')}")
                print(f"成交量: {row.get('成交量', 'N/A')}")
                print(f"{'='*50}")
        else:
            print("❌ 未找到阿里巴巴")
        
        # 查询恒生科技相关ETF
        print("\n\n📊 查询: 恒生科技ETF")
        hst = query_stock(df, "恒生科技")
        if not hst.empty:
            for _, row in hst.head(3).iterrows():
                print(f"\n{'='*50}")
                print(f"名称: {row.get('名称', 'N/A')}")
                print(f"代码: {row.get('代码', 'N/A')}")
                print(f"最新价: {row.get('最新价', 'N/A')}")
                print(f"涨跌幅: {row.get('涨跌幅', 'N/A')}%")
                print(f"{'='*50}")
        else:
            print("❌ 未找到恒生科技ETF")
            
        print("\n✅ 查询完成！")
    else:
        print("❌ 无法获取数据")
