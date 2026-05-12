# MathModelAgent Feedback Loop + Hand Off 升级说明

> 升级日期: 2026-05-12
> 涉及 Phase: 1 (有限重试) → 2 (Fallback Hand Off) → 3 (Evaluator Shadow Mode) → 4 (Feedback Rerun) → 5 (SystemMessage 集成)

---

## 一、升级概览

本次升级为 MathModelAgent 的多 Agent 流水线引入四层容错与质量保障机制：

| 功能 | 作用 | 配置开关 |
|------|------|----------|
| **有限重试** | 所有 Agent 有明确重试上限，不再无限循环 | `MAX_COORDINATOR_RETRIES` / `MAX_MODELER_RETRIES` |
| **Fallback Hand Off** | 主 LLM 故障时自动切换备用模型，新建实例避免状态污染 | `FALLBACK_*` 系列配置 |
| **Evaluator (Shadow Mode)** | 用独立便宜 LLM 评估输出质量，只记录不触发重跑 | `EVALUATOR_API_KEY` + `EVALUATOR_MODEL` |
| **Feedback Rerun** | 评估不通过时注入反馈重跑，先 Writer 后 Coder | `MAX_FEEDBACK_ROUNDS` + `EVALUATION_THRESHOLD` |

**核心设计原则**: wrap, don't rewrite — 所有增强均在编排层（workflow.py）实现，不修改 Agent 的 `run()` 核心逻辑。

**向后兼容**: 所有新增配置项均有默认值，未配置时系统行为与升级前完全一致。

---

## 二、新增文件清单

| 文件 | 用途 |
|------|------|
| `backend/app/core/evaluator.py` | 评估器（使用 `simple_chat()` 做单次评估，异常时返回 `passed=True`） |

---

## 三、修改文件清单

| 文件 | 变更内容 |
|------|----------|
| `backend/app/config/setting.py` | 新增 22 个配置项（重试次数 / Fallback / Evaluator / Feedback） |
| `backend/app/schemas/A2A.py` | 新增 `EvaluationResult` 数据模型 |
| `backend/app/schemas/enums.py` | 新增 `EVALUATOR` Agent 类型枚举 |
| `backend/app/core/agents/coordinator_agent.py` | `while True` → `for` 有限循环，超限 `raise ValueError` |
| `backend/app/core/agents/modeler_agent.py` | 同上 |
| `backend/app/core/agents/writer_agent.py` | 新增 `max_retries`，异常重试 + 软降级返回错误信息 |
| `backend/app/core/llm/llm_factory.py` | 新增 `get_fallback_llms()` 和 `get_evaluator_llm()` |
| `backend/app/core/workflow.py` | Hand Off 包装器 + Feedback Rerun 编排 + Evaluator Shadow Mode 集成 |

---

## 四、架构设计

### 4.1 四层容错机制

```
Agent 执行
    │
    ├─ 第 1 层: 有限重试（Agent 内部）
    │   └─ JSON 解析失败 / LLM 调用异常 → 重试 N 次 → 超限抛异常
    │
    ├─ 第 2 层: Fallback Hand Off（编排层）
    │   └─ 主 LLM 异常 / 返回失败响应 → 新建 Agent + Fallback LLM → 重试
    │
    ├─ 第 3 层: Evaluator Shadow Mode（编排层）
    │   └─ 评估器对输出评分 → 记录日志 + SystemMessage → 不触发重跑
    │
    └─ 第 4 层: Feedback Rerun（编排层）
        └─ 评估不通过 → 拼接反馈到 prompt → 新建 Agent 重跑 → 最多 N 轮
```

### 4.2 Hand Off 策略

```
coordinator_agent.run(ques_all)
    │
    ├─ 成功 → 返回 CoordinatorToModeler
    │
    └─ 异常 → fallback_llms["coordinator"] 存在？
        │
        ├─ 是 → 新建 CoordinatorAgent(task_id, fallback_llm)
        │       └─ fallback_agent.run(ques_all) → 返回或抛异常
        │
        └─ 否 → 直接抛出原始异常
```

**关键**: Hand Off 时**新建 Agent 实例**，不用 `agent.model = fallback_llm`，避免脏 `chat_history` 状态污染。

### 4.3 Feedback Rerun 流程

```
_run_writer_with_feedback(writer_agent, prompt, evaluator)
    │
    for round in 0..MAX_FEEDBACK_ROUNDS:
    │
    ├─ 1. 执行 Agent（含 Hand Off）
    ├─ 2. 无评估器或最后一轮 → 返回结果
    ├─ 3. 评估通过（passed=True 或 score >= threshold）→ 返回结果
    └─ 4. 评估不通过 → 拼接反馈到 prompt → 新建 Agent → 继续循环

最终返回最后一轮结果
```

**Feedback 注入方式**:
```python
augmented = f"{original_prompt}\n\n【评估反馈（第{round}轮）】\n{eval_result.feedback}"
```

利用已有的 `run(prompt)` 接口，不修改 `run()` 方法。

### 4.4 Coder 专用 Hand Off

CoderAgent 与其他 Agent 不同：它在 `run()` 内部处理重试，失败时返回 `CoderToWriter(code_response="任务失败...")` 而非抛异常。因此 `_run_coder_with_handoff()` 同时检测：

- 异常（`except Exception`）→ Hand Off
- 失败响应（`code_response.startswith("任务失败")`）→ Hand Off

---

## 五、配置说明

在 `.env.dev` 中添加（均为可选，未配置时跳过对应功能）：

### 5.1 有限重试

```env
# JSON 解析最大重试次数（默认 5）
MAX_COORDINATOR_RETRIES=5
MAX_MODELER_RETRIES=5

# Writer 最大重试次数（代码中默认 3）
# Coder 已有 MAX_RETRIES 配置
```

### 5.2 Fallback LLM

```env
# 协调者 Fallback
FALLBACK_COORDINATOR_API_KEY=sk-yyy
FALLBACK_COORDINATOR_MODEL=gpt-4o-mini
FALLBACK_COORDINATOR_BASE_URL=https://api.openai.com/v1
FALLBACK_COORDINATOR_MAX_TOKENS=4096

# 建模手 Fallback
FALLBACK_MODELER_API_KEY=sk-yyy
FALLBACK_MODELER_MODEL=gpt-4o-mini

# 代码手 Fallback
FALLBACK_CODER_API_KEY=sk-yyy
FALLBACK_CODER_MODEL=gpt-4o-mini

# 写作手 Fallback
FALLBACK_WRITER_API_KEY=sk-yyy
FALLBACK_WRITER_MODEL=gpt-4o-mini
```

仅当 `API_KEY` 和 `MODEL` 均配置时才创建 Fallback 实例。

### 5.3 评估器

```env
# 独立的便宜模型，不复用 Writer LLM
EVALUATOR_API_KEY=sk-xxx
EVALUATOR_MODEL=gpt-4o-mini
EVALUATOR_BASE_URL=https://api.openai.com/v1
```

未配置时跳过评估和 Feedback Rerun。

### 5.4 Feedback Rerun

```env
# 最大 Feedback 重跑轮数（默认 2）
MAX_FEEDBACK_ROUNDS=2

# 评估通过阈值，0-1（默认 0.6）
EVALUATION_THRESHOLD=0.6
```

---

## 六、新增配置项汇总

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `MAX_COORDINATOR_RETRIES` | 5 | Coordinator JSON 解析最大重试次数 |
| `MAX_MODELER_RETRIES` | 5 | Modeler JSON 解析最大重试次数 |
| `FALLBACK_COORDINATOR_API_KEY` | None | Coordinator Fallback API Key |
| `FALLBACK_COORDINATOR_MODEL` | None | Coordinator Fallback 模型 |
| `FALLBACK_COORDINATOR_BASE_URL` | None | Coordinator Fallback Base URL |
| `FALLBACK_COORDINATOR_MAX_TOKENS` | None | Coordinator Fallback 最大 Token |
| `FALLBACK_MODELER_API_KEY` | None | Modeler Fallback API Key |
| `FALLBACK_MODELER_MODEL` | None | Modeler Fallback 模型 |
| `FALLBACK_MODELER_BASE_URL` | None | Modeler Fallback Base URL |
| `FALLBACK_MODELER_MAX_TOKENS` | None | Modeler Fallback 最大 Token |
| `FALLBACK_CODER_API_KEY` | None | Coder Fallback API Key |
| `FALLBACK_CODER_MODEL` | None | Coder Fallback 模型 |
| `FALLBACK_CODER_BASE_URL` | None | Coder Fallback Base URL |
| `FALLBACK_CODER_MAX_TOKENS` | None | Coder Fallback 最大 Token |
| `FALLBACK_WRITER_API_KEY` | None | Writer Fallback API Key |
| `FALLBACK_WRITER_MODEL` | None | Writer Fallback 模型 |
| `FALLBACK_WRITER_BASE_URL` | None | Writer Fallback Base URL |
| `FALLBACK_WRITER_MAX_TOKENS` | None | Writer Fallback 最大 Token |
| `EVALUATOR_API_KEY` | None | 评估器 API Key |
| `EVALUATOR_MODEL` | None | 评估器模型 |
| `EVALUATOR_BASE_URL` | None | 评估器 Base URL |
| `MAX_FEEDBACK_ROUNDS` | 2 | 最大 Feedback 重跑轮数 |
| `EVALUATION_THRESHOLD` | 0.6 | 评估通过阈值（0-1） |

---

## 七、前端 SystemMessage 事件

所有新增事件通过现有 `SystemMessage(type=warning/info/error)` 机制发送到前端：

| 事件 | 消息示例 | type |
|------|----------|------|
| Hand Off 触发 | 协调者主模型失败(ValueError)，正在切换备用模型... | warning |
| Coder Hand Off（响应） | 代码手主模型失败，正在切换备用模型... | warning |
| Coder Hand Off（异常） | 代码手主模型异常(TimeoutError)，正在切换备用模型... | warning |
| Writer 重试 | 写作手执行出错，正在重试(1/3)... | warning |
| Writer 软降级 | 写作手超过最大重试次数(3)，最后错误: XXX | error |
| 评估结果（通过） | [评估] ques1 代码手评分: 0.85 (通过) | info |
| 评估结果（未通过） | [评估] ques1 写作手评分: 0.40 (未通过) | warning |
| Feedback 重跑 | 写作手 ques1 评估未通过(score=0.40)，注入反馈重跑... | warning |

---

## 八、工作流执行流程（升级后）

```
1. 初始化 LLM（主模型 + Fallback + 评估器）
2. CoordinatorAgent 解析题目
   └─ 失败 → Hand Off 到 Fallback → 仍失败则抛异常
3. ModelerAgent 制定方案
   └─ 失败 → Hand Off 到 Fallback → 仍失败则抛异常
4. 创建代码沙盒环境
5. 循环每个子任务（solution_flows）:
   a. CoderAgent 求解
      └─ 失败/异常 → Hand Off 到 Fallback
      └─ Feedback: 评估不通过 → 拼接反馈 → 新建 Agent 重跑（最多 N 轮）
   b. WriterAgent 撰写对应章节
      └─ 失败/异常 → Hand Off 到 Fallback
      └─ Feedback: 评估不通过 → 拼接反馈 → 新建 Agent 重跑（最多 N 轮）
   c. Evaluator 评估（Shadow Mode，只记录不触发重跑）
6. 关闭代码沙盒
7. WriterAgent 撰写剩余章节（带 Feedback + Hand Off）
8. 保存结果
```

---

## 九、依赖变更

无新增依赖。所有功能基于现有 `litellm`、`pydantic`、`redis` 实现。
