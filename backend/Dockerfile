# 第一阶段：依赖安装
FROM python:3.12-slim AS deps

# 安装 uv（推荐直接用官方 distroless 镜像复制二进制文件，速度快且干净）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 复制所有项目文件
COPY . .

# 安装依赖到虚拟环境
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --cache-dir /root/.cache/uv -e .

# 第二阶段：运行时镜像
FROM python:3.12-slim AS runtime

# 复制虚拟环境
COPY --from=deps /opt/venv /opt/venv

# 确保使用虚拟环境
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# 复制应用代码
COPY . .

EXPOSE 8000

# 使用虚拟环境中的 uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ws-ping-interval", "60", "--ws-ping-timeout", "120"]