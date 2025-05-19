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

3 天的比赛时间变为 1 小时 <br> 
自动完整一份可以获奖级别的建模论文

<p align="center">
    <img src="./docs/index.png">
    <img src="./docs/chat.png">
    <img src="./docs/coder.png">
    <img src="./docs/writer.png">
</p>

## ✨ 功能特性

- 🔍 自动分析问题，数学建模，编写代码，纠正错误，撰写论文
- 💻 本地代码解释器
- 📝 生成一份编排好格式的论文
- 🤝 muti-agents: ~~建模手~~，代码手(反思模块，本地代码解释器)，论文手
- 🔄 muti-llms: 每个agent设置不同的模型
- 💰 成本低 agentless(单次任务成本约 1 rmb)

## 🚀 后期计划

- [x] 添加并完成 webui、cli
- [ ] 完善的教程、文档
- [ ] 提供 web 服务
- [ ] 英文支持（美赛）
- [ ] 集成 latex 模板
- [ ] 接入视觉模型
- [ ] 添加正确文献引用
- [x] 更多测试案例
- [ ] docker 部署
- [ ] 引入用户的交互（选择模型，重写等等）
- [x] codeinterpreter 接入云端 如 e2b 等供应商..
- [ ] 多语言: R 语言, matlab
- [ ] 绘图 napki,draw.io
- [ ] 添加 benchmark

## 视频demo

<video src="https://github.com/user-attachments/assets/954cb607-8e7e-45c6-8b15-f85e204a0c5d"></video>

> [!CAUTION]
> 项目处于实验探索迭代demo阶段，有许多需要改进优化改进地方，我(项目作者)很忙，有时间会优化更新
> 欢迎贡献

## 📖 使用教程

0. 详细教程
- [ ] Windows   waiting
- [x] Linux/WSL [below](#wsl部署教程linux)
- [ ] MacOS     waiting

> 确保电脑中安装好 Python, Nodejs, **Redis** 环境

> 如果你想运行 命令行版本 cli 切换到 [master](https://github.com/jihe520/MathModelAgent/tree/master) 分支,部署更简单，但未来不会更新



1. 配置模型

复制`/backend/.env.dev.example`到`/backend/.env.dev`(删除`.example` 后缀)
填写配置模型和 APIKEY
推荐模型能力较强的、参数量大的模型。

```bash
# support all model, check out https://docs.litellm.ai/docs/ 
API_KEY=
# gpt-4.1,deepseek/deepseek-chat
#注意这里deepseek/deepseek-chat才是一整个模型，如果只输入一般api无法成功调用
MODEL=
# 确保安装 Redis
```

复制`/fronted/.env.example`到`/fronted/.env`(删除`.example` 后缀)



2. 安装依赖

下载项目

```bash
git clone https://github.com/jihe520/MathModelAgent.git # 克隆项目
```

启动后端

```bash
cd backend # 切换到 backend 目录下
pip install uv # 推荐使用 uv 管理 python 项目
uv sync # 安装依赖
# 启动后端
# 激活 python 蓄虚拟环境
source .venv/bin/activate # MacOS or Linux
venv\Scripts\activate.bat # Windows
# MacOS or Linux 运行这条命令
ENV=DEV uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload
# Windows 运行这条命令
set ENV=DEV ; uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120
```

启动前端

```bash
cd frontend # 切换到 frontend 目录下
npm install -g pnpm
pnpm i #确保电脑安装了 pnpm 
pnpm run dev
```


运行的结果和产生在`backend/project/work_dir/xxx/*`目录下
- notebook.ipynb: 保存运行过程中产生的代码
- res.md: 保存最后运行产生的结果为 markdown 格式，使用 markdown 转 word(研究下 pandoc)

## 🤝 贡献和开发

[DeepWiki](https://deepwiki.com/jihe520/MathModelAgent)

- 项目处于**开发实验阶段**（我有时间就会更新），变更较多，还存在许多 Bug，我正着手修复。
- 希望大家一起参与，让这个项目变得更好
- 非常欢迎使用和提交  **PRs** 和 issues 
- 需求参考 后期计划

clone 项目后，下载 **Todo Tree** 插件，可以查看代码中所有具体位置的 todo

`.cursor/*` 有项目整体架构、rules、mcp 可以方便开发使用

## 📄 版权License

个人免费使用，请勿商业用途，商业用途联系我（作者）

## 🙏 Reference

Thanks to the following projects:
- [OpenCodeInterpreter](https://github.com/OpenCodeInterpreter/OpenCodeInterpreter/tree/main)
- [TaskWeaver](https://github.com/microsoft/TaskWeaver)
- [Code-Interpreter](https://github.com/MrGreyfun/Local-Code-Interpreter/tree/main)
- [Latex](https://github.com/Veni222987/MathModelingLatexTemplate/tree/main)
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)

## 其他

感谢赞助
[danmo-tyc](https://github.com/danmo-tyc)

有问题可以进群问
[QQ 群：699970403](http://qm.qq.com/cgi-bin/qm/qr?_wv=1027&k=rFKquDTSxKcWpEhRgpJD-dPhTtqLwJ9r&authKey=xYKvCFG5My4uYZTbIIoV5MIPQedW7hYzf0%2Fbs4EUZ100UegQWcQ8xEEgTczHsyU6&noverify=0&group_code=699970403)

<img src="./docs/qq.jpg" height="400px">


## WSL部署教程/Linux

使用WSL安装旨在规避win系统环境配置的问题

默认WSL已安装完成，不会的可以参考网络教程，提供两处仅供参考
- [图文教程](https://blog.csdn.net/x777777x/article/details/141092913)
- [视频教程](https://www.bilibili.com/video/BV1tW42197za/?spm_id_from=333.337.search-card.all.click&vd_source=3a1d2230b9c1cfca59cf301925902d13)

后续以Ubuntu为例
### 项目文件的两种处理
- Ubuntu下
```bash
git clone https://github.com/jihe520/MathModelAgent.git # 克隆项目
```
网速过慢也可以使用ssh下载，请自行网络查阅相关教程
- Windows向Ubuntu转移
在github上下载源代码（.zip）解压到Windows下 例如：D:\

进入Ubuntu面板
```bash
mv /mnt/d/MathModelAgent ~/
```

### 环境配置
- 下载环境
一般python在Linux下自带，可以忽略
```bash
#更新包管理器
sudo apt update
#安装或更新python pip
sudo apt install -y python3 python3-pip
#安装node npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
#安装 redis
sudo apt install redis
```
- 检查
```bash
python3 --version
pip3 --version
node -v
npm -v
sudo systemctl status redis-server
redis-cli ping
```
输出版本号则说明正常，对应输出检查可以询问AI

### 安装依赖项和启动

后端
```bash
cd backend # 切换到 backend 目录下

#Linux在最近版本不建议安装包管理，因此需要先创建虚拟环境
python3 -m venv .venv
#启用虚拟环境
source .venv/bin/activate

pip install uv # 推荐使用 uv 管理 python 项目
uv sync # 安装依赖

#上面不行的看这里,但是国内网络环境推荐使用清华镜像，否则科学上网是必要的
pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple
uv sync -i https://pypi.tuna.tsinghua.edu.cn/simple

# 启动后端
ENV=DEV uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload
```
下载成功后的结果一般为
```bash
$ pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple #你输入的命令行
#返回结果
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Requirement already satisfied: uv in ./.venv/lib/python3.12/site-packages (0.7.5)

$ uv sync -i https://pypi.tuna.tsinghua.edu.cn/simple
#初次下载会有一大串，还有进度条
Resolved 154 packages in 8ms
Audited 148 packages in 0.04ms
```
启动结果
```bash
$  ENV=DEV uvicorn app.main:app --host 0.0.0.0 --port 8000 --ws-ping-interval 60 --ws-ping-timeout 120 --reload #你输入的命令行
#返回结果
INFO:     Will watch for changes in these directories: ['/home/shuihong/MathModelAgent/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13652] using WatchFiles
INFO:     Started server process [13654]
INFO:     Waiting for application startup.
2025-05-19 11:07:56.028 | INFO     | app.main:lifespan:13 - Starting MathModelAgent
INFO:     Application startup complete.
2025-05-19 11:07:56.029 | INFO     | app.main:lifespan:18 - CORS_ALLOW_ORIGINS:
```
前端
```bash
cd frontend # 切换到 frontend 目录下
npm install -g pnpm
pnpm i #确保电脑安装了 pnpm 
pnpm run dev
```
启动结果
```bash
$ pnpm run dev  #你输入的命令行
#返回结果
> frontend@0.0.0 dev /home/shuihong/MathModelAgent/frontend
> vite
  VITE v6.1.1  ready in 735 ms
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### 关闭
Ctrl+C 退出
