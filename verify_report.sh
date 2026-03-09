#!/bin/bash
# 报告数据核对脚本

REPORT_FILE=$1

if [ -z "$REPORT_FILE" ]; then
    echo "用法: ./verify_report.sh <报告文件路径>"
    exit 1
fi

echo "=== 数据核对开始 ==="
echo "核对文件: $REPORT_FILE"
echo "核对时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 提取A股代码
echo "🔍 提取A股标的..."
A_CODES=$(grep -oE 'sh[0-9]{6}|sz[0-9]{6}' "$REPORT_FILE" | sort -u | tr '\n' ',' | sed 's/,$//')

# 提取港股代码
echo "🔍 提取港股标的..."
HK_CODES=$(grep -oE 'rt_hk[0-9]{4,5}' "$REPORT_FILE" | sort -u | tr '\n' ',' | sed 's/,$//')

echo ""
echo "📊 查询实时行情..."

# 查询A股
if [ -n "$A_CODES" ]; then
    echo "A股标的: $A_CODES"
    curl -s "https://hq.sinajs.cn/list=$A_CODES" -H "Referer: https://finance.sina.com.cn" 2>/dev/null | iconv -f gb2312 -t utf-8 > /tmp/a_share_data.txt
    echo "✅ A股数据已获取"
fi

# 查询港股
if [ -n "$HK_CODES" ]; then
    echo "港股标的: $HK_CODES"
    curl -s "https://hq.sinajs.cn/list=$HK_CODES" -H "Referer: https://finance.sina.com.cn" 2>/dev/null | iconv -f gb2312 -t utf-8 > /tmp/hk_data.txt
    echo "✅ 港股数据已获取"
fi

echo ""
echo "📋 实时行情数据:"
echo "---"

if [ -f /tmp/a_share_data.txt ]; then
    cat /tmp/a_share_data.txt | grep -v "^var" | head -5
fi

if [ -f /tmp/hk_data.txt ]; then
    cat /tmp/hk_data.txt | grep -v "^var" | head -5
fi

echo "---"
echo ""
echo "⚠️  请人工核对报告中的数据与上述实时数据是否一致"
echo ""
echo "=== 数据核对完成 ==="
