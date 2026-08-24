---
name: 7ai-disclosure
description: "全国大学生数学建模竞赛 AI 工具使用过程记录与支撑材料生成。国赛论文工作流启动时自动启用，持续记录真实工具、用途、提示过程、采纳修改和人工核验，并在一次性人工确认后生成四部分简版“AI 工具使用详情.pdf”。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# AI 工具使用记录与详情生成

本 skill 有 `record` 和 `finalize` 两种模式。国赛任务由 `1start-mathmodel` 强制调用；其他赛事只在用户明确要求时使用。它只整理真实发生的 AI 使用，不补造记录，也不自动宣称合规。

桌面 Agent 正在参与国赛论文生成时，视为实际使用了 AI，不得生成“全程未使用 AI”的空记录。

## 输出约束

最终 PDF 只包含标题、页眉页码和以下四个一级部分：

1. 所用 AI 工具名称、版本或型号；
2. 具体使用目的和环节；
3. 主要提示方式与使用过程说明，可附非表格的典型交互示例；
4. 对 AI 输出的采纳、人工修改和核验的主要情况，语言润色除外。

第一部分使用“编号、AI 工具名称、版本或型号”三列表格；第二部分使用“工具编号、使用环节、具体使用目的”三列表格。工具编号采用 `TOOL-01`、`TOOL-02` 等，第二至第四部分必须引用对应编号。禁止写入密钥、密码、完整聊天记录、模型私有思维链或无关个人信息。

## record：持续记录

1. 若 `reports/AI_USAGE_LOG.md` 不存在，从 `templates/AI_USAGE_LOG.md` 复制创建。
2. 查看当前阶段的真实对话、运行配置和产物。工具名称与模型优先读取本次任务的真实配置或响应元数据；不可获得时写“待队员确认”，不得根据供应商或界面猜测版本。
3. 复用已有 `TOOL-xx`；新工具使用下一个连续编号，编号必须从 `TOOL-01` 开始连续递增。
4. 追加一个连续编号的 `AI-xxx` 记录，写明工具编号、使用环节、具体目的、提示方式、使用过程、采纳情况、人工修改、人工核验和证据文件。
5. 仅用于语言润色时，将“是否仅用于语言润色”写为“是”，人工修改和核验字段可以删除或写“不适用（仅语言润色）”。
6. 典型交互为可选项；如记录，只保留代表性提示、输出和队员处理摘要，不复制全部对话。
7. 无法确认的内容写 `待队员确认`，不得推断队员已经审核。
8. 每个国赛阶段结束后立即运行记录校验：

```bash
PYTHON_BIN="$(command -v python3 || command -v python)"
"$PYTHON_BIN" "<本 skill 目录>/scripts/validate_ai_usage_log.py" reports/AI_USAGE_LOG.md --mode record
```

## finalize：生成支撑材料

1. 先检查日志，将所有 `待队员确认` 和只能由队员确认的内容合并为一条消息。只询问一次，集中确认工具版本、AI 输出采纳情况、非语言润色类人工修改和人工核验方法与结果。
2. 根据队员的一次回复更新相应字段和 `当前状态`。若回复仍缺少必填信息，列出缺项并停止；不得连续拆成多轮零散问题，也不得自行补造。
3. 运行最终校验：

```bash
PYTHON_BIN="$(command -v python3 || command -v python)"
"$PYTHON_BIN" "<本 skill 目录>/scripts/validate_ai_usage_log.py" reports/AI_USAGE_LOG.md --mode finalize
```

存在待确认、缺项、无效工具引用、未确认记录或疑似密钥时停止生成。

4. 最终校验通过后，必须调用确定性生成脚本，不再让模型自由复制或手填模板：

```bash
"$PYTHON_BIN" "<本 skill 目录>/scripts/generate_ai_usage_pdf.py" \
  reports/AI_USAGE_LOG.md \
  --output-dir supporting_materials
```

生成脚本负责日志到四部分模板的映射、LaTeX 转义、XeLaTeX 两遍编译、Tectonic 回退，以及文件名、非空、A4、文本层、规定部分、占位符和疑似密钥检查。典型交互使用正文段落，不使用表格；证据文件和内部状态只用于校验，不写入最终 PDF。

5. 必须得到名称完全一致的 `supporting_materials/AI 工具使用详情.pdf`，再逐页检查是否存在越界、重叠、裁切或乱码。
6. 在 `reports/VERIFY_REPORT.md` 记录一次性确认、日志校验、编译、程序化 PDF 检查和逐页视觉检查结果。
7. 只有 `paper/main.pdf` 与 `supporting_materials/AI 工具使用详情.pdf` 均通过检查，国赛提交包才能标记最终 `PASS`。

仅当本任务并非由桌面 Agent 生成、且队伍确认全程未使用任何 AI 时，不生成空白详情 PDF，并在验收报告中记录确认依据。
