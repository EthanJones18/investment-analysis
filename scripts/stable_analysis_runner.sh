#!/bin/bash
# 投资分析任务稳定执行脚本
# 功能：带重试机制、错误处理、状态记录

set -e

TASK_NAME="$1"
shift
ASSETS="$@"

LOG_DIR="/root/.openclaw/workspace/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/analysis_$(date +%Y%m%d_%H%M%S).log"
MAX_RETRIES=3
RETRY_DELAY=30

echo "========================================" | tee -a "$LOG_FILE"
echo "任务: $TASK_NAME" | tee -a "$LOG_FILE"
echo "标的: $ASSETS" | tee -a "$LOG_FILE"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 记录执行状态
record_status() {
    local status="$1"
    local message="$2"
    cat > "$LOG_DIR/last_run_status.json" << EOF
{
    "task": "$TASK_NAME",
    "timestamp": "$(date -Iseconds)",
    "status": "$status",
    "message": "$message",
    "assets": "$ASSETS"
}
EOF
}

# 检查AI服务状态
check_ai_service() {
    echo "检查AI服务状态..." | tee -a "$LOG_FILE"
    # 这里可以添加健康检查逻辑
    return 0
}

# 执行分析任务
run_analysis() {
    local attempt="$1"
    echo "" | tee -a "$LOG_FILE"
    echo "--- 第 $attempt 次尝试 ---" | tee -a "$LOG_FILE"
    
    # 调用分析（这里会被替换为实际的agent调用）
    # 返回码：0=成功，1=AI过载，2=其他错误
    return 0
}

# 主执行逻辑
main() {
    check_ai_service
    
    local attempt=1
    local success=false
    
    while [ $attempt -le $MAX_RETRIES ]; do
        if run_analysis $attempt; then
            success=true
            break
        else
            echo "第 $attempt 次尝试失败" | tee -a "$LOG_FILE"
            
            if [ $attempt -lt $MAX_RETRIES ]; then
                echo "等待 ${RETRY_DELAY}秒后重试..." | tee -a "$LOG_FILE"
                sleep $RETRY_DELAY
            fi
        fi
        
        attempt=$((attempt + 1))
    done
    
    echo "" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
    
    if [ "$success" = true ]; then
        echo "✅ 任务执行成功" | tee -a "$LOG_FILE"
        record_status "success" "任务完成"
        exit 0
    else
        echo "❌ 任务执行失败，已重试 $MAX_RETRIES 次" | tee -a "$LOG_FILE"
        record_status "failed" "达到最大重试次数"
        exit 1
    fi
}

main