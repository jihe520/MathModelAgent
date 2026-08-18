---
name: 4drawio
description: "数学建模非数据型图示绘制阶段。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和已有 figures/ 生成技术路线图、子问题求解流程图、模型结构图、数据处理流程图等 DrawIO 图，并导出论文可引用 PDF。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# DrawIO 非数据图示绘制

本 skill 承接 `3coding-visual`。它只负责论文中的**非数据型图示**，例如技术路线图、求解流程图、模型结构图、数据处理流程图、变量关系图、指标体系图等。

## 数学建模规范参考

如需领域判断，读取 `../_references/modeling_core_norms.md` 中的“图表与可视化”和“非数据图工具选择”小节。该文件仅作为规范知识库，不要求为了凑数量生成额外图示，也不替代具体题目的图形需求判断。

## 最高判断原则（canonical rule）

一张非数据图必须解释仅靠正文难以快速理解的结构、关系或流程，否则不生成。

这是本阶段是否生成图的唯一最高判断原则。它必须优先于任何“默认画图模板”和“固定图文件清单”。

## 阶段边界

- 本阶段负责：DrawIO 源文件、非数据图 PDF、图示生成记录。
- 本阶段不负责：折线图、柱状图、散点图、热力图、箱线图、雷达图、灵敏度曲线等数据图。这些由 `3coding-visual` 生成。
- 本阶段不重跑模型、不修改 `code/`，不改写 `reports/RESULTS_REPORT.md` 的数值结论。
- 本阶段不是每道赛题必跑；若当前论文没有值得额外图示说明的结构、关系或流程，则可直接跳过。

## 可选产出与 skip 规则

4drawio 不是每道赛题必跑。若当前论文和已有数据图已足够表达结论与方法，则本阶段可直接 skip。

跳过时，只在 `reports/DRAWIO_REPORT.md` 中简要记录：

```markdown
# 非数据图示报告
## 状态
not needed
## 图示清单
| 文件 | 类型 | 用途 | 导出状态 |
| --- | --- | --- | --- |
## 备注
- 状态：not needed
- 原因：正文和现有数据图已足够表达
```

不得为了完成 workflow 强制生成技术路线图、流程图或架构图。总体技术路线图只是候选图类型之一，只有在确实提升理解时才生成。

读取这些文件的目的不是提取数据作图，而是理解论文方法、章节结构、子问题关系和已有图表，避免重复，并在确有需要时补足非数据图。

## 工作流程

### Step 1: 盘点已有图表和需求

先读取以下文件（存在则读取）：`reports/ANALYSIS_MODELING_REPORT.md`、`reports/RESULTS_REPORT.md`、`figures/` 目录列表。

然后从前序文档提取是否存在“需要补充的非数据图示”需求。输出一份候选清单，但不要把它当作默认任务清单：

```text
DRAWIO CANDIDATE LIST:
[ ] 总体技术路线图
[ ] 数据处理 pipeline
[ ] 复杂算法流程图
[ ] 模型/变量关系图
[ ] 指标体系图
```

这些只是候选，不是必须全部生成；文件名按实际图示决定，不固定要求 `fig_roadmap`、`fig_flow_q1`、`fig_flow_q2` 等文件必然存在。

若当前正文和现有图表已经足够表达方法与结构，则直接 skip，不制造无意义图。

### Step 2: 判定图类型

候选图示仅在确实有解释价值时使用：

| 图类型 | 适用场景 |
| --- | --- |
| 总体技术路线图 | 展示整体解题路线、章节逻辑、方法串联，且确实提升理解 |
| 数据处理 pipeline | 展示数据清洗、特征构造、建模输入，且相比正文更难理解 |
| 复杂算法流程图 | 展示单个子问题的输入、判断、算法、输出，且存在决策步骤 |
| 模型/变量关系图 | 展示模块关系、变量关系、模型层次，且正文较难概览 |
| 指标体系图 | 展示目标层、准则层、指标层，且需要结构化表达 |

在以下情况，不用 DrawIO 生成图：

- 结果对比型柱状图
- 预测误差曲线
- 灵敏度曲线
- 相关性热力图
- 分布图和箱线图
- 其他依赖实验或结果数据的图表

如果同一信息已经被 `3coding-visual` 的数据图清楚表达，4drawio 不再重复生成 DrawIO 版本。

### Step 3: 生成 DrawIO 源文件

每张图一个 `.drawio` 文件，放在 `figures/`。

DrawIO 内容要求：

- 文字语言与论文语言一致。
- 节点文字短，必要时双行，不堆长句。
- 同类节点样式统一。
- 箭头方向清晰，避免交叉。
- 图中不写大段解释，解释留给论文正文。
- 不使用装饰性阴影和过度渐变。

生成大 XML 时，分段写入，避免截断。示例：

```bash
mkdir -p figures
cat << 'XMLEOF' > figures/fig_roadmap.drawio
<mxfile>
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- nodes and edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
XMLEOF
```

### Step 4: 导出 PDF

优先用可用的 DrawIO 命令导出 PDF：

```bash
DRAWIO_BIN="$(command -v drawio 2>/dev/null || command -v draw.io 2>/dev/null || command -v draw.io.exe 2>/dev/null || true)"
if [ -n "$DRAWIO_BIN" ]; then
  "$DRAWIO_BIN" --export --format pdf --crop --output figures/fig_roadmap.pdf figures/fig_roadmap.drawio
else
  echo "DrawIO command not found; keep .drawio source and record export failure."
fi
```

如果无法导出 PDF，保留 `.drawio`，在 `reports/DRAWIO_REPORT.md` 记录失败原因和建议导出命令。

### Step 5: 自检和修复

每张图必须检查：

- `.drawio` 文件非空。
- 若导出成功，`.pdf` 文件非空。
- 节点没有明显重叠。
- 箭头不穿过核心节点。
- 字号、颜色、边框风格一致。
- 文件名和图意一致。
- 没有与 `3coding-visual` 的数据图重复。

发现问题要修 `.drawio` 并重新导出，不要只在报告里解释。

### Step 6: 写生成记录

保留 `reports/DRAWIO_REPORT.md`，但只记录最小信息：

```markdown
# 非数据图示报告
## 状态
generated / not needed
## 图示清单
| 文件 | 类型 | 用途 | 导出状态 |
| --- | --- | --- | --- |
## 备注
- ...
```

不记录长篇画图过程，不写成工作日志。最终的 caption、图号、正文引用、插入位置和排版由 `5writing` 决定。

## 质量要求

- 图示服务论文论证，不为装饰而画。
- 每张图必须能对应到 `reports/ANALYSIS_MODELING_REPORT.md` 中的真实方法。
- 数据型图表不得在本阶段重复生成。
- 若没有值得额外图示说明的结构、关系或流程，则直接 skip，并在报告中写明 `状态：not needed`。
- 4drawio 只负责生成 `.drawio` 与可用 `.pdf`，不负责 `caption`、图号、正文引用和最终插入位置。

## 与 `3coding-visual` 和 `5writing` 的边界

- 数据驱动图表由 `3coding-visual` 负责。
- 4drawio 在生成前应先检查已有 `figures/` 和前序报告，避免重复生成已有图。
- 4drawio 只负责：生成 `.drawio`、导出论文可用 `.pdf`、确认图示内容正确、可编辑、可用。
- 不负责：`caption`、图号、正文引用、最终插入位置、最终图片宽度、论文排版。这些交给 `5writing`。
- 4drawio 只需要从前序阶段读取：模型路线、数据处理流程、子问题依赖、算法结构、模块/变量关系、已存在图表清单；不要求读取全部结果数据，不重新计算结果。
