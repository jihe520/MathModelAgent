---
name: 6verity
description: "数学建模竞赛最终验证和验收阶段，支持 Typst 和 LaTeX 双引擎。用于论文写完后检查章节数量、标题顺序、图表引用、数值一致性、占位符、内部文件泄露、参考文献、代码可复现性、编译和提交就绪状态。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# 验证和验收（Typst / LaTeX）

本 skill 是完整工作流的最后一关。它不重新建模、不生成新结果、不代替写作阶段重写论文；它负责发现硬错误、修复可直接修复的问题，并输出 `reports/VERIFY_REPORT.md`。

## 数学建模规范参考

如需领域判断，读取 `../_references/modeling_core_norms.md` 中的“论文验收与一致性”和“代码实现与结果”小节，并根据需要参考 `../_references/common_failure_cases.md` 中的常见失误案例；若当前任务需要核对 CUMCM 赛制要求，再读取 `../_references/competition_rules/cumcm.md`。该文件仅作为规范知识库，不是固定执行流程；具体目录、入口文件、结果文件和图表目录由当前项目结构决定。

## 阶段边界

- 本阶段负责：结构验收、文本质量门禁、图表引用检查、结果一致性检查、Typst/LaTeX 编译检查、PDF 视觉检查和提交清单。
- 本阶段不负责：重新设计模型、重新跑大规模实验、重新组织整篇论文。
- 发现事实问题时，优先做小范围修复；若需要回到前序阶段，写入 `reports/VERIFY_REPORT.md` 并标记为未通过。

## 事实来源优先级（唯一 canonical）

- `ANALYSIS_MODELING_REPORT.md`：负责模型设计逻辑、变量定义、关键假设和理论路线。
- `RESULTS_REPORT.md` 及真实结果文件：负责最终实际实现模型、参数、数值结果、benchmark、约束校验、敏感性/稳健性结论。
- `paper/`：负责表达上述已验证事实，不作为新的事实来源。
- `6verity`：负责核验一致性和归属，不重新决定事实。

冲突处理：

- 论文与 `RESULTS_REPORT` 不一致 → 判定为 5writing 问题。
- `RESULTS_REPORT` 与分析路线不一致：
  - 若只是实现偏差 → 回 3coding；
  - 若涉及模型类型、关键假设、目标函数或主要约束变化 → 回 2analysis。
- 6verity 不得自行“选一个看起来合理的版本”覆盖冲突；必须保留证据链并回退到正确责任方。

## 输入

由模型先根据当前工作区判断项目布局，再把实际路径传给检查脚本。常见输入包括但不限于：

1. 论文入口文件：`main.typ` 或 `main.tex`。
2. 正文章节目录或正文文件（`.typ` / `.tex`）。
3. 参考文献文件（`references.typ` / `references.tex`）。
4. 前序阶段的分析、建模和结果报告。
5. 图表目录。
6. 可复现代码目录。
7. 编译后的 PDF，或由入口文件生成的 PDF。

若项目使用不同命名，按实际结构传参并在 `reports/VERIFY_REPORT.md` 中说明。

## 工作流程


### Step 1: 运行文本质量门禁

优先运行本 skill 的脚本。脚本按入口文件扩展名自动选择检查逻辑（`.typ` → Typst 检查，`.tex` → LaTeX 检查）：

```bash
set -o pipefail
mkdir -p _tmp
SCRIPT_PATH="<按当前 skill 实际位置确定>/scripts/writing_check.sh"
bash "$SCRIPT_PATH" \
  --paper-dir "$PAPER_DIR" \
  --main "$MAIN_FILE" \
  --sections-dir "$SECTIONS_DIR" \
  --references "$REFERENCES_FILE" \
  --figures-dir "$FIGURES_DIR" \
  --results-file "$RESULTS_FILE" \
  --problem-analysis "$PROBLEM_ANALYSIS_FILE" \
  --all-results "$ALL_RESULTS_FILE" \
  | tee _tmp/writing_check.log
```

如果本 skill 被复制到其他目录，使用实际脚本路径。可以先运行 `bash <script> --help` 查看参数。不要把脚本路径、论文目录或文件名写死在验收逻辑中。

脚本只扫描文本，不生成论文，也不编译 PDF。它的 `FAIL` 属于硬错误，必须修复后重跑。

### Step 2: 章节数量和标题顺序

**Typst 引擎**检查：

- 入口 `.typ` 文件中 `#include("...")` 的数量是否与实际正文结构匹配。
- include 顺序是否符合文件名前缀顺序，例如 `1_...`, `2_...`, `3_...`。
- 每个 section 是否有明确一级标题（`= 标题`，等号后有空格）。
- 标题顺序是否符合所选论文类型。

**LaTeX 引擎**检查：

- 入口 `.tex` 文件中 `\input{...}` 或 `\include{...}` 的数量是否与实际正文结构匹配。
- 章节顺序是否符合文件名前缀顺序。
- 每个 section 是否有 `\section{}` 或对应级别标题。

通用检查（两种引擎）：

- 章节文件是否缺失、重复引用、未被引用。
- 如果题目不是三问，不强行要求三段问题章节；按 `ANALYSIS_MODELING_REPORT.md` 的子问题数量核对。
- 根据 `ANALYSIS_MODELING_REPORT.md` 中识别出的实际子问题数量和目标，检查论文是否逐问形成了对应的方法、结果和结论；不要求机械地按“问题一/二/三”标题匹配，以实际赛题结构为准。
- 若某个关键子问题没有结果或结论，判为 P1，而不是普通写作问题。

### Step 3: 图表和章节匹配

**Typst 引擎**检查：

- 图表目录中的 PDF 是否在正文中被引用。
- `#figure(image(...), caption: [...])` 的图片是否真实存在。图片路径必须相对于 `.typ` 文件。
- 数据图是否放在对应结果/分析章节，非数据流程图是否放在方法/总体思路章节。

**LaTeX 引擎**检查：

- `\includegraphics{}` 引用的图片文件是否真实存在。路径相对于 `.tex` 文件。
- `\caption{}` 是否存在。
- 数据图是否放在对应结果/分析章节。

通用检查（两种引擎）：

- 连续图表之间是否有足够解释文字。
- caption 是否过长、过泛或与图意不一致。
- 图表编号、正文引用和章节语义是否一致。

不要生成 `*_typst_includes.typ` 或 `*_latex_includes.tex`；图表必须直接嵌在对应 section 中。

### Step 4: 写作质量和泄露检查

检查并修复：

- `TODO`、`PLACEHOLDER`、`待补充`、`待续写`、`示例数据` 等占位符。
- 论文正文出现内部工作流文件名、临时目录名、代码目录名或结果 JSON 路径。
- 过多列表式写作（Typst 中大量 `#list`、`enum`，LaTeX 中大量 `\begin{itemize}`、`\begin{enumerate}`）。
- 段落反复以"如图""由图""图 X 展示了"开头。
- 图表后没有解释、公式后没有变量含义、结论只报数不解释。

### Step 5: 数值和结果一致性

检查：

- 最终模型路线与实际实现一致。
- 关键数值与 `RESULTS_REPORT.md` 或真实结果文件一致。
- benchmark（如适用）是否被正确解释。
- 关键约束是否已验证并正确表述。
- 敏感性/稳健性结论是否有真实结果依据。
- 摘要关键数字与正文一致。
- 图表真实存在、被正文引用、caption 与图意一致。
- 未验证内容没有被包装成确定事实。
- 参考文献真实且正文引用能对应。
- 公式中的符号应在符号说明或正文首次出现处解释。

发现数值冲突时，不要自行发明新结果；应回到结果记录或代码输出修正论文。不要把这些扩展成大型逐项审计表；只核验关键证据项和归属关系。

### Step 6: 引用和模板规范

检查：

- 参考文献文件是否存在，或模板是否采用了其他真实参考文献机制。
- 正文引用标记（Typst 的 `@label`/`#super`，LaTeX 的 `\cite{}`）是否能对应到真实参考文献。
- 中文论文 caption、表题、摘要语言保持中文；英文论文保持英文。
- 选定的模板入口是否保留所选比赛模板的必要封面、摘要、编号、页眉页脚或提交格式。
- 不要把模板结构误删成普通空白文档。


### Step 7: 编译

**Typst 编译**：

```bash
command -v typst >/dev/null 2>&1 && typst compile "$MAIN_FILE" "$OUTPUT_PDF"
```

**LaTeX 编译**：

```bash
command -v xelatex >/dev/null 2>&1 && xelatex -interaction=nonstopmode "$MAIN_FILE" && xelatex -interaction=nonstopmode "$MAIN_FILE"
```

xelatex 需跑两遍解决目录和交叉引用。

编译失败必须修复语法、路径、图片引用或模板问题后重跑。编译通过后确认输出 PDF 非空。

### Step 8: PDF 视觉检查

如果模型有视觉能力，必须把编译后的 PDF 每页导出为 PNG 并逐页查看。这个步骤用于发现纯文本扫描和编译器无法发现的版式错误。

优先使用系统已有工具导出页面 PNG；不要为了视觉检查引入沉重依赖。可选命令示例：

```bash
mkdir -p _tmp/pdf-pages
if command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -png -r 160 "$OUTPUT_PDF" _tmp/pdf-pages/page
elif command -v mutool >/dev/null 2>&1; then
  mutool draw -r 160 -o _tmp/pdf-pages/page-%03d.png "$OUTPUT_PDF"
elif command -v magick >/dev/null 2>&1; then
  magick -density 160 "$OUTPUT_PDF" _tmp/pdf-pages/page-%03d.png
else
  echo "No PDF rasterizer found; record visual check as not run."
fi
```

导出后逐页检查：

- 页面是否空白、缺页、页数异常或页面尺寸异常。
- 标题、摘要、正文、页眉页脚、页码是否被裁切或位置明显错误。
- 表格是否超出页边距，单元格文字是否重叠、溢出、被截断。
- 图片、图题、表题、公式、编号是否与正文重叠。
- 公式是否越界，长公式是否压到页边距或下一段文字。
- 列表、段落、脚注、参考文献是否出现异常大空白、重叠或孤立残行。
- 中文/英文/数学符号字体是否明显缺字、乱码或 fallback 异常。
- 封面、摘要页、目录、附录等模板关键页面是否保留比赛要求的视觉结构。

如果是模板转换或已有参考 PDF 的项目，还应将不同引擎的 PDF 都逐页导出 PNG，按页对比版式差异；页数或页面尺寸不一致必须记录为硬错误或明确说明原因。

如果模型没有视觉能力，必须在 `reports/VERIFY_REPORT.md` 中明确写出“未执行视觉检查”的原因，并至少完成 PDF 非空、页数、页面尺寸等可程序化检查。

## 严重级别

采用简洁三档：

### P0：致命 / 提交阻断
包括但不限于：

- 缺少核心文件或入口文件。
- 论文无法编译。
- 图片/图表引用失效。
- PDF 为空、缺页、明显乱码或严重版式破坏。
- 模板关键结构缺失。
- TODO / PLACEHOLDER / 工作流泄漏。
- 直接导致无法提交或严重失真的问题。

### P1：事实或方法一致性错误
包括但不限于：

- 关键数值与 `RESULTS_REPORT` 冲突。
- 最终模型路线与实际实现不一致。
- benchmark、关键约束或敏感性结论被错误描述。
- 未验证结论被写成确定事实。
- 参考文献真实性或正文引用对应错误。
- 摘要与正文关键结果冲突。

### P2：结构、表达和轻度版式问题
包括：

- 图表解释不足。
- caption 不够准确但不改变事实。
- 章节衔接、语言表达、轻微排版问题。
- 非致命的未引用备用图等。

原则：

- P0、P1 必须在最终 PASS 前解决或明确回退处理。
- P2 尽量修，但不能因为 P2 阻塞真正重要的提交节奏。

## 自动修复边界

6verity 可以自行修复的范围仅限：

- 明确的语法/编译错误。
- 图片路径、label、引用路径等确定性错误。
- 标题层级、明显占位符、内部工作流痕迹。
- 不改变事实含义的轻微格式和排版问题。

以下问题不得擅自修改，只能报告并回退：

- 关键数值冲突。
- 模型路线冲突。
- benchmark 结论冲突。
- 关键假设或约束问题。
- 需要重新计算、重新建模或改变事实才能解决的问题。
- 无法确定哪个来源正确的事实性冲突。

### Step 9: 写验收报告

创建 `reports/VERIFY_REPORT.md`，保持简洁：

```markdown
# 验证和验收报告

## 结论
PASS / FAIL

## 问题清单
| 级别 | 问题 | 证据 | 处理动作 | 状态 |
| --- | --- | --- | --- | --- |

## 编译与 PDF
- 编译状态：
- PDF 状态：
- 视觉检查状态：

## 回退事项
- 需要回 5writing：
- 需要回 3coding：
- 需要回 2analysis：

## 最终提交状态
- P0：0 / ...
- P1：0 / ...
- P2：...
- 是否可提交：是 / 否
```

只有当 P0 与 P1 都已解决或明确回退、P2 仅为轻微问题、编译与 PDF 检查完毕时，才写 `PASS`。
