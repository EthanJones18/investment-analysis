#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def get_hk_stock_quote(code, name):
    """获取港股实时行情 - 东方财富API"""
    try:
        # 东方财富港股API
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=116.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f170,f169"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()
        stock = data.get('data', {})
        
        if stock:
            print(f"\n{'='*60}")
            print(f"📊 {name}")
            print(f"代码: {stock.get('f57', code)}")
            print(f"{'='*60}")
            print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 解析数据（东方财富数据需要除以100）
            latest = stock.get('f43', 0)
            if latest:
                latest = float(latest) / 100
            
            open_price = stock.get('f46', 0)
            if open_price:
                open_price = float(open_price) / 100
                
            high = stock.get('f44', 0)
            if high:
                high = float(high) / 100
                
            low = stock.get('f45', 0)
            if low:
                low = float(low) / 100
            
            change_pct = stock.get('f170', 'N/A')
            change_amt = stock.get('f169', 'N/A')
            
            print(f"💰 最新价: {latest}")
            print(f"📈 涨跌额: {change_amt}")
            print(f"📉 涨跌幅: {change_pct}%")
            print(f"🔺 最高价: {high}")
            print(f"🔻 最低价: {low}")
            print(f"📊 开盘价: {open_price}")
            print(f"💹 成交量: {stock.get('f47', 'N/A')}")
            print(f"{'='*60}\n")
            return True
        else:
            print(f"❌ 未获取到 {name} 的数据")
            return False
    except Exception as e:
        print(f"❌ {name} 查询失败: {e}")
        return False

def get_hk_index():
    """获取恒生科技指数 - 使用ETF作为参考"""
    try:
        # 使用南方恒生科技ETF (03033) 作为参考
        return get_hk_stock_quote("03033", "南方恒生科技ETF (参考恒生科技指数)")
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 正在查询实时行情...\n")
    
    # 查询恒生科技指数（通过ETF）
    get_hk_index()
    
    # 查询阿里巴巴
    get_hk_stock_quote("09988", "阿里巴巴-W")
    
    print("✅ 查询完成！")
