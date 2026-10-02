FROM node:20-alpine

WORKDIR /app

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装 pnpm（须与 package.json 的 packageManager 版本一致，否则 pnpm 会尝试
# 下载 @pnpm/exe 并按 pnpm-lock.yaml 校验其完整性，在 --frozen-lockfile 下失败）
RUN npm install -g pnpm@10.6.3

# 清理 npm 缓存并安装依赖
RUN pnpm install --frozen-lockfile

# 复制源代码
COPY . .

EXPOSE 5173

# 运行开发服务器
CMD ["pnpm", "run", "dev", "--host"]