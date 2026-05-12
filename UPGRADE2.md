# MathModelAgent 三功能升级说明

> 升级日期: 2026-05-12
> 涉及 Phase: 0 (基础设施) → 1 (Web Search) → 2 (RAG 知识库) → 3 (HIL 人机协作)

---

## 一、升级概览

本次升级为 MathModelAgent 新增三项核心能力：

| 功能 | 作用 | 配置开关 |
|------|------|----------|
| **Web Search** | Agent 自主搜索互联网获取真实数据 | `SEARCH_ENABLED` + `TAVILY_API_KEY` |
| **RAG 知识库** | 从本地知识库检索建模方法、代码模板、论文写作参考 | `RAG_ENABLED` |
| **HIL 人机协作** | 在关键节点暂停等待用户审批，支持 6 种决策动作 | `HIL_ENABLED` |

**向后兼容**: 三项功能均有独立开关，未配置时系统行为与升级前完全一致。

---

## 二、新增文件清单

### 后端新增文件

| 文件 | 用途 |
|------|------|
| `backend/app/schemas/evidence.py` | Evidence 数据模型（DataEvidence / KnowledgeEvidence） |
| `backend/app/tools/tool_registry.py` | 统一工具注册与分发（替代 if/elif 硬编码） |
| `backend/app/services/state_store.py` | Redis 持久化状态存储（搜索缓存 + HIL checkpoint） |
| `backend/app/tools/web_searcher.py` | Web 搜索工具（Tavily API → LLM 提取 → DataEvidence） |
| `backend/app/tools/knowledge_retriever.py` | RAG 知识检索（ChromaDB + Rerank → KnowledgeEvidence） |
| `backend/app/services/checkpoint_manager.py` | HIL 检查点管理器（Redis 持久化等待/提交决策） |
| `backend/scripts/build_knowledge_base.py` | 知识库离线构建脚本 |

### 前端新增文件

| 文件 | 用途 |
|------|------|
| `frontend/src/components/ApprovalDialog.vue` | HIL 审批对话框（6 按钮 + 倒计时 + 编辑/追问） |

---

## 三、修改文件清单

### 后端修改

| 文件 | 变更内容 |
|------|----------|
| `backend/app/config/setting.py` | 新增 TAVILY / RAG / HIL 三组配置项 |
| `backend/app/core/functions.py` | 新增 `search_web_tool` 和 `search_knowledge_tool` schema |
| `backend/app/core/agents/coder_agent.py` | 工具分发改用 `tool_registry.dispatch()`；新增 `available_tools` 属性 |
| `backend/app/core/agents/modeler_agent.py` | 新增 `run_with_tools()` 方法（单次 tool call 模式） |
| `backend/app/core/flows.py` | 新增搜索证据和知识库注入参数（coder/writer prompt） |
| `backend/app/core/workflow.py` | 集成 Web Search / RAG / HIL 三功能到主工作流 |
| `backend/app/core/prompts/modeler.py` | 新增知识库参考指令 |
| `backend/app/schemas/response.py` | 新增 `ApprovalMessage` 消息类型 |
| `backend/app/routers/ws_router.py` | 扩展为双向 WebSocket（客户端可发送决策消息） |
| `backend/app/pyproject.toml` | 新增 chromadb / sentence-transformers / pymupdf / rank-bm25 依赖 |

### 前端修改

| 文件 | 变更内容 |
|------|----------|
| `frontend/src/utils/response.ts` | 新增 `ApprovalMessage` TypeScript 接口 |
| `frontend/src/stores/task.ts` | 新增 `onApproval()` 回调注册和 `sendDecision()` 方法 |

---

## 四、架构设计

### 4.1 统一数据抽象

```
Web Search  ──→  DataEvidence   ──┐
                                  ├──→  注入到 Agent Prompt
RAG 知识库  ──→  KnowledgeEvidence ┘
```

- `DataEvidence`: 含 unit / time_range / region / original_excerpt 等结构化字段
- `KnowledgeEvidence`: 含 method_name / source_type / source_file 等结构化字段

### 4.2 Tool Registry 分发

```
Agent.tool_call(name, args)
        │
        ▼
  tool_registry.dispatch(name, args, task_id)
        │
        ├── execute_code  →  code_interpreter
        ├── search_web    →  WebSearcher.search()
        ├── search_papers →  OpenAlexScholar
        └── search_knowledge → KnowledgeRetriever.retrieve()
```

各 Agent 不再硬编码 if/elif 分发，统一通过 registry 路由。

### 4.3 HIL Checkpoint 流程

```
workflow.execute()
    │
    ├─ Coordinator ──→ checkpoint: problem_split
    │                      ├─ confirm  → 继续
    │                      ├─ edit     → 用修改内容继续
    │                      ├─ abort    → 中止
    │                      └─ ...
    ├─ Modeler     ──→ checkpoint: model_selection
    ├─ Coder(×N)   ──→ checkpoint: code_review_{key} (默认关闭)
    └─ Writer(全部) ──→ checkpoint: paper_review
```

决策通过 WebSocket 双向通道传递：前端 `sendDecision()` → 后端 `state_store.set()` → `checkpoint_manager.wait_for_update()` 返回。

### 4.4 RAG 三 Agent 分别检索

| Agent | 检索 source_type | 用途 |
|-------|-----------------|------|
| ModelerAgent | textbook, paper | 建模方法 + 优秀论文方案 |
| CoderAgent | code | 代码模板 |
| WriterAgent | paper, problem | 论文写作模板 |

---

## 五、配置说明

### 5.1 Web Search

在 `.env.dev` 中添加：

```env
TAVILY_API_KEY=tvly-xxxxxxxxxxxx
SEARCH_ENABLED=true
SEARCH_CACHE_TTL=86400
```

获取 API Key: https://tavily.com

### 5.2 RAG 知识库

```env
RAG_ENABLED=true
RAG_DB_PATH=data/chromadb
RAG_TOP_K=5
RAG_EMBEDDING_MODEL=BAAI/bge-m3
RAG_RERANKER_MODEL=BAAI/bge-reranker-v2-m3
```

构建知识库：

```bash
cd backend
# 准备知识库文件
mkdir -p data/knowledge/{papers,textbooks,code,problems}
# 将 PDF/Markdown/代码文件放入对应目录

# 安装依赖
uv sync

# 构建索引
python scripts/build_knowledge_base.py
```

### 5.3 HIL 人机协作

```env
HIL_ENABLED=true
HIL_TIMEOUT=300
```

检查点开关（JSON 格式）：

```env
HIL_CHECKPOINTS={"problem_split":true,"model_selection":true,"code_review":false,"paper_review":true}
```

| 检查点 | 默认 | 说明 |
|--------|------|------|
| problem_split | 开 | 协调者拆题后暂停 |
| model_selection | 开 | 建模手出方案后暂停 |
| code_review | 关 | 每个子任务代码执行后暂停（按需开启） |
| paper_review | 开 | 全部写完后暂停 |

### 5.4 6 种决策动作

| 动作 | 行为 |
|------|------|
| **confirm** | 确认当前结果，继续下一步 |
| **edit** | 用用户修改后的内容继续 |
| **regenerate** | 用原始 prompt 重跑当前 Agent |
| **ask** | 暂停等待用户补充信息后继续 |
| **skip** | 跳过审核，直接继续 |
| **abort** | 清理资源，标记任务失败 |

超时（默认 300 秒）自动执行 confirm。

---

## 六、依赖变更

新增 Python 依赖（`backend/pyproject.toml`）：

```
chromadb>=0.4.0
sentence-transformers>=2.2.0
pymupdf>=1.24.0
rank-bm25>=0.2.2
```

安装：

```bash
cd backend
uv sync
```

---

## 七、工作流执行流程（升级后）

```
1. Web Search 初始化（注册 search_web 工具）
2. RAG 初始化（注册 search_knowledge 工具）
3. CoordinatorAgent 解析题目
4. ── HIL Checkpoint: problem_split ──
5. RAG 检索建模方法知识
6. ModelerAgent 制定方案（可调用 search_web / search_knowledge）
7. ── HIL Checkpoint: model_selection ──
8. RAG 检索代码模板知识
9. 循环每个子任务:
   a. CoderAgent 求解（可调用 execute_code / search_web / search_knowledge）
   b. ── HIL Checkpoint: code_review_{key}（默认关闭）──
   c. WriterAgent 撰写对应章节
10. 关闭代码沙盒
11. RAG 检索论文写作知识
12. WriterAgent 撰写剩余章节（摘要/问题重述/分析/假设/符号/评价）
13. ── HIL Checkpoint: paper_review ──
14. 保存结果
```
