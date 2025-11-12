@echo off
echo 智能启动 Redis 服务器...

REM 1. 首先清理可能残留的Redis进程
echo 正在清理可能的残留进程...
taskkill /IM redis-server.exe /F >nul 2>&1

REM 2. 等待进程完全结束
timeout /t 1 /nobreak >nul

REM 3. 强制释放端口（如果被占用）
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":6379"') do (
    echo 清理端口占用进程 PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

REM 4. 清理可能存在的不兼容RDB文件
if exist redis-portable\dump.rdb (
    echo 清理不兼容的RDB文件...
    del redis-portable\dump.rdb >nul 2>&1
)
if exist dump.rdb (
    del dump.rdb >nul 2>&1
)

REM 5. 再等待一下确保清理完成
timeout /t 1 /nobreak >nul

REM 7. 启动Redis
echo 启动 Redis 服务器...
cd /d "%~dp0"
start "Redis Server" redis-portable\redis-server.exe redis-portable\redis.windows.conf

REM 8. 等待启动
timeout /t 2 /nobreak >nul

REM 9. 验证启动状态
netstat -an | findstr ":6379" >nul
if %errorlevel% == 0 (
    echo ✅ Redis 服务启动成功！端口: 6379
) else (
    echo ❌ Redis 服务启动失败，请检查配置
)

echo.
echo Redis 服务已在后台运行，可以关闭此窗口。
pause