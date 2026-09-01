# CUMCM 三人团队 SOP

## 核心原则

全队只执行一套 CUMCM workflow，由三个角色分工推进，而不是让三台电脑上的三个 Codex 各自执行一套完整 workflow。除非人类明确要求切换角色，每个 Codex 只在当前角色范围内工作，并通过正式 artifacts 交接；不得越权覆盖其他角色维护的正式产物。

## 角色表

| 角色 | 定位 | 主责阶段与产物 |
|---|---|---|
| A | 建模手、workflow 总控 | 主持 1start、2analysis；冻结模型路线；解释结果；必要时 4drawio |
| B | 编程手、计算事实负责人 | 主持 3coding；维护 `RESULTS_REPORT.md`、`results/`、`figures/` 及可复现计算 |
| C | 论文手、最终材料负责人 | 主持 5writing、后期 6verity；维护论文、附录、支撑材料和提交包 |

角色的详细权限与禁区分别见 `A_MODELING_ROLE.md`、`B_CODING_ROLE.md`、`C_WRITING_ROLE.md`。现有 Skill 仍是各阶段的执行规范，Role 文件只约束多人协作边界。

## 比赛推进

1. 比赛开始时，三人共同阅读题目和关键附件，统一题意与文件认知。
2. A 正式主持 1start 和 2analysis，形成模型路线、评价设计及交接 artifacts。
3. 核心路线必须经过人类团队的 major route checkpoint；确认后才作为 B 的正式输入。
4. 随后进入稳态流水线：A 研究下一问，B 计算当前问，C 撰写已经冻结且已有正式证据的问题。
5. 最终阶段由 A 审核模型表达，B 审核计算事实，C 主控论文、附录、支撑材料与提交包，最后执行 6verity。

## 三种正式交接

### A → B：模型交接

A 交付已确认的 analysis/modeling artifacts，明确问题定义、假设、变量、公式、候选与选定模型、评价/benchmark 设计、所需输入输出及未决风险。未通过 route checkpoint 的方案不得视为冻结模型。

### B → C：结果交接

B 以 `RESULTS_REPORT.md`、`results/`、`figures/` 和可复现代码为正式结果交接，明确实际模型、参数、关键数值、benchmark、诊断、稳健性、solver 状态、限制与可引用图表。口头结论或临时终端输出不是正式论文事实。

### C → A/B：论文审核

C 将模型定义与解释交 A 审核，将数值、表格、图表和计算结论交 B 审核。发现缺口时定向请求责任人补充，不由 C 自行创造内容或另跑一套模型。

## 单一事实源优先级

1. 当届官方规则、原始题面与附件；
2. A 已确认并冻结的 analysis/modeling artifacts；
3. B 的 `RESULTS_REPORT.md` 与真实 `results/`、`figures/`、可复现计算产物；
4. 已核验的外部资料与 references；
5. 论文及其他下游材料。

下游表述与上游正式事实冲突时，不自行选择“看起来正确”的版本，必须回到对应事实负责人核对并统一。

## Rollback

- B 发现数据不支持、核心模型不可实现、solver failure、benchmark 失败或结果异常且可能改变核心机制时，停止静默替换，向 A 报告并回退 2analysis。
- A 修改核心假设、模型定义、目标函数或评价机制时，必须更新正式 modeling artifact，标明受影响范围，并明确宣布相关旧结果和旧论文内容失效；B 重新计算后才能交给 C。
- C 发现模型解释缺口时回 A；发现数值、图表或计算证据缺口/冲突时回 B。修复完成后更新下游材料并重新验收。
- 未解决的 blocker 不得靠文字包装绕过，也不得进入最终 PASS。

## Git 协作

- `main` 是全队稳定事实源；A、B、C 使用各自工作分支。
- 影响其他角色正式输入的重大修改必须主动通知相关成员。
- 修改合并后，下游角色先同步再继续，避免基于过期 artifact 工作。
- 保持提交范围清晰即可，不引入复杂企业级 PR 流程。

## AI 使用记录

`reports/AI_USAGE_LOG.md` 是全队共享的 AI 使用事实记录。三个角色分别对自己承担阶段的阶段摘要和 material AI event 负责；不记录普通问答，不复制完整聊天。最终 `AI工具使用详情.pdf` 必须由这些真实记录整理，不能赛后凭空补写。

## 最终提交

6verity PASS 前，A 完成模型审核，B 完成结果审核，C 完成论文、附录、支撑材料、AI 详情和最终一致性检查。PASS 后只上传 `VERIFY_REPORT`“最终提交状态”中确认的两个文件：最终电子论文与最终电子支撑材料 ZIP/RAR。

最终 submission freeze 以及最终两个上传文件必须由三名人类队员共同确认。6verity PASS 仅表示满足提交条件，不构成 Codex 的自动冻结、提交或上传授权。
