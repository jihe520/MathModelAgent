---
name: 7ai-disclosure
description: "全国大学生数学建模竞赛 AI 工具使用过程记录与支撑材料生成。用于在各建模阶段记录工具、用途、提示过程、采纳修改和人工核验，并在赛后生成及验收“AI 工具使用详情.pdf”。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# AI 工具使用记录与详情生成

本 skill 有 `record` 和 `finalize` 两种模式。它只整理真实发生的 AI 使用，不替参赛队补造记录，也不自动宣称合规。

## 合规边界

记录至少覆盖：工具名称及版本/模型、用途及阶段、主要提示方式和过程、采纳情况及人工修改与核验。核心建模与分析必须由参赛队主导，AI 贡献必须由队员审查和验证。

禁止写入 API 密钥、访问令牌、账号密码、完整聊天记录、模型私有思维链或与申报无关的个人信息。典型交互只保留代表性提示与结果摘要。

## record：分阶段记录

1. 若 `reports/AI_USAGE_LOG.md` 不存在，从 `templates/AI_USAGE_LOG.md` 复制创建。
2. 查看本阶段真实对话、报告、代码、结果和验证产物，复用已有 `TOOL-xx`；新工具使用下一个连续编号。
3. 在“分阶段使用记录”下追加一个 `AI-xxx` 记录，写清用途、提示方法、使用过程、采纳、人工修改、人工核验和证据文件。
4. 在需要时补充一条代表性典型交互或未采纳的重要建议。不要逐轮复制聊天。
5. 无法从证据确认的内容必须写 `待队员确认`；不得推断队员已经完成审核。
6. 运行结构校验：

```bash
python "<本 skill 目录>/scripts/validate_ai_usage_log.py" reports/AI_USAGE_LOG.md --mode record
```

校验错误必须修复；允许保留明确标记的 `待队员确认`，供队员后续补齐。

## finalize：生成支撑材料

1. 先运行最终校验：

```bash
python "<本 skill 目录>/scripts/validate_ai_usage_log.py" reports/AI_USAGE_LOG.md --mode finalize
```

只要仍有 `待队员确认`、缺项、无效引用、未完成人工审查或疑似密钥，立即停止，不生成“已完成”的 PDF。

2. 创建 `supporting_materials/`，将 `templates/AI工具使用详情模板.tex` 复制为 `supporting_materials/AI 工具使用详情.tex`。
3. 依据日志填写模板；工具和阶段记录数量按实际增减。不得把模板中的示例或占位符当成事实。
4. 在 `supporting_materials/` 中用 XeLaTeX 编译两遍：

```bash
xelatex -interaction=nonstopmode -halt-on-error "AI 工具使用详情.tex"
xelatex -interaction=nonstopmode -halt-on-error "AI 工具使用详情.tex"
```

5. 必须得到名称完全一致的 `supporting_materials/AI 工具使用详情.pdf`。
6. 检查 PDF 非空、可提取文本、页面为 A4；逐页渲染检查表格越界、重叠、裁切、乱码和异常空白。
7. 在 `reports/VERIFY_REPORT.md` 记录日志校验、编译、文件名、页数、A4、文本层与视觉检查结果。

如果队伍确认全程未使用 AI，不生成空白详情 PDF；在验收报告中记录“未使用 AI，按赛事要求无需提交该支撑材料”，并保留队员确认依据。
