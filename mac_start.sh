#!/bin/bash
echo "=============================================="
echo "  一键启动 Redis + 后端FastAPI + 前端Vue/React"
echo "=============================================="
echo ""

# 获取脚本所在目录（处理符号链接和相对路径）
cd "$(dirname "$0")" || exit 1
PROJECT_DIR="$(pwd)"

# ====================== 启动 Redis ======================
osascript -e "tell application \"Terminal\" to do script \"echo '[Redis] 启动中...' && redis-server\""

# ====================== 启动 后端 ======================
osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR/backend' && export REDIS_URL=redis://localhost:6379/0 && source .venv/bin/activate && echo '[后端] 启动中...' && uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload\""

# ====================== 启动 前端 ======================
osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR/frontend' && echo '[前端] 启动中...' && pnpm run dev\""

echo "三个服务已全部启动！"
echo ""
