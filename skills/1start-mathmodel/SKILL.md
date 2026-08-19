---
name: 1start-mathmodel
description: "数学建模竞赛工作流入口。用于启动完整建模流程：询问用户偏好，生成 plan.md 和 todo.md，并按阶段调用赛题分析、建模、代码与图表、流程图、论文撰写、验证验收等 skills。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 数学建模工作流

本 skill 是数学建模竞赛项目的总控入口。它不替代后续阶段 skill，而是负责启动流程、询问偏好、记录决策、生成计划，并按顺序调用各阶段 skill。

## 数学建模规范参考

如需领域判断，优先读取 `../_references/modeling_core_norms.md` 和 `../_references/model_catalog.md`。前者提供长期稳定的数学建模原则、题型防错和结果一致性要求；后者提供模型候选工具箱，不作为机械选型规则。若当前任务涉及 CUMCM 赛制要求，再读取 `../_references/competition_rules/cumcm.md`。这些文件仅提供规范参考，不改变本 skill 的阶段顺序和产出约定。

## 必须产出

在当前工作目录中创建或更新以下文件：

- `plan.md`：整体流程方案、建模方向、阶段顺序、预期产物和风险控制。
- `todo.md`：具体待办事项列表，记录每个阶段的任务和状态。

## 工作流

### 1. 询问用户偏好 AskUserQuestions

在规划前，只询问会实质影响全局流程的问题。问题要少而关键。

优先询问（按重要性排序）：

1. **排版引擎**：Typst 还是 LaTeX？— 决定 5writing 使用哪套模板和编译命令。
2. **竞赛类型**：国赛/华为杯/华中杯/MCM/...— 决定模板和规则来源。
3. **论文语言**：中文/英文 — MCM/ICM/COMAP 强制英文，其他默认中文。

**子问题数量**不作为启动阶段必须询问项。若用户已明确给出，可写入 `plan.md`；否则由 `2analysis-modeling` 根据题面自动识别，不在 1start 阶段强制追问。

不在本阶段询问：具体模型、benchmark、绘图细节、算法参数、以及其他应由下游阶段决定的内容。

将用户的选择记录到 `plan.md` 的"方案"小节中。


### 2. 制定方案

按以下结构编写 `plan.md`，保持轻量：

```markdown
# 方案

用户偏好：
- 排版引擎：<Typst / LaTeX>
- 竞赛类型：<国赛 / 华为杯 / MCM / ...>
- 论文语言：<中文 / 英文>
- 子问题数量：<已知 N 个 / 待分析确定>（可选）

当前阶段：2analysis-modeling
阶段推进：2analysis → 3coding → 4drawio（按需）→ 5writing → 6verity
阻断原则：
- 存在 blocker / 未完成关键 checkpoint 时暂停
- 需要改变模型路线时回退 2analysis
- 实现问题回退 3coding
- 论文表达问题回退 5writing
```

`plan.md` 不做运行日志，也不增加复杂表格或 DAG。

## 项目目录结构

各阶段按此骨架创建和填充文件：

```text
.
├── plan.md                      # 1: 本文件
├── todo.md                      # 1: 待办事项
├── reports/                     # 各阶段文档报告
│   ├── ANALYSIS_MODELING_REPORT.md  # 1: 赛题分析-建模报告（2analysis-modeling）
│   ├── RESULTS_REPORT.md            # 2: 结果报告（3coding-visual）
│   ├── DRAWIO_REPORT.md             # 3: 非数据图说明（4drawio）
│   ├── VERIFY_REPORT.md             # 5: 验收报告（6verity）
├── code/                        # 2: 代码（3coding-visual）
│   ├── problem1.py
│   ├── problem2.py
│   ├── problem3.py               # 问题的数量应该更具题目动态调整
│   ├── ... 
│   ├── utils.py
│   └── outputs/                 #     运行中间产物、调试输出、模型日志、临时计算结果
├── results/                     # 2: 最终或结构化结果数据、关键指标及后续可直接引用的数据文件
├── figures/                     # 2+3: 论文可用图表及必要图源（3coding-visual + 4drawio）
│   ├── *.pdf                    #     数据图 + 非数据图 PDF
│   ├── *.drawio                 #     非数据图源文件
├── paper/                       # 4: 论文（5writing）
│   ├── main.typ / main.tex      #     论文主文件（按用户选择的引擎）
│   └── sections/                #     各节文件（.typ 或 .tex）
```

方案必须明确每个阶段由哪个下游 skill 负责，以及该阶段应产出什么文件。

### 3. 生成待办

将 `todo.md` 写成阶段性 checklist，格式如下：

```markdown
# 待办事项

- [ ] 1. 赛题分析与建模设计 - `2analysis-modeling`
- [ ] 2. 编程实现和图表生成 - `3coding-visual`
- [ ] 3. 非数据图示（按需） - `4drawio`
- [ ] 4. 竞赛论文撰写 - `5writing`
- [ ] 5. 验证和验收 - `6verity`
```

若某阶段 blocked，只在该项后简短备注原因，不增加复杂语法体系。

### 4. 依次执行阶段

按以下顺序调用下游 skills：

| 阶段 | Skill | 作用 | 主要产物 |
| --- | --- | --- | --- |
| 赛题分析与建模设计 | `2analysis-modeling` | 解析题面、识别子问题、确定模型路线、关键假设和验证要求。 | `ANALYSIS_MODELING_REPORT.md` |
| 编程实现和图表生成 | `3coding-visual` | 实现可复现代码、运行实验、输出结果和数据图表。 | `code/`, `results/`, `RESULTS_REPORT.md`, `figures/` |
| 非数据图示（按需） | `4drawio` | 在论文确实需要时，绘制流程图、架构图、路线图等非数据型图示。 | `figures/*.drawio`, `figures/*.pdf`, `DRAWIO_REPORT.md` |
| 竞赛论文撰写 | `5writing` | 基于已验证证据写论文。 | `paper/` |
| 验证和验收 | `6verity` | 最终门禁：一致性、编译、图表、提交状态检查。 | `VERIFY_REPORT.md` |

## 阶段边界

- `3coding-visual` 负责生成所有依赖计算结果或实验输出的数据图表。
- `4drawio` 只负责概念图、算法流程图、架构图、路线图等非数据型图示；不是每道题都必须生成图。
- 若本题不需要非数据型图，可在 `todo.md` 中标记 `done: not needed`，不得为了完成 workflow 强制生成无意义图示。
- `5writing` 负责决定图表在论文中的位置，并按所选引擎写入图表代码：
  - Typst：`#figure(image("../../figures/xxx.pdf", width: 85%), caption: [...])`
  - LaTeX：`\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{../../figures/xxx.pdf}\caption{...}\label{fig:xxx}\end{figure}`
- 不要让 `5writing` 编造数值结论。论文中的数值必须来自 `RESULTS_REPORT.md`、结果表或已生成图表的数据。

## 阶段推进规则（canonical）

1. 当前阶段完成且关键产物存在，才能进入下一阶段。
2. 若当前阶段存在未解决 checkpoint 或 blocker，不得继续推进。
3. 若下游 skill 明确要求回退，则将对应阶段标记为 `blocked`，并回到指定前序阶段处理。
4. `1start-mathmodel` 只负责推进 / 暂停 / 回退，不自行替代下游重新判断模型、结果或论文内容。

关键门槛：

- `2analysis-modeling → 3coding-visual`
  - `ANALYSIS_MODELING_REPORT.md` 已生成。
  - 最终重大模型路线已完成必要确认。
- `3coding-visual → 4drawio / 5writing`
  - `RESULTS_REPORT.md` 与核心结果已生成。
  - 不存在路线级 blocker。
- `4drawio → 5writing`
  - 若本题需要非数据图，则相关图示已完成；若不需要，可直接跳过。
- `5writing → 6verity`
  - `paper/` 已形成可验收论文。
  - 关键结果有证据来源。
- `6verity`
  - `P0 / P1` 未清零时不得标记最终完成。
  - 若需要回退，按 `VERIFY_REPORT.md` 指向的阶段处理。

## 阶段状态

只使用四种状态，不做复杂状态机：

- `pending`
- `in progress`
- `done`
- `blocked`

`blocked` 后直接记录原因，例如：

- `blocked: 等待最终模型路线确认`
- `blocked: 3coding 要求回退 2analysis`
- `blocked: 5writing 缺少可信结果`
- `blocked: 6verity 存在 P0/P1`

`1start-mathmodel` 只负责判断是否推进、暂停或回退，不承担后续阶段的具体判断。

## 读取边界

`1start-mathmodel` 可以检查：

- 阶段产物是否存在；
- 下游报告是否明确存在 blocker / checkpoint / FAIL；
- 是否满足进入下一阶段的最小条件。

但不要：

- 自己重新分析赛题；
- 自己重新评估模型优劣；
- 自己解释数值结果；
- 自己审论文事实。

这些仍由对应下游 skill 负责。
