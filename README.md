<h1 align="center">🤖 MathModelAgent 📐</h1>
<p align="center">
    <img src="./docs/icon.png" height="250px">
</p>
<h4 align="center">
    专为数学建模设计的 Agent<br>
    自动完成数学建模，生成一份完整的可以直接提交的论文。
</h4>

<h5 align="center">简体中文 | <a href="README_EN.md">English</a></h5>

## 🌟 愿景：

3 天的比赛时间变为 1 小时
自动完整一份可以获奖级别的建模论文

<p align="center">
    <img src="./docs/chat.png">
    <img src="./docs/coder.png">
</p>

## ✨ 功能特性

- 🔍 自动分析问题，数学建模，编写代码，纠正错误，撰写论文
- 💻 Code Interpreter
    - local Interpreter: 基于 jupyter , 代码保存为 notebook 方便再编辑
    - 云端 code interpreter: [E2B](https://e2b.dev/) 和 [daytona](https://app.daytona.io/)
- 📝 生成一份编排好格式的论文
- 🤝 multi-agents: 建模手，代码手，论文手等
- 🔄 multi-llms: 每个 agent 设置不同的、合适的模型
- 🤖 支持所有模型: [litellm](https://docs.litellm.ai/docs/providers)
- 💰 成本低：workflow agentless，不依赖 agent 框架
- 🧩 自定义模板：prompt inject 为每个 subtask 单独设置需求
- 🌐 Web Search: Agent 自主搜索互联网获取真实数据（Tavily API）
- 📚 RAG 知识库: 从本地知识库检索建模方法、代码模板、论文写作参考（ChromaDB + Rerank）
- 🤝 HIL 人机协作: 关键节点暂停等待用户审批，支持 6 种决策动作（confirm / edit / regenerate / ask / skip / abort）
- 🛡️ 四层容错: 有限重试 → Fallback Hand Off → Evaluator Shadow Mode → Feedback Rerun




---
---

我在平台中托管了一个在线版本，方便使用，欢迎体验：

https://mathmodel.top/home

## SKILLS

项目蒸馏成完全由 SKILLS 驱动
不再做 Harness 层

### Intro

MathModelAgent SKILL —— 直接在 Harness 中驱动的数学建模自动化方案.

**💰 开源免费，接入任意模型**
完全开源免费，可接入任何模型。

**🧠 端到端自动化**
从问题分析、建模、编码、绘图到论文排版和验收，一条 `/1start-mathmodel` 命令全自动完成，中间阶段自动串联，无需人工干预。

**📄 17 套 Typst 论文模板**
内置中英文主流赛事模板（国赛、华数杯、华为杯、MCM/ICM 等），自动匹配赛事类型，生成排版精良、可直接提交的 PDF 论文。

**📐 内置建模知识库**
包含完整的建模规范、模型选择决策树（AHP、TOPSIS、ARIMA、GA 等）、常见易错模式和 MCM/ICM 评分标准，每个阶段自动参考，降低模型幻觉。

**✅ 9 步自动验收**
文本泄漏检测 → 数值一致性校验 → Typst 编译 → PDF 可视化检查，确保论文零低级错误。

**🔧 可组合、可扩展**
每个阶段是独立 Skill，可单独调用（如只跑分析、只写论文）；模板和知识库可自由扩展；支持 Typst 生态排版。



### Install & Usage

安装 SKILL
```
npx skills add jihe520/MathModelAgent --all
```

运行
```
// claude
claude --dangerously-skip-permissions
claude: /1start-mathmodel 完成这个数学建模任务

// codex
codex --yolo
codex: $start-mathmodel 完成这个数学建模任务
```

其他命令
```
/doctor:  检查环境配置
/typst-author: typst 知识
```


### What Can You Contribute?

项目以后只会做 SKLLS 层的迭代和优化，不会再做其他部分。

如果你希望寻找 Agent 开发岗位，你可以研究该项目 Agent 设计并贡献，我会尽量合并.

你能做什么：

- 优化贡献比赛 typst Template , 你可以找一些 LaTeX 转成 typst
- 优化 SKILL Workflow
- 在不同的 Harness 上测试 不同的 LLM, 提供反馈和案例放在 example 仓库

Harness SKILL 的优化需要大量黑盒测试和调优.


### Thinking

- 两年前，我做了一个 Mulit-Agent 的数学建模项目并开源出来，收到了社区的欢迎和很多 star, 感谢大家支持。
- 感谢开源的 latex 模板，我在此基础上转化为 typst 模板
- 此 SKILL 是一个基础模板，你可以基于此构建更适合你自己的 MathModel SKILL
- For Agent DEVs : 两年前，我都是自己实现一套 Agent 框架，现在和以后更多的 Agent 产品直接基于 Harness 如 Codex / Claude Code / Pi  + SKILLS 来构建

---
---





## 🚀 后期计划

- [x] 添加并完成 webui、cli
- [x] 完善的教程、文档
- [ ] 提供 web 服务
- [ ] 英文支持（美赛）
- [ ] 集成 latex 模板
- [ ] 接入视觉模型
- [x] 添加正确文献引用
- [x] 更多测试案例
- [x] docker 部署
- [ ] human in loop ( HIL ): 关键节点暂停等待用户审批，支持 6 种决策动作（confirm/edit/regenerate/ask/skip/abort）
  <!-- TODO: 数据模型已实现，但工作流集成不完整 -->
- [ ] feedback: 评估器评分 + 反馈注入重跑，先 Writer 后 Coder
  <!-- TODO: 核心逻辑未实现，仅有 Agent 基类中的 TODO 注释 -->
- [x] codeinterpreter 接入云端 如 e2b 等供应商..
- [ ] 多语言: R 语言, matlab
- [ ] 绘图 napki,draw.io,plantuml,svg, mermaid.js
- [ ] 添加 benchmark
- [ ] web search tool: Tavily API 搜索互联网获取真实数据
  <!-- NOTE: 原计划 Tavily API 未实现，当前使用 OpenAlex 替代 -->
- [ ] RAG 知识库: ChromaDB + Rerank 检索建模方法、代码模板、论文写作参考
  <!-- TODO: 仅配置项存在，核心检索逻辑未实现 -->
- [ ] A2A hand off: Fallback 自动切换备用模型 + 有限重试 + Evaluator Shadow Mode
  <!-- TODO: 配置项和核心逻辑均未实现，仅有基础重试机制 -->
- [ ] chat / agent mode

## 视频demo

<video src="https://github.com/user-attachments/assets/954cb607-8e7e-45c6-8b15-f85e204a0c5d"></video>

> [!CAUTION]
> 项目处于实验探索迭代demo阶段，有许多需要改进优化改进地方，我(项目作者)很忙，有时间会优化更新
> 欢迎贡献


## 📖 使用教程


提供三种部署方式，请选择最适合你的方案：
1. [docker(最简单)](#-方案一docker-部署推荐最简单)
2. [本地部署](#-方案二-本地部署)
3. [脚本本地部署(社区)](#-方案三自动脚本部署来自社区)


下载项目

```bash
git clone https://github.com/jihe520/MathModelAgent.git # 克隆项目
```


> 如果你想运行 命令行版本 cli 切换到 [master](https://github.com/jihe520/MathModelAgent/tree/master) 分支,部署更简单，但未来不会更新



### 🐳 方案一：Docker 部署（推荐：安全简单）

> 确保电脑安装了 docker 环境

1. 启动服务

在项目文件夹下运行:

```bash
docker-compose up
```

2. 访问

现在你可以访问：
- 前端界面：http://localhost:5173
- 后端API：http://localhost:8000

3. 配置

侧边栏 -> 头像 -> API Key

### 💻 方案二: 本地部署（推荐项目开发者部署）

> 确保电脑中安装好 Python, Nodejs, **Redis** 环境



#### step1:安装依赖

1. 下载Redis(记得设置环境变量redis_path)

- windows 下载地址：<https://github.com/tporadowski/redis/releases>
- linux or mac 下载地址：<https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/>

2. 安装后端依赖

```bash
# ============ 安装依赖 ============
# 1. 切换到 backend 目录
cd backend
# 2. 安装 uv 包管理器（推荐）
pip install uv
# 3. 同步项目依赖
uv sync
```

```bash
# ============ MacOS / Linux 安装命令 ============
# 1. 设置环境变量
export ENV=DEV
export REDIS_URL=redis://localhost:6379/0
```

```powershell
# ============ Windows PowerShell 安装命令 ============
# 1. 设置环境变量
$env:ENV="DEV"
$env:REDIS_URL="redis://localhost:6379/0"
# 2. 设置 PowerShell 执行策略策略为 RemoteSigned
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# 3. 创建虚拟环境
python -m venv venv
```

3.安装前端依赖

```bash
cd frontend # 切换到 frontend 目录下
npm install -g pnpm
pnpm i
```

#### step2:启动项目

**windows用户直接双击运行项目中的win_start.bat 即可启动项目**

1.启动 Redis

```bash
redis-server
```

2.启动后端

```bash
# ============ MacOS / Linux 安装命令 ============
# 1. 激活虚拟环境
source .venv/bin/activate
# 2. 启动后端服务（激活后可直接使用 uvicorn 命令）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload
```

```bash
# ============ Windows PowerShell 安装命令 ============
# 1. 切换到 backend 目录
cd .\backend\
# 2. 激活虚拟环境
.\venv\Scripts\Activate.ps1
# 3. 启动后端服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload
```


3.启动前端

```bash
cd .\frontend\
pnpm run dev
```

修改 backend/.env.dev 的环境变量 **REDIS_URL**

配置API Key

1. 使用 WebUI
    侧边栏 -> 头像 -> API Key
2. 修改 backend/.env.dev 文件
    先将.env.example文件 改为.env.dev
    然后在.env.dev中 修改各 Agent API 配置



### 🚀 方案三：自动脚本部署（来自社区）
有没有自动部署的脚本 ？
[mmaAutoSetupRun](https://github.com/Fitia-UCAS/mmaAutoSetupRun)



[教程](./docs/md/tutorial.md)

运行的结果和产生在`backend/project/work_dir/xxx/*`目录下
- notebook.ipynb: 保存运行过程中产生的代码
- res.md: 保存最后运行产生的结果为 markdown 格式

需要自定义自定义提示词模板 template ？
Prompt Inject : [prompt](./backend/app/config/md_template.toml)

网络状况太差难以配置Docker等设置？
网络不畅时的配置过程示例：[网络环境极差时的MathModelAgent配置过程](docs/md/网络环境极差时的MathModelAgent配置过程.md)


## ⚙️ 新功能配置

MathModelAgent 支持以下可选功能，默认已关闭，开启后未配置外部依赖时自动降级跳过。详见 [升级说明](./升级说明.md)。

| 功能 | 配置开关 | 说明 |
|------|----------|------|
| Web Search | `SEARCH_ENABLED` + `TAVILY_API_KEY` | Agent 自主联网搜索真实数据（Tavily API） |
| RAG 知识库 | `RAG_ENABLED` | 从本地知识库检索建模方法和代码模板（ChromaDB + Rerank） |
| HIL 人机协作 | `HIL_ENABLED` | 关键节点暂停等待用户审批，支持 6 种决策动作 |
| Fallback Hand Off | `FALLBACK_*` 系列 | 主模型故障自动切换备用模型 |
| Evaluator + Feedback | `EVALUATOR_*` 系列 | 输出质量评估 + 反馈重跑 |

快速启用 Web Search：注册 [Tavily](https://tavily.com) 获取 API Key，在 `backend/.env.dev` 中设置 `TAVILY_API_KEY=tvly-xxx`。

## 🤝 贡献和开发

[DeepWiki](https://deepwiki.com/jihe520/MathModelAgent) | [Zread](https://zread.ai/jihe520/MathModelAgent)


> [!TIP]
> 如果你有跑出来好的案例可以提交 PR 在该仓库下:
> [MathModelAgent-Example](https://github.com/jihe520/MathModelAgent-Example)

- 项目处于**开发实验阶段**（我有时间就会更新），变更较多，还存在许多 Bug，我正着手修复。
- 希望大家一起参与，让这个项目变得更好
- 非常欢迎使用和提交  **PRs** 和 issues 
- 需求参考 后期计划

clone 项目后，下载 **Todo Tree** 插件，可以查看代码中所有具体位置的 todo

`.cursor/*` 有项目整体架构、rules、mcp 可以方便开发使用

## 📄 版权License

个人免费使用，请勿商业用途，商业用途联系我（作者）

[License](./docs/md/License.md)

## 🙏 Reference

Thanks to the following projects:
- [OpenCodeInterpreter](https://github.com/OpenCodeInterpreter/OpenCodeInterpreter/tree/main)
- [TaskWeaver](https://github.com/microsoft/TaskWeaver)
- [Code-Interpreter](https://github.com/MrGreyfun/Local-Code-Interpreter/tree/main)
- [Latex](https://github.com/Veni222987/MathModelingLatexTemplate/tree/main)
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)
- [ai-manus](https://github.com/Simpleyyt/ai-manus)

## 其他

### 💖 Sponsor

[☕️ 给作者买一杯咖啡](./docs/md/sponser.md)

https://linux.do/

#### 企业

<div align="center">
    <a href="https://share.302.ai/UoTruU" target="_blank">
    <img src="./docs/302ai.jpg">
    </a>
</div>

[302.AI](https://share.302.ai/UoTruU) 是一个按用量付费的企业级AI资源平台，提供市场上最新、最全面的AI模型和API，以及多种开箱即用的在线AI应用

#### 用户

[danmo-tyc](https://github.com/danmo-tyc)

### 👥 GROUP

有问题可以进群问

点击链接加入腾讯频道【MathModelAgent】：https://pd.qq.com/s/7rfbai3au

点击链接加入群聊 779159301【MathModelAgent】：https://qm.qq.com/q/Fw2cCJPoki

[Discord](https://discord.gg/3Jmpqg5J)

> [!CAUTION]
> 免责声明: 注意，AI 生成仅供参考，目前水平直接参加国赛获奖是不可能的，但我相信 AI 和 该项目未来的成长。

