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

## 工作流

### 步骤 0：确定排版引擎

**撰写论文前必须让用户选择排版引擎。** 引擎决定后续所有步骤（模板路径、章节文件扩展名、图片插入语法、编译命令），选错会导致整篇论文格式错误。

使用 AskUserQuestion 工具向用户询问："撰写论文使用哪种排版引擎？"

- 选项 1：LaTeX（xelatex 编译，数学建模竞赛主流，模板已全部就绪）— 推荐选项放第一位
- 选项 2：Typst（typst 编译，调用 typst-author skill 辅助写作）

询问前先读取 `plan.md` 的"用户偏好 → 排版引擎"字段作为预选项：
- 若 plan.md 已记录引擎选择，向用户确认："检测到之前选择的引擎是 <LaTeX/Typst>，是否沿用？"
- 若 plan.md 不存在或未记录引擎选择，直接询问用户选择。
- 若用户未明确指定或跳过，**默认使用 LaTeX**。

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


### 步骤 3：构建图表规划

在写正文各节之前，根据 `figures/*.pdf`、`reports/RESULTS_REPORT.md`，以及 `reports/DRAWIO_REPORT.md`（如果存在）构建图表规划：

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

- 每张进入论文的图表必须服务至少一个明确论证或结果说明；正文应在适当位置引导并解释图表，而不是连续堆图。
- caption 必须真实描述图表内容，不得夸大图中没有体现的结论。
- 图中数字、正文数字和 `RESULTS_REPORT.md` 中对应结果必须口径一致。
- 不为满足数量而插入无实际论证作用的图。

### 步骤 5：参考文献

只使用真实存在且已核验基本书目信息的参考文献。文件名按引擎选择：Typst 用 `paper/references.typ`，LaTeX 用 `paper/references.tex`。

- 禁止编造作者、题名、期刊/会议、年份、DOI 或其他引用信息。
- 若某项外部研究性主张需要文献支持但当前无法核验来源，不得通过写成“相关研究表明”等无来源措辞绕过核验；应核验来源、降低为无需该来源即可成立的普通表述，或删除。
- 不为了增加参考文献数量而添加无实际作用的引用。

### 步骤 6：最后撰写摘要或总结

在正文、结果、图表和关键数字基本稳定后撰写中文摘要或英文 Summary Sheet。摘要中的方法、核心结果和关键数字必须从已验证正文及结果中提炼，不从分析阶段尚未验证的推荐方案直接生成结果性摘要。修改正文关键结果后，应同步检查摘要一致性。

### 6.1 最小交接给 6verity

最终 paper 与现有报告应能让 `6verity` 核验：

- 论文入口和使用的模板/引擎；
- 关键模型路线是否与实际实现一致；
- 关键结果和 benchmark 是否可追溯；
- 图表是否真实存在并与正文一致；
- 摘要关键数字是否与正文一致；
- 参考文献是否真实；
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
