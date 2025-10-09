# 环境变量配置说明

## 快速开始

1. 复制环境变量模板文件：
```bash
cp backend/.env.example backend/.env.dev
```

2. 编辑 `backend/.env.dev` 文件，填入你的实际 API 密钥：
```bash
# 将所有的 your_gitee_ai_api_key_here 替换为你的实际 Gitee AI API 密钥
COORDINATOR_API_KEY=你的_gitee_ai_api_密钥
MODELER_API_KEY=你的_gitee_ai_api_密钥
CODER_API_KEY=你的_gitee_ai_api_密钥
WRITER_API_KEY=你的_gitee_ai_api_密钥

# 填入你的邮箱（用于 OpenAlex 学术搜索）
OPENALEX_EMAIL=你的邮箱@example.com
```

## 重要安全说明

⚠️ **绝对不要将包含真实 API 密钥的 .env 文件提交到 Git 仓库！**

- `.env.dev`、`.env.prod` 等环境文件已经被添加到 `.gitignore` 中
- 只提交 `.env.example` 模板文件
- 如果意外提交了密钥，请立即撤销密钥并生成新的密钥

## 获取 API 密钥

1. **Gitee AI**: 访问 [Gitee AI](https://ai.gitee.com/) 获取 API 密钥
2. **OpenAlex**: 访问 [OpenAlex](https://openalex.org/) 注册账号获取邮箱访问权限