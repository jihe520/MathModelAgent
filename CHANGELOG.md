# 修改日志 (Changelog)

## 版本: v1.1.0 - 2025年10月9日

### 🚀 主要更新

#### 1. 集成 Gitee AI 支持
- **替换 API 提供商**: 将默认的 OpenAI API 配置替换为 Gitee AI
- **更新模型配置**: 所有 Agent（Coordinator、Modeler、Coder、Writer）现在默认使用 `DeepSeek-V3` 模型
- **API 端点更新**: 基础 URL 更改为 `https://ai.gitee.com/v1`

#### 2. Redis 连接优化
- **优雅降级处理**: 当 Redis 服务不可用时，应用现在能够优雅降级而不会崩溃
- **文件系统备份**: 消息存储自动切换到文件系统（`logs/messages/` 目录）
- **错误处理改进**: Redis 连接失败时记录警告而非抛出异常

#### 3. 环境配置安全性增强
- **密钥保护**: 移除了硬编码的 API 密钥，改为环境变量配置
- **模板文件**: 新增 `.env.example` 作为配置模板
- **GitIgnore 更新**: 添加了环境文件、日志文件等的忽略规则

### 📝 详细修改内容

#### 后端 (Backend) 修改

##### 1. 环境配置文件
- **修改**: `backend/.env.dev`
  - 更新所有 API 密钥配置为 Gitee AI
  - 修改 Redis URL 从 `redis://redis:6379/0` 到 `redis://localhost:6379/0`
- **新增**: `backend/.env.example`
  - 提供安全的配置模板，不包含真实密钥

##### 2. Redis 管理器优化 (`app/services/redis_manager.py`)
```python
# 主要改进：
- get_client() 方法现在返回 Optional[aioredis.Redis] 而非直接抛出异常
- set() 方法增加 Redis 可用性检查
- publish_message() 方法在 Redis 不可用时仍能保存消息到文件
- subscribe_to_task() 方法增加优雅降级处理
```

##### 3. 路由器改进 (`app/routers/common_router.py`)
```python
# 状态检查优化：
- /status 端点现在能正确处理 Redis 不可用的情况
- 返回 "disabled" 状态而非 "error" 当 Redis 不可用时
```

##### 4. LLM 核心模块 (`app/core/llm/llm.py`)
- 集成 Gitee AI 配置
- 优化模型调用逻辑

##### 5. 建模路由器 (`app/routers/modeling_router.py`)
- 更新 API 密钥验证逻辑
- 改进错误处理

#### 前端 (Frontend) 修改

##### 1. API 对话框组件 (`src/pages/chat/components/ApiDialog.vue`)
- 更新 UI 以支持 Gitee AI 配置
- 改进用户体验

#### 项目配置

##### 1. Git 忽略规则 (`.gitignore`)
```gitignore
# 新增的忽略规则：
- 所有环境变量文件 (*.env, *.env.*)
- Python 缓存文件
- Node.js 模块
- 日志文件
- 数据库文件
- 生成的项目文件
```

##### 2. 文档更新
- **新增**: `ENV_SETUP.md` - 环境变量配置指南
- **新增**: `GiteeAI_Integration_Complete.md` - Gitee AI 集成完整文档

### 🔧 技术改进

#### 1. 错误处理
- Redis 连接失败时的优雅降级
- 更好的日志记录和错误信息

#### 2. 安全性
- 移除了所有硬编码的 API 密钥
- 环境变量文件已从版本控制中排除
- 提供安全的配置模板

#### 3. 可维护性
- 改进了代码结构
- 添加了详细的注释和文档
- 更好的错误处理机制

### 🚨 重要安全说明

1. **API 密钥保护**: 所有真实的 API 密钥现在通过环境变量管理，不再提交到版本控制
2. **配置文件**: 使用 `.env.example` 作为模板，开发者需要创建自己的 `.env.dev` 文件
3. **Git 安全**: 更新了 `.gitignore` 以防止意外提交敏感信息

### 🛠️ 部署注意事项

#### 本地开发环境设置
1. 复制环境变量模板：
   ```bash
   cp backend/.env.example backend/.env.dev
   ```

2. 编辑 `.env.dev` 文件，填入实际的 API 密钥

3. 如果没有 Redis，应用会自动降级到文件存储模式

#### Docker 部署
- Docker 环境中 Redis URL 应设置为 `redis://redis:6379/0`
- 本地部署使用 `redis://localhost:6379/0`

### 📊 影响范围

- **影响的文件**: 6个核心文件修改
- **新增文件**: 3个（文档和配置模板）
- **安全改进**: 100% 移除硬编码密钥
- **向后兼容性**: 保持 API 接口不变
- **性能影响**: 无负面影响，Redis 降级时使用文件存储

### 🔄 迁移指南

对于现有部署：
1. 更新环境变量配置
2. 获取 Gitee AI API 密钥
3. 更新 `.env` 文件中的配置
4. 重启服务

### 🎯 下一步计划

1. 添加 Redis 连接状态监控
2. 实现自动重连机制
3. 优化文件存储性能
4. 添加更多 AI 模型支持

---
