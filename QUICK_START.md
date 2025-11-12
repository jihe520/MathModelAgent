# 🚀 MathModelAgent 项目快速启动指南

## 📋 项目概述

**MathModelAgent** 是一个专为数学建模设计的智能Agent系统，能够自动完成数学建模、代码编写和论文生成的完整流程。项目采用前后端分离架构，支持多模型、多Agent协作。

## 🏗️ 项目架构

```
MathModelAgent/
├── frontend/           # Vue3 前端界面
├── backend/           # FastAPI 后端服务
├── redis-portable/    # Redis 数据库（Windows便携版）
├── docs/              # 文档资料
└── docker-compose.yml # Docker 容器编排
```

## 🔧 环境要求

### 基础环境
- **Python**: >= 3.12
- **Node.js**: >= 18.0
- **pnpm**: 包管理器
- **Redis**: 数据缓存（项目已包含便携版）

### 系统要求
- **操作系统**: Windows 10/11, macOS, Linux
- **内存**: 建议 8GB 以上
- **存储**: 至少 2GB 可用空间

## ⚡ 快速启动（3 步骤）

### 步骤 1: 环境准备

```powershell
# 1. 克隆项目到本地
git clone https://github.com/shinebuling/MathModelAgent.git
cd MathModelAgent

# 2. 检查 Python 版本
python --version  # 确保 >= 3.12

# 3. 检查 Node.js 和 pnpm
node --version
pnpm --version
```

### 步骤 2: 启动 Redis

```powershell
# 使用项目提供的一键启动脚本（推荐）
.\redis_start_clean.bat

# 或手动启动
.\redis-portable\redis-server.exe .\redis-portable\redis.windows.conf
```

**✅ 验证 Redis 启动成功**
- 看到 `Redis 服务启动成功！端口: 6379` 提示
- 或使用客户端测试：`.\redis-portable\redis-cli.exe ping`

### 步骤 3: 启动后端服务

```powershell
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv .venv

# 3. 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# 4. 安装依赖
pip install -e .

# 5. 启动后端服务（确保在 backend 目录下）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 步骤 4: 启动前端界面

```powershell
# 新开一个终端窗口
cd frontend

# 1. 安装依赖
pnpm install

# 2. 启动开发服务器
pnpm dev
```

## 🎯 访问地址

启动成功后，您可以通过以下地址访问系统：

- **前端界面**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **Redis端口**: localhost:6379

## 🐳 Docker 快速部署

如果您prefer使用Docker，可以一键启动整个系统：

```powershell
# 1. 确保Docker已安装并运行
docker --version

# 2. 启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps
```

**Docker 访问地址**:
- **前端**: http://localhost:3000
- **后端**: http://localhost:8000
- **Redis**: localhost:6379

## 🔑 配置说明

### 后端配置
在 `backend/` 目录下创建 `.env` 文件：

```env
# Redis 配置
REDIS_URL=redis://localhost:6379/0

# API Keys (根据需要配置)
OPENAI_API_KEY=your_openai_key
CLAUDE_API_KEY=your_claude_key

# E2B 配置（可选）
E2B_API_KEY=your_e2b_key

# 环境设置
ENV=DEV
DEBUG=True
```

### 前端配置
前端配置文件位于 `frontend/src/config/`，通常无需修改。

## 🛠️ 常见问题解决

### Redis 启动问题

**问题**: `Can't handle RDB format version 9`
```powershell
# 解决方案：删除旧的数据文件
del .\redis-portable\dump.rdb
del .\dump.rdb
# 重新启动 Redis
.\redis_start_clean.bat
```

**问题**: 端口 6379 被占用
```powershell
# 查找占用进程
netstat -ano | findstr ":6379"
# 结束进程（替换 PID）
taskkill /PID [进程ID] /F
```

### Python 环境问题

**问题**: 依赖安装失败
```powershell
# 升级 pip
pip install --upgrade pip
# 清理缓存重装
pip cache purge
pip install -e . --no-cache-dir
```

**问题**: 虚拟环境激活失败
```powershell
# 检查执行策略
Get-ExecutionPolicy
# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 前端启动问题

**问题**: pnpm 命令不存在
```powershell
# 安装 pnpm
npm install -g pnpm
```

**问题**: 依赖安装缓慢
```powershell
# 使用淘宝镜像
pnpm config set registry https://registry.npmmirror.com
```

## 📁 项目目录详解

```
MathModelAgent/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── main.py            # FastAPI 主应用
│   │   ├── core/              # 核心逻辑
│   │   │   ├── agents/        # 多Agent实现
│   │   │   ├── llm/           # LLM接入
│   │   │   └── workflow.py    # 工作流引擎
│   │   ├── routers/           # API路由
│   │   ├── services/          # 业务服务
│   │   └── tools/             # 工具集成
│   └── pyproject.toml         # Python项目配置
├── frontend/                   # 前端界面
│   ├── src/
│   │   ├── pages/             # 页面组件
│   │   ├── components/        # 通用组件
│   │   └── apis/              # API接口
│   └── package.json           # 前端依赖配置
├── redis-portable/             # Redis便携版
└── docs/                      # 文档目录
```

## 🎮 使用指南

1. **创建新项目**: 在前端界面点击"新建项目"
2. **输入问题**: 描述您的数学建模问题
3. **选择模型**: 配置使用的LLM模型
4. **开始建模**: 系统自动分析、建模、编码
5. **查看结果**: 获取完整的论文和代码

## 🔄 开发模式

### 后端热重载
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端热重载
```powershell
cd frontend
pnpm dev
```

### 代码质量检查
```powershell
# 后端代码检查
cd backend
ruff check .
ruff format .

# 前端代码检查
cd frontend
pnpm lint
```

## 🚀 生产部署

### 后端生产配置
```powershell
cd backend
pip install gunicorn
gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000
```

### 前端生产构建
```powershell
cd frontend
pnpm build
pnpm preview
```

## 📞 技术支持

- **GitHub Issues**: [项目Issues页面](https://github.com/shinebuling/MathModelAgent/issues)
- **文档**: 查看 `docs/` 目录下的详细文档
- **示例**: 参考 `backend/app/example/` 目录

## 🎉 恭喜！

如果所有服务都正常启动，您现在可以开始使用 MathModelAgent 进行数学建模了！

**快速验证**:
1. ✅ Redis: `.\redis-portable\redis-cli.exe ping` 返回 `PONG`
2. ✅ 后端: 访问 http://localhost:8000/docs 看到API文档
3. ✅ 前端: 访问 http://localhost:5173 看到用户界面

---

*享受您的数学建模之旅！* 🎯