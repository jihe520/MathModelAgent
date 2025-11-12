@echo off
echo 正在清理所有相关服务进程...

echo.
echo 1. 清理 Python/uvicorn 进程...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul

echo.
echo 2. 清理 Node.js 进程...
taskkill /f /im node.exe 2>nul

echo.
echo 3. 清理 Redis 进程...
taskkill /f /im redis-server.exe 2>nul

echo.
echo 4. 等待端口释放...
timeout /t 3 /nobreak >nul

echo.
echo 5. 检查端口占用情况...
netstat -ano | findstr "8000 6379 5173"

echo.
echo 清理完成！现在可以重新启动服务了。
pause