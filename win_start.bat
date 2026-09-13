@echo off
chcp 65001 >nul

echo ==============================================
echo  一键启动 Redis + 后端FastAPI + 前端Vue/React
echo ==============================================
echo.

:: ====================== 前置检查 ======================
:: 不使用括号块：cmd 解析含中文的括号块时会把后续 echo 行拆断执行
where redis-server >nul 2>&1
if not errorlevel 1 goto :check_pnpm
echo [错误] 未找到 redis-server，请先安装 Redis 并加入 PATH:
echo        Windows 下载地址: https://github.com/tporadowski/redis/releases
goto :fail

:check_pnpm
where pnpm >nul 2>&1
if not errorlevel 1 goto :check_venv
echo [错误] 未找到 pnpm，请先执行: npm install -g pnpm
goto :fail

:: ====================== 探测后端虚拟环境 ======================
:: README 的 uv sync 流程生成 .venv，PowerShell 教程生成 venv，两者均支持
:check_venv
set "VENV_DIR="
if exist ".\backend\venv\Scripts\Activate.bat" set "VENV_DIR=venv"
if not defined VENV_DIR if exist ".\backend\.venv\Scripts\Activate.bat" set "VENV_DIR=.venv"
if defined VENV_DIR goto :start_all

echo [错误] 未找到后端虚拟环境 backend\venv 或 backend\.venv
echo        请先按 README 安装后端依赖: cd backend 然后 uv sync
goto :fail

:: ====================== 启动服务 ======================
:start_all
echo 使用后端虚拟环境: backend\%VENV_DIR%
echo.

start "Redis 服务" cmd /k "redis-server"

start "后端服务" cmd /k "cd /d .\backend && .\%VENV_DIR%\Scripts\Activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload"

start "前端服务" cmd /k "cd /d .\frontend && pnpm run dev"

echo 三个服务已启动，请等待各窗口内服务就绪。
echo.
goto :end

:fail
echo.
echo 启动中止: 请根据上方提示修复后重试。
pause
exit /b 1

:end
pause
