---
name: 5writing
description: "数学建模竞赛论文撰写阶段，支持 Typst 和 LaTeX 双引擎。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和 figures/*.pdf 选择比赛模板、排版引擎、组织章节，并在论文正文中按章节直接插入图表。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 竞赛论文撰写（Typst / LaTeX）

本 skill 承接 `3coding-visual` 和 `4drawio`。前序阶段只提供真实数据、图表 PDF 和记录文件；本阶段负责选择比赛模板和排版引擎、组织论文结构，并决定每张图表放入哪个章节。

**Typst 引擎**下可调用 typst-author skill 学习 typst 写法；**LaTeX 引擎**参考本文件末尾的"LaTeX 写作要点"小节。

## 数学建模规范参考

如需领域判断，读取 `../_references/modeling_core_norms.md` 中的“通用论文写作原则”“图表与可视化”和“非数据图工具选择”小节；若当前赛题为 CUMCM 或需核对赛制要求，再读取 `../_references/competition_rules/cumcm.md`。该文件仅作为规范知识库，论文结构仍按比赛模板和当前赛题内容决定，不作为固定模板强制要求。

## 写作证据约束（核心原则）

- 模型设计逻辑、变量定义、假设和理论路线优先读取 `reports/ANALYSIS_MODELING_REPORT.md`。
- 实际实现模型、参数、实验结果、benchmark、约束校验、敏感性/稳健性结论，以 `reports/RESULTS_REPORT.md` 和真实结果文件为准。
- 图表只引用真实存在、可追溯的 `figures/` 文件。
- 若分析阶段推荐路线与代码阶段最终实际实现存在偏差，以 `RESULTS_REPORT.md` 中明确记录的最终实际实现为论文结果依据，并合理说明必要偏差；不得把未实现的推荐路线写成已经实现。
- 论文中的关键结果必须能追溯到 `RESULTS_REPORT.md` 或真实结果文件；允许正常四舍五入以统一小数位数，但不得改变计算口径、重新计算出与结果报告不同的值，或让摘要、正文、表格、图表采用相互矛盾的精度/口径。
- 题面事实不得改写成未经支持的新事实；建模假设必须明确作为假设表达；只有经过 3coding 验证的结果才能作为确定性结果陈述；尚未验证的推测不得包装成实验结论。
- 只引用真实存在且已核验基本书目信息的来源；禁止编造作者、题名、期刊/会议、年份、DOI 或其他引用信息。若某项外部研究性主张无法核验，不得用无来源措辞绕过核验，应核验来源、降为无需该来源即可成立的普通表述，或删除。
- 每张进入论文的图表必须服务至少一个明确论证或结果说明；caption 必须真实描述图意，不得夸大图中没有体现的结论。
- 摘要在正文、结果、图表和关键数字基本稳定后生成；摘要中的方法、核心结果和关键数字必须从已验证正文及结果中提炼，不从分析阶段尚未验证的推荐方案直接生成结果性摘要。
- 对赛事格式要求只使用已确认的官方规则或 `_references/competition_rules/cumcm.md` 中已记录内容；不主动补造未确认的当年比赛规则；不因美化或个人偏好擅自删除、改变模板要求保留的封面、编号、页眉页脚、摘要页或其他结构。
- 默认复用 `3coding-visual` 已生成的报告、结构化结果、诊断数据和图表，不为写作重新拟合模型或重跑昂贵计算。只有结果缺失、结果之间冲突，或现有证据不足以支持必须写入的核心结论时，才回退 `3coding-visual`；不得以“重新算一遍”替代对已有产物的读取和组织。

## 模板族

本技能内捆绑的模板位于：

```text
templates/zh/<竞赛>/main.typ         # Typst 模板
templates/zh/<竞赛>-latex/main.tex   # LaTeX 模板
templates/en/<竞赛>/main.typ         # Typst 模板
templates/en/<竞赛>-latex/main.tex   # LaTeX 模板
```

- 选择排版引擎后，所有章节文件、图片路径和插图语法必须按同一引擎保持一致。
- 保留模板要求保留的封面、页眉页脚、编号、摘要页等结构；不自行删改比赛模板的关键格式元素。
- 若模板与当年官方规则存在冲突，应标记并进入验收，而不是自行猜测处理。
- CUMCM 必须以 `../_references/competition_rules/cumcm.md` 的 2026 官方规则覆盖旧模板默认值；不得生成正文目录，并须区分纸质版前两页、电子版论文、正文页数、附录与独立支撑材料。

## 工作流

### 步骤 0：确定排版引擎

撰写论文前先读取 `plan.md` 的"用户偏好 → 排版引擎"字段。若其中已明确记录有效值 `LaTeX` 或 `Typst`，直接沿用，不再重复询问。只有 `plan.md` 缺失、该字段缺失或值无效，或者用户主动要求变更引擎时，才询问用户。引擎决定后续所有步骤（模板路径、章节文件扩展名、图片插入语法、编译命令）。

需要询问时，使用 AskUserQuestion 工具向用户询问："撰写论文使用哪种排版引擎？"

- 选项 1：LaTeX（xelatex 编译，数学建模竞赛主流，模板已全部就绪）— 推荐选项放第一位
- 选项 2：Typst（typst 编译，调用 typst-author skill 辅助写作）

- 若需要询问且用户未明确指定或跳过，**默认使用 LaTeX**。
- 若用户主动要求变更引擎，以本次选择为准，并同步更新 `plan.md` 中的排版引擎字段。

根据确定的引擎选择对应模板族：

- **Typst 引擎**：使用 `templates/<lang>/<竞赛>/main.typ`，调用 typst-author skill。编译命令 `typst compile main.typ`。
- **LaTeX 引擎**：使用 `templates/<lang>/<竞赛>-latex/main.tex`，xelatex 编译（中文和英文均需跑两遍解决交叉引用）。编译命令 `xelatex -interaction=nonstopmode main.tex`（执行两次）。

**后续步骤中的所有代码示例、文件扩展名、图片插入语法都必须按所选引擎选择对应版本，不要混用。**

### 步骤 1：选择语言和模板


除非用户明确要求中文，否则 MCM/ICM/COMAP 一律使用英文。所有中文竞赛名称使用中文。

模板键示例（Typst 引擎）：

```text
长三角 -> zh/changsanjiao
APMCM 英文版 -> en/apmcm
全国赛/国赛/CUMCM -> zh/cumcm
统计建模 -> zh/stats
MCM/ICM/COMAP -> en/mcm
```

模板键示例（LaTeX 引擎）：

```text
全国赛/国赛/CUMCM -> zh/cumcm-latex
MCM/ICM/COMAP -> en/mcm-latex
```

### 步骤 2：准备模板

用以下命令检查捆绑模板是否可访问（`SKILL_DIR` 为本 skill 所在目录）：

**Typst 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>/main.typ" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：直接将 `templates/zh/<竞赛>/` 整目录复制到 `paper/`。这些模板是自包含入口文件，不依赖额外共享样式文件。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 Typst 框架，并在 `paper/` 内注明"重建自 default 结构"。

存在匹配模板时，绝不从零开始写论文。

**LaTeX 模板**：

```bash
ls "$SKILL_DIR/templates/zh/<竞赛>-latex/main.tex" 2>/dev/null && echo "OK" || echo "MISSING"
```

- **文件存在（OK）**：将 `templates/zh/<竞赛>-latex/` 整目录复制到 `paper/`。
- **文件不存在（MISSING）**：说明 skill 未完整安装或在沙箱中，此时依照本 SKILL.md 步骤 3 列出的对应节文件结构，从零重建最小可编译 LaTeX 框架，并在 `paper/` 内注明"重建自 default-latex 结构"。


### 步骤 3：建立证据清单并构建图表规划

在写正文各节之前，必须反查 `reports/ANALYSIS_MODELING_REPORT.md`、`reports/RESULTS_REPORT.md`、`results/`、`figures/`，按顶层子问题建立“已有证据 → 正文落点”清单。至少识别：模型选择依据、数学定义、关键参数或目标函数、求解/训练过程、核心结果、benchmark、诊断与敏感性/稳健性、约束校验、实际解释、分析阶段的 citation needs，以及可用的结果表和图。清单用于防止遗漏，不新增固定报告文件，可保留在工作上下文中。

不是所有中间结果都必须进入论文，但凡支撑模型成立、模型优于基线、结论稳健或建议可执行的重要证据，都必须进入正文、表格、图或附录之一；决定不采用某项已有重要产物时，应确认它与核心论证重复或没有独立论证价值，不能仅因压缩篇幅而丢弃。

在证据清单基础上构建图表规划：

```text
图表规划
fig_roadmap.pdf -> 引言/问题重述
fig_flow_q1.pdf -> 问题一模型构建
fig_flow_q2.pdf -> 问题二模型构建
fig_pipeline.pdf -> 数据预处理/方法节
结果图 -> 对应的结果节
```

图片路径相对于写入该图片的文件：写在 `paper/main.typ` 或 `paper/main.tex` 中通常用 `../figures/xxx.pdf`，写在 `paper/sections/*.typ` 或 `paper/sections/*.tex` 中通常用 `../../figures/xxx.pdf`。

**Typst 引擎**图片插入：

```typst
#figure(
  image("../../figures/fig_q1_error_dist.pdf", width: 85%),
  caption: [问题一预测误差分布],
)
```

**LaTeX 引擎**图片插入：

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{../../figures/fig_q1_error_dist.pdf}
  \caption{问题一预测误差分布}
  \label{fig:q1_error}
\end{figure}
```

英文论文使用英文图注。

### 步骤 4：撰写各节

**以下章节文件名按所选引擎使用 `.typ`（Typst）或 `.tex`（LaTeX）扩展名。** 例如 Typst 引擎用 `1_restatement.typ`，LaTeX 引擎用 `1_restatement.tex`。文件名主体保持一致；具体结构按所选模板规定执行，不要自行重写为其他章节顺序。

正文写作应使用连贯的学术段落。避免在最终论文中出现工作流内部名称，如 `reports/`、`figures/` 或 `CLAUDE.md`。

每个核心模型或顶层子问题必须形成完整、可读的论证链，而不是只给模型名称、一个公式和若干最终数字。正文应按题目实际需要呈现：

1. 为什么选择该模型，候选路线或 benchmark 如何影响选择；
2. 模型的数学定义，变量、假设、关键参数、目标函数与约束的含义；
3. 数据如何进入模型，求解、训练、优化或推断过程如何进行；
4. 核心数值结果及其与 benchmark 的比较；
5. 适用的诊断、误差评估、可行性回代、敏感性或稳健性证据；
6. 结果对题目要求意味着什么、为何可信、有哪些适用边界。

上述内容按模型性质取舍详略，不要求机械使用固定小标题，也不按页数或字数凑量；但不得把 3coding 已完成的关键 benchmark、诊断或稳健性证据压缩成无解释的一句话，或只放图表而不解释其对模型选择和结论的作用。

- 每张进入论文的图表必须服务至少一个明确论证或结果说明；正文应在适当位置引导并解释图表，而不是连续堆图。
- caption 必须真实描述图表内容，不得夸大图中没有体现的结论。
- 图中数字、正文数字和 `RESULTS_REPORT.md` 中对应结果必须口径一致。
- 不为满足数量而插入无实际论证作用的图。

### 步骤 5：参考文献

读取分析阶段的 citation needs，并根据实际正文重新确认最终需要引用的核心方法、非常规指标/标准、赛题外领域事实和外部数据资料。用户已提供可靠文献时优先复用；用户未提供时不要求其必须自行寻找。当前 Agent 具备网页搜索能力且缺少必要来源时，应主动通过实际 Web Search / 网页检索寻找并核验，不能仅凭模型记忆生成完整引用信息；核心方法优先原始论文或公认权威来源。

核验来源依次优先：出版商、期刊、会议官方页面或真实 DOI 页面；作者主页、大学或科研机构仓储中的原始论文；官方教材、标准、政府或权威组织资料；其他可交叉核验的高可信来源。搜索结果页、博客和聚合转载页可用于发现候选，但存在原始来源时不能作为核心书目信息的唯一依据。对实际引用至少核验可获得的题名、作者、年份和期刊/会议/出版社等；DOI、URL 只有实际核验后才写，缺失时宁可省略，不得猜测补全。

必须形成“正文中的外部方法/论断 → 正文 citation → bibliography entry”的可追溯关系。文件名按引擎选择：Typst 用 `paper/references.typ`，LaTeX 用 `paper/references.tex`。不要规定最低篇数，不把未用于正文的资料塞入 bibliography，不给本队实验结果、参数搜索或数值输出错误添加外部引用，也不为普通公式机械引用。若重要 citation need 无法可靠核验，明确保留为 unresolved citation need；核心方法或关键外部事实因此缺乏依据时，不得伪造引用掩盖，应调整正文或作为写作 blocker 交给最终验收。

### 步骤 6：最后撰写摘要或总结

在正文、结果、图表和关键数字基本稳定后撰写中文摘要或英文 Summary Sheet。摘要中的方法、核心结果和关键数字必须从已验证正文及结果中提炼，不从分析阶段尚未验证的推荐方案直接生成结果性摘要。修改正文关键结果后，应同步检查摘要一致性。

摘要完成后，再次逐项对照步骤 3 的证据清单与 `ANALYSIS_MODELING_REPORT.md`、`RESULTS_REPORT.md`、`results/`、`figures/`：确认每个核心模型的选择依据、定义、求解、结果、benchmark、诊断/稳健性和实际解释已有合适正文落点；确认重要图表已被使用并在正文中解释。完成 citation coverage 检查，确认重要 citation needs 已被可靠来源覆盖、正文 citation 与 bibliography 对应，或已明确记录 unresolved citation need。发现缺口时优先补足论证或引用已有产物，不通过重复文字、机械扩页或无价值图表填充。

### 步骤 6.1：CUMCM 格式、AI 声明与支撑材料

CUMCM 项目按年度规则完成以下交付，不把它们混成一份文件：

- 电子版论文第一页为摘要专用页，不含纸质版承诺书和编号专用页；不要目录，正文不超过 30 页，正文后附录页数不限，最终推荐 PDF 不超过 20 MB。摘要原则上不超过一页，摘要、正文、附录均不得含身份、学校或赛区信息。
- 论文附录列出支撑材料文件，并纳入全部完整可运行源程序及必要软件交互命令；确实无程序时使用官方指定说明。与论文分开提交的电子支撑材料按所列清单组织；附录代码、清单、电子支撑材料与论文结果必须一致。
- 读取从 1start 起持续维护的 `reports/AI_USAGE_LOG.md`。本工作流使用 Codex / AI Agent 时，在参考文献之前按官方“已使用”句式生成“AI工具使用声明”，按真实用途替换简要用途，不得声称未使用。
- 根据真实阶段记录整理支撑材料中的 `AI工具使用详情.pdf`，覆盖工具名称/版本或型号、用途和环节、主要提示方式与过程、重要输出的采纳/拒绝/修改及人工核验，可选少量典型交互；不复制完整聊天，也不得在写作末尾凭空重构历史。语言润色按官方“采纳、人工修改和核验主要情况（语言润色除外）”处理，但仍须如实声明使用。
- 支撑材料还应包含实际使用的外部数据资料和必要的大篇幅中间结果；按官方要求打包为不超过 20 MB 的 RAR/ZIP。默认复用现有代码和结果，不为组装支撑材料重新拟合模型。

若 AI 留痕缺失到无法真实生成详情，或核心内容缺少人工确认/核验，不得编造补齐：回到对应责任阶段补充可核验事实，作为 blocker 处理。

### 6.2 最小交接给 6verity

最终 paper 与现有报告应能让 `6verity` 核验：

- 论文入口和使用的模板/引擎；
- 关键模型路线是否与实际实现一致；
- 关键结果和 benchmark 是否可追溯；
- 图表是否真实存在并与正文一致；
- 摘要关键数字是否与正文一致；
- citation needs 是否得到处理，正文 citation、真实来源与 bibliography 是否闭环；
- CUMCM 页面结构、正文/附录/支撑材料边界、AI 声明与 `AI工具使用详情.pdf` 是否符合年度规则并与真实留痕一致；
- 模板关键结构是否保留。

不另增交接报告文件。

## LaTeX 写作要点

以下要点供 **LaTeX 引擎**使用。Typst 引擎请调用 typst-author skill 获取语法帮助。

### 编译命令

```bash
# 中文模板（xelatex，跑两遍解决交叉引用）
xelatex main.tex && xelatex main.tex

# 英文模板（xelatex，同样跑两遍）
xelatex main.tex && xelatex main.tex
```

### 文档结构

```latex
\documentclass[a4paper,12pt]{article}   % 英文
\documentclass[a4paper,12pt]{ctexart}   % 中文

\usepackage{...}   % 宏包加载
\usepackage{graphicx}   % 图片支持
\usepackage{booktabs}   % 三线表
\usepackage{amsmath,amssymb}   % 数学公式
\usepackage{hyperref}   % 交叉引用（需两遍编译）
```

### 图表插入

```latex
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{../../figures/fig_q1.pdf}
  \caption{图注}
  \label{fig:q1}
\end{figure}

% 三线表
\begin{table}[htbp]
  \centering
  \caption{表注}
  \begin{tabular}{ccc}
    \toprule
    \textbf{列1} & \textbf{列2} & \textbf{列3} \\
    \midrule
    数据 & 数据 & 数据 \\
    \bottomrule
  \end{tabular}
\end{table}
```

### 交叉引用

```latex
如图~\ref{fig:q1}所示，...   % 图片引用
式~(\ref{eq:objective}) 给出...   % 公式引用
见第~\pageref{fig:q1} 页   % 页码引用
```

### 数学公式

```latex
行内公式：$f(x) = \sum_{i=1}^n \theta_i \phi_i(x)$

行间公式：
\begin{equation}
  \mathcal{L}(\theta) = \frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2
  \label{eq:objective}
\end{equation}
```

### 章节和强调

```latex
\section{问题重述}
\subsection{问题背景}
\textbf{问题一：} xxx   % 对应 Typst 的 #strong
```
