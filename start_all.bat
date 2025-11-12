@echo off
chcp 65001 >nul
echo ===========================================
echo    MathModelAgent 一键启动脚本
echo ===========================================
echo.

echo 步骤 1: 清理旧进程...
call cleanup_services.bat

echo.
echo 步骤 2: 启动 Redis...
start "Redis Server" cmd /k ".\redis-portable\redis-server.exe .\redis-portable\redis.windows.conf"
timeout /t 3 /nobreak >nul

echo.
echo 步骤 3: 启动后端服务...
start "Backend Server" cmd /k "cd backend && .\.venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 5 /nobreak >nul

echo.
echo 步骤 4: 启动前端服务...
start "Frontend Server" cmd /k "cd frontend && pnpm dev"

echo.
echo 正在等待服务启动...
timeout /t 3 /nobreak >nul

echo.
echo ===========================================
echo    所有服务启动完成！
echo ===========================================
echo.
echo 访问地址:
echo 前端界面: http://localhost:5173
echo 后端API:  http://localhost:8000
echo API文档:  http://localhost:8000/docs
echo.
echo 按任意键退出...
pause >nul