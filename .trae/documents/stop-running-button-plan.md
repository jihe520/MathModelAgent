# 停止运行按钮实现方案

## 需求概述

在任务详情页（`task/index.vue`）右上角区域（"下载结果"按钮旁）新增一个「停止运行」按钮，点击后可中止正在执行的任务。

## 现状分析

### 当前任务执行链路

```
POST /modeling → background_tasks.add_task()
  → run_modeling_task_async()
    → asyncio.create_task(MathModelWorkFlow().execute(problem))
    → asyncio.wait_for(task, timeout=3600*5)  # 5小时硬超时
```

### 关键发现

* **无取消机制**：没有 cancel API、没有 cancel\_event、没有任务注册表

* **任务不可追踪**：`asyncio.create_task()` 创建后无法通过 task\_id 获取引用

* **前端无运行状态**：没有 `isRunning`/`taskStatus` 字段，只能间接推断

* **WebSocket 单向通信**：`send()` 方法存在但从未使用

***

## 实现步骤

### Step 1：后端 — 建立任务注册与取消机制

**文件**: [modeling\_router.py](backend/app/routers/modeling_router.py)

1.1 新增模块级任务注册表：

```python
# 文件顶部新增
import asyncio
from typing import Dict, Tuple

# 任务注册表: task_id -> (asyncio.Task, asyncio.Event)
_active_tasks: Dict[str, Tuple[asyncio.Task, asyncio.Event]] = {}
```

1.2 修改 `run_modeling_task_async()` 函数：

* 创建 `asyncio.Event()` 作为取消信号

* 用 `asyncio.create_task()` 创建任务并存入 `_active_tasks`

* 将 `cancel_event` 传入 `MathModelWorkFlow.execute()`

* 任务完成/异常时从注册表中清理

1.3 新增取消接口 `POST /modeling/{task_id}/cancel`：

* 查找 `_active_tasks[task_id]`

* 调用 `cancel_event.set()` 发送取消信号

* 可选：调用 `task.cancel()` 作为兜底

* 通过 Redis 发布取消通知给前端

***

### Step 2：后端 — 工作流层支持取消

**文件**: [workflow.py](backend/app/core/workflow.py)

2.1 `MathModelWorkFlow.__init__()` 接收 `cancel_event: asyncio.Event` 参数

2.2 在 `execute()` 的关键检查点插入取消检测（每个 agent 调用前后）：

```python
# 在每个 agent.run() 调用前检查
if self.cancel_event.is_set():
    await redis_manager.publish_message(
        self.task_id,
        SystemMessage(content="任务已停止", type="warning"),
    )
    return
```

关键检查点位置：

* CoordinatorAgent 调用前/后

* ModelerAgent 调用前/后

* 每个 solution\_flow 循环迭代开始时（CoderAgent + WriterAgent）

* 每个 write\_flow 循环迭代开始时

***

### Step 3：后端 — Agent 层传播取消事件

**文件**: [agent.py](backend/app/core/agents/agent.py) 及各子类 Agent

3.1 `Agent.__init__()` 新增可选参数 `cancel_event: asyncio.Event | None = None`

3.2 `Agent.run()` 在 `self.model.chat()` 调用外层包裹取消检测：

```python
# 使用 asyncio.wait 配合 cancel_event 实现可中断等待
chat_task = asyncio.create_task(self.model.chat(...))
done, pending = await asyncio.wait(
    {chat_task, asyncio.create_task(self.cancel_event.wait())},
    return_when=asyncio.FIRST_COMPLETED,
)
if self.cancel_event.is_set():
    chat_task.cancel()
    raise asyncio.CancelledError("任务被用户停止")
```

> 注：各子类 Agent（CoordinatorAgent、ModelerAgent、CoderAgent、WriterAgent）需将 `cancel_event` 透传给基类。

***

### Step 4：前端 — 新增取消 API

**文件**: [commonApi.ts](frontend/src/apis/commonApi.ts)

4.1 新增函数：

```typescript
/** 取消正在运行的任务 */
export function cancelTask(task_id: string) {
	return request.post<{ success: boolean; message: string }>(
		`/modeling/${task_id}/cancel`,
	);
}
```

***

### Step 5：前端 — Task Store 增加运行状态管理

**文件**: [task.ts](frontend/src/stores/task.ts)

5.1 新增状态：

```typescript
/** 任务是否正在运行 */
const isRunning = ref(false);
```

5.2 新增 actions：

```typescript
/** 取消任务 */
async function cancelTask(taskId: string) {
	try {
		const res = await cancelTaskAPI(taskId);
		if (res.data.success) {
			isRunning.value = false;
		}
	} catch (error) {
		console.error("取消任务失败:", error);
	}
}
```

5.3 修改 `connectWebSocket()` / 消息处理逻辑：

* 收到 `type="success"` 的 system message（"任务处理完成"）→ `isRunning = false`

* 收到 `type="warning"` 的 system message（"任务已停止"）→ `isRunning = false`

* 连接 WebSocket 时 → `isRunning = true`（假设进入页面时任务可能还在跑）

5.4 在 return 中导出 `isRunning` 和 `cancelTask`

***

### Step 6：前端 — UI 添加停止按钮

**文件**: [index.vue](frontend/src/pages/task/index.vue)（第 130-137 行区域）

6.1 在 `<div class="flex justify-end gap-2 items-center">` 中，"下载消息"按钮前面插入：

```vue
<Button
  v-if="taskStore.isRunning"
  variant="destructive"
  @click="handleStop"
  :disabled="isStopping"
>
  <span v-if="isStopping">停止中...</span>
  <span v-else>停止运行</span>
</Button>
```

6.2 新增 `handleStop` 方法和 `isStopping` 状态：

```typescript
const isStopping = ref(false);

async function handleStop() {
	isStopping.value = true;
	await taskStore.cancelTask(props.task_id);
	isStopping.value = false;
}
```

6.3 样式细节：

* 使用 `variant="destructive"`（红色警告样式）区分于普通操作按钮

* 停止中状态禁用按钮并显示 "停止中..." 防止重复点击

***

## 涉及文件清单

| 文件                                             | 改动类型 | 说明                                 |
| ---------------------------------------------- | ---- | ---------------------------------- |
| `backend/app/routers/modeling_router.py`       | 修改   | 新增任务注册表 + 取消接口                     |
| `backend/app/core/workflow.py`                 | 修改   | execute() 传入 cancel\_event 并在关键点检测 |
| `backend/app/core/agents/agent.py`             | 修改   | 基类支持 cancel\_event，run() 可被中断      |
| `backend/app/core/agents/coordinator_agent.py` | 修改   | 透传 cancel\_event                   |
| `backend/app/core/agents/modeler_agent.py`     | 修改   | 透传 cancel\_event                   |
| `backend/app/core/agents/coder_agent.py`       | 修改   | 透传 cancel\_event                   |
| `backend/app/core/agents/writer_agent.py`      | 修改   | 透传 cancel\_event                   |
| `frontend/src/apis/commonApi.ts`               | 修改   | 新增 cancelTask API                  |
| `frontend/src/stores/task.ts`                  | 修改   | 新增 isRunning 状态和 cancelTask action |
| `frontend/src/pages/task/index.vue`            | 修改   | 右上角添加停止按钮                          |

## 取消机制流程图

```
用户点击「停止运行」
  ↓
前端 POST /modeling/{task_id}/cancel
  ↓
后端查找 _active_tasks[task_id]
  ↓
cancel_event.set()  ←── 设置取消信号
  ↓
同时 redis_manager.publish_message("任务已停止", type="warning")
  ↓
┌─────────────────────────────────┐
│ 工作流 execute() 检测到信号     │
│   ├─ 当前 agent 正在 LLM 调用   │ → asyncio.CancelledError → 向上冒泡
│   └─ 当前 agent 之间（空闲期）   │ → 直接 return               │
└─────────────────────────────────┘
  ↓
从 _active_tasks 中清理该任务
  ↓
前端收到 warning 类型 system message → isRunning = false → 按钮隐藏
```

## 边界情况处理

1. **任务已完成再点取消**：后端返回任务不在注册表中，前端忽略即可
2. **取消时 LLM 正在调用**：通过 `asyncio.wait` + `task.cancel()` 双重机制确保中断
3. **页面刷新后丢失状态**：进入任务页时默认 `isRunning=true`，收到完成/停止消息后更新
4. **代码沙盒 cleanup**：取消后仍需执行 `code_interpreter.cleanup()` 清理资源（在 finally 中）

