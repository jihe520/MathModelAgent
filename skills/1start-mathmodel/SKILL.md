---
name: 1start-mathmodel
description: "数学建模竞赛工作流入口。用于启动完整建模流程：询问用户偏好，生成 plan.md 和 todo.md，并按阶段调用赛题分析、建模、代码与图表、流程图、论文撰写、验证验收及 AI 使用披露等 skills。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, WebSearch, WebFetch
---

# 数学建模工作流

本 skill 是数学建模竞赛项目的总控入口。它不替代后续阶段 skill，而是负责启动流程、询问偏好、记录决策、生成计划，并按顺序调用各阶段 skill。

## 数学建模规范参考

如需领域判断，读取 `../_references/math_modeling_norms.md`。该文件只提供数学建模基本规范和防错知识，不改变本 skill 的阶段顺序和产出约定。

## 国赛识别与强制披露

- 用户选择 `CHINA`、国赛、CUMCM 或全国大学生数学建模竞赛时，立即将任务标记为国赛，并强制加载 `7ai-disclosure`。
- 明确为其他赛事时，不生成国赛专用的 `AI 工具使用详情.pdf`。
- 无法判断赛事时，在开始阶段询问一次赛事类型，不得等到论文完成后再判断。
- 桌面 Agent 正在参与论文生成时，视为实际使用了 AI，不得走“全程未使用 AI”分支。

## 必须产出

在当前工作目录中创建或更新以下文件：

- `plan.md`：整体流程方案、建模方向、阶段顺序、预期产物和风险控制。
- `todo.md`：具体待办事项列表，记录每个阶段的任务和状态。
- 国赛任务的 `reports/AI_USAGE_LOG.md`：赛中持续维护并在终检时自动归纳的 AI 工具使用过程记录。

## 工作流

### 1. 询问用户偏好 AskUserQuestions

在规划前，只询问会实质影响流程的问题。问题要少而关键。

优先询问（按重要性排序）：

1. **排版引擎**：Typst 还是 LaTeX？— 决定 5writing 使用哪套模板和编译命令。两套引擎均覆盖全部模板（14 中 + 3 英）。Typst 使用 `typst` 命令编译；LaTeX 使用 `xelatex` 命令编译（需跑两遍解决交叉引用）。
2. **竞赛类型**：国赛/华为杯/华中杯/MCM/...— 决定模板选择，见 5writing 的模板族清单。
3. **论文语言**：中文/英文 — MCM/ICM/COMAP 强制英文，其他默认中文。
4. **子问题数量是否已知**：影响章节文件生成数量。若未知，由 2analysis-modeling 阶段根据题面确定。

将用户的选择记录到 `plan.md` 的"方案"小节中。


### 2. 制定方案

按以下结构编写 `plan.md`：

```markdown
# 方案

要依次调用这些 skill，按照里面要求完成任务。

用户偏好：
- 排版引擎：<Typst / LaTeX>
- 竞赛类型：<国赛 / 华为杯 / MCM / ...>
- 论文语言：<中文 / 英文>
- 子问题数量：<已知 N 个 / 待分析确定>

workflow:
   step      skills
1. 赛题分析与建模设计 - `2analysis-modeling`
2. 编程实现和图表生成 - `3coding-visual`
3. 流程与架构图绘制 - `4drawio`
4. 竞赛论文撰写 - `5writing`
5. 验证和验收 - `6verity`
6. AI 使用详情终检与生成 - `7ai-disclosure`（仅国赛强制）
```

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
│   └── AI_USAGE_LOG.md               # 国赛全程: AI 使用记录（7ai-disclosure）
├── code/                        # 2: 代码（3coding-visual）
│   ├── problem1.py
│   ├── problem2.py
│   ├── problem3.py               # 问题的数量应该更具题目动态调整
│   ├── ... 
│   └── utils.py
├── results/                     # 2: 结果记录（3coding-visual）
├── figures/                     # 2+3: 所有图表（3coding-visual + 4drawio）
│   ├── *.pdf                    #     数据图 + 非数据图 PDF
│   ├── *.drawio                 #     非数据图源文件
├── paper/                       # 4: 论文（5writing）
│   ├── main.typ / main.tex      #     论文主文件（按用户选择的引擎）
│   └── sections/                #     各节文件（.typ 或 .tex）
└── supporting_materials/        # 6: AI 使用支撑材料（确有使用 AI 时）
    ├── AI 工具使用详情.tex
    └── AI 工具使用详情.pdf
```

方案必须明确每个阶段由哪个下游 skill 负责，以及该阶段应产出什么文件。

### 3. 生成待办

将 `todo.md` 写成阶段性 checklist，格式如下：

```markdown
# 待办事项

- [ ] 1. 赛题分析与建模设计 - `2analysis-modeling`
- [ ] 2. 编程实现和图表生成 - `3coding-visual`
- [ ] 3. 流程与架构图绘制 - `4drawio`
- [ ] 4. 竞赛论文撰写 - `5writing`
- [ ] 5. 验证和验收 - `6verity`
- [ ] 6. AI 使用详情终检与生成 - `7ai-disclosure`（仅国赛强制）
```

每完成一个阶段，都要更新 `todo.md` 中对应任务的状态。

### 4. 依次执行阶段

按以下顺序调用下游 skills：

| 阶段 | Skill | 作用 | 主要产物 |
| --- | --- | --- | --- |
| 赛题分析与建模设计 | `2analysis-modeling` | 解析题意、识别变量/约束/数据/评价指标，并建立数学模型、目标函数、约束条件和求解策略。 | `ANALYSIS_MODELING_REPORT.md` |
| 编程实现和图表生成 | `3coding-visual` | 实现可复现代码，运行实验，生成结果表和多种多样的图表。 | `code/`, `results/` ,  `RESULTS_REPORT.md`, `figures/图表` |
| 流程与架构图绘制 | `4drawio` | 在论文确实需要时，绘制方法流程图、架构图和非数据型概念图。 | `figures/*.drawio`, `figures/*.pdf`, `DRAWIO_REPORT.md` |
| 竞赛论文撰写 | `5writing` | 基于分析、建模、代码结果和图表撰写最终竞赛论文，并按章节直接插入图表。 | `paper/` |
| 验证和验收 | `6verity` | 检查可复现性、一致性、产物完整性、格式规范和提交就绪状态。 | `VERIFY_REPORT.md` |
| AI 使用详情终检与生成（仅国赛强制） | `7ai-disclosure` | 校验全过程记录，生成并验收赛事要求的 AI 使用支撑材料。 | `AI_USAGE_LOG.md`, `AI 工具使用详情.pdf` |

## AI 使用记录衔接

以下规则只对国赛任务强制执行：

1. 启动时加载 `7ai-disclosure`，从其模板初始化 `reports/AI_USAGE_LOG.md`。优先根据本次任务的真实模型配置创建工具条目；无法获得版本元数据时写“运行环境未提供具体版本”。
2. `2analysis-modeling`、`3coding-visual`、`4drawio`、`5writing` 和 `6verity` 每个阶段结束后，立即调用 `7ai-disclosure record`，根据真实对话、模型配置和产物追加记录；不得等到赛后凭记忆补造。
3. `6verity` 首先完成论文验收并得到 `PAPER_PASS`。此状态只表示论文通过，不能表示整个国赛提交包已经完成。
4. 随后调用 `7ai-disclosure finalize`。它根据本次会话、文件、运行结果和验收记录自动归纳并脱敏，不为填写详情另行询问队员。
5. 自动归纳只能陈述有证据的采纳、迭代修正和核验；没有人工修改证据时省略该句，不得补造人工经历。通过最终校验后运行确定性生成脚本。
6. 只有 `paper/main.pdf` 与名称完全一致的 `supporting_materials/AI 工具使用详情.pdf` 都存在并通过检查，才把 `todo.md` 的最后一步标记完成，并在 `reports/VERIFY_REPORT.md` 写最终 `PASS`。

若不是桌面 Agent 参与生成、且队伍能够确认全程未使用任何 AI，才允许不生成空白详情 PDF，并在验收报告中写明确认依据。

## 阶段边界

- `3coding-visual` 负责生成所有依赖计算结果或实验输出的数据图表。
- `4drawio` 只负责概念图、算法流程图、架构图、路线图等非数据型图示。
- 不要让 `4drawio` 重复绘制 `3coding-visual` 已经生成的统计图或数据图。
- `5writing` 负责决定图表在论文中的位置，并按所选引擎写入图表代码：
  - Typst：`#figure(image("../../figures/xxx.pdf", width: 85%), caption: [...])`
  - LaTeX：`\begin{figure}[H]\centering\includegraphics[width=0.85\textwidth]{../../figures/xxx.pdf}\caption{...}\label{fig:xxx}\end{figure}`
- 不要让 `5writing` 编造数值结论。论文中的数值必须来自 `RESULTS_REPORT.md`、结果表或已生成图表的数据。
