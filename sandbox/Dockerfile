# 使用官方推荐的 Python 基础镜像
FROM python:3.12-slim AS builder

# 安装 uv（推荐直接用官方 distroless 镜像复制二进制文件，速度快且干净）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 先复制依赖文件，利用 Docker 层缓存
COPY pyproject.toml uv.lock ./

# 安装依赖（不安装项目本身，加快后续构建）
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# 再复制项目代码
COPY . .

# 安装项目本身
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

EXPOSE 8001

# 直接使用 uvicorn，因为依赖已安装到系统 Python
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]