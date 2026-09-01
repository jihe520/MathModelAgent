# CUMCM Team Runtime Sequencing Protocol

## Codex Runtime Rule

三个 Codex 必须根据当前 Phase 和对应问题 state 判断自己是否拥有执行权限。时间仅为建议，**Gate / state 才是权限依据**。

若当前 Gate 未满足：

- 不得自行假设 Gate 已满足；
- 不得为继续 workflow 而越权产生下游正式 artifact；
- 应报告正在等待的 Gate、负责人及所需正式 artifact。

若人类未说明当前 Phase/state，Codex 应先根据现有正式 artifacts 判断；无法可靠判断时询问人类，不得自行推进完整 workflow。

## Phase 0 — Workspace Ready

**建议时间：比赛开始约 0–15 min**

| 角色 | 当前允许事项 |
|---|---|
| A/B/C | 确认同一赛题和附件、同步同一稳定 `main`、确认各自 Team Role、启动各自 Codex |
| A | 检查赛题文件 |
| B | 仅检查环境与附件可读性 |
| C | 仅准备论文工程与模板 |

本阶段不得正式建模或产生正式结果。

### GATE 0 — WORKSPACE READY

三名队员拥有同一完整赛题/附件，角色与工作区正确。

## Phase 1 — Independent Reading

**建议时间：约 15–45 min**

A/B/C 独立完整读题。Codex 可辅助理解，但不得冻结模型或产生正式结果。

| 角色 | 阅读重点 |
|---|---|
| A | 问题结构、候选模型、建模难点 |
| B | 数据结构、实现风险、计算复杂度 |
| C | 每问要求、论文必须回答的内容、陌生概念 |

### GATE 1 — PROBLEM UNDERSTOOD

三名人类队员都能说明每一问的输入、目标与预期输出。

## Phase 2 — Team Problem Selection

**建议时间：约 45–75 min**

三人共同讨论候选赛题、数据条件、模型可行性、实现难度和论文可解释性。A 主持讨论，但 Codex 不得自行决定最终选题。

### GATE 2 — HUMAN TEAM PROBLEM SELECTION CONFIRMED

最终选题已由三名人类队员共同确认。

## Phase 3 — Formal Analysis + Parallel Preparation

**建议时间：约 75 min–2.5 h**

| 角色 | 当前允许事项 |
|---|---|
| A | 正式执行 1start → 2analysis，形成 modeling artifacts |
| B | 数据 profiling；字段、单位、缺失、异常核对；实现风险探索 |
| C | 建论文骨架；准备符号、references、appendix、supporting-material 结构；撰写已确认的题意和数据说明 |

B 不得提前产生未经 A 冻结路线授权的正式模型结果。C 不得写死尚未冻结的模型与结果。

## Phase 4 — Major Route Checkpoint

**建议时间：约 2.5–3 h**

A 向人类团队说明各问的模型路线、核心假设、benchmark、validation 与主要风险；B 确认可实现性；C 确认论文论证可理解。最终决定由三名人类队员共同作出。

### GATE 3 — MODEL ROUTE FROZEN

只有对应问题通过 Gate 3 后，B 才获得对该问题正式执行 3coding-visual 并产生正式结果的权限。各问题可以分别通过 Gate 3，无须等待全部问题同时冻结。

## Phase 5 — Pipeline Active

**建议时间：约 3–4.5 h 开始**

稳态流水线：

- A：研究下一问；
- B：计算当前已冻结问；
- C：撰写已有正式上游事实的部分。

A → B handoff 必须基于正式 modeling artifact。B 不得依据聊天中的临时想法自行改变正式模型。

## Phase 6 — First Result Handoff

**目标时间：约 4.5–6 h；以 artifact 完成为准，不以时间强制**

B 完成某问后，将正式结果写入：

- `RESULTS_REPORT.md`；
- `results/`；
- `figures/`。

完成正式交接后，该问题才可标记为 **RESULT FROZEN / WRITABLE**。C 只有在此状态下，才能把对应数值、图表与结论作为正式论文事实。A 同时检查结果是否符合模型逻辑。

## Per-question State Machine

约 6 小时后主要按状态推进，而非按固定时间推进：

`MODELING → COMPUTING → WRITABLE → WRITING FROZEN`

| State | 权限含义 |
|---|---|
| **MODELING** | A 尚未冻结路线；B 不得产生正式结果；C 不得写正式模型结果 |
| **COMPUTING** | A 路线已经冻结；B 获得该问的正式计算权限 |
| **WRITABLE** | B 的正式结果已经冻结；C 获得该问的正式结果写作权限 |
| **WRITING FROZEN** | C 已完成该部分，且 A 已审核模型表述、B 已审核数字与图表 |

### Rollback

- 模型、假设或路线问题 → 回到 **MODELING**，由 A 重新工作；
- 代码、数值、solver 或结果问题 → 回到 **COMPUTING**，由 B 重新工作；
- 纯写作问题 → 不改变上游状态，由 C 修复写作。

任何上游 rollback 都使对应下游 artifact 自动成为 **STALE**。在重新通过相应 Gate/state 前，STALE artifact 不得作为正式事实，不得继续向下游交接。

## FINALIZATION MODE

**建议在距离最终提交约 10–14 小时时进入；具体时点由三名人类队员按实际进度确认。**

进入后：

- 不再进行没有明确证据支持的模型升级；
- A 主审模型、假设与论证；
- B 主审代码、结果、图表与复现；
- C 主审论文、引用、格式、appendix 与 supporting materials；
- 执行最终 6verity；
- 只修明确错误与 P0/P1。

6verity PASS 仅表示满足提交条件，不构成 Codex 的自动冻结、提交或上传授权。

### GATE FINAL — HUMAN SUBMISSION FREEZE CONFIRMED

三名人类队员共同确认 submission freeze，并共同确认 `VERIFY_REPORT` 最终提交状态中列明的两个上传文件。
