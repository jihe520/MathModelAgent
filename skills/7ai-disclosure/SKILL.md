---
name: 7ai-disclosure
description: "全国大学生数学建模竞赛 AI 工具使用过程记录与支撑材料生成。用于持续记录工具、用途、提示过程、采纳修改和人工核验，并生成四部分简版“AI 工具使用详情.pdf”。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# AI 工具使用记录与详情生成

本 skill 有 `record` 和 `finalize` 两种模式。它只整理真实发生的 AI 使用，不补造记录，也不自动宣称合规。

## 输出约束

最终 PDF 只包含标题、页眉页码和以下四个一级部分：

1. 所用 AI 工具名称、版本或型号；
2. 具体使用目的和环节；
3. 主要提示方式与使用过程说明，可附非表格的典型交互示例；
4. 对 AI 输出的采纳、人工修改和核验的主要情况，语言润色除外。

第一部分使用“编号、AI 工具名称、版本或型号”三列表格；第二部分使用“工具编号、使用环节、具体使用目的”三列表格。工具编号采用 `TOOL-01`、`TOOL-02` 等，第二至第四部分必须引用对应编号。禁止写入密钥、密码、完整聊天记录、模型私有思维链或无关个人信息。

## record：持续记录

1. 若 `reports/AI_USAGE_LOG.md` 不存在，从 `templates/AI_USAGE_LOG.md` 复制创建。
2. 查看当前阶段的真实对话和产物，复用已有 `TOOL-xx`；新工具使用下一个连续编号。
3. 追加一个 `AI-xxx` 记录，写明工具编号、使用环节、具体目的、提示方式、使用过程、采纳情况、人工修改、人工核验和证据文件。
4. 仅用于语言润色时，将“是否仅用于语言润色”写为“是”，人工修改和核验字段可以删除或写“不适用（仅语言润色）”。
5. 典型交互为可选项；如记录，只保留代表性提示、输出和队员处理摘要，不复制全部对话。
6. 无法确认的内容写 `待队员确认`，不得推断队员已经审核。
7. 运行：

```bash
python "<本 skill 目录>/scripts/validate_ai_usage_log.py" reports/AI_USAGE_LOG.md --mode record
```

## finalize：生成支撑材料

1. 运行最终校验：

```bash
python "<本 skill 目录>/scripts/validate_ai_usage_log.py" reports/AI_USAGE_LOG.md --mode finalize
```

存在待确认、缺项、无效工具引用、未确认记录或疑似密钥时停止生成。

2. 将 `templates/AI工具使用详情模板.tex` 复制为 `supporting_materials/AI 工具使用详情.tex`，按日志填写并增删实际工具和记录。
3. PDF 必须严格采用上述四部分；典型交互使用正文段落，不使用表格。证据文件和内部状态用于校验，不写入最终 PDF。
4. 在 `supporting_materials/` 中用 XeLaTeX 编译两遍：

```bash
xelatex -interaction=nonstopmode -halt-on-error "AI 工具使用详情.tex"
xelatex -interaction=nonstopmode -halt-on-error "AI 工具使用详情.tex"
```

5. 必须得到 `supporting_materials/AI 工具使用详情.pdf`，并检查文件非空、A4、文本层及逐页版式。
6. 在 `reports/VERIFY_REPORT.md` 记录日志校验、编译和 PDF 验收结果。

若队伍确认全程未使用 AI，不生成空白详情 PDF，并在验收报告中记录确认依据。
