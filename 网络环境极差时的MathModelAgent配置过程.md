# 网络环境极差时的MathModelAgent配置过程

此文档用于记录2025/7/12时，在网络极差时的配置过程。

试图在VMware Workstation17中的CentOS 7上部署。因为网络问题而失败。

校园网能上GitHub上不了dockerhub，在外面挂VPN（不开启TUN）能上dockerhub上不了GitHub。

改用Windows 11 家庭中文版 24H2 从零开始安装并使用Docker部署。

## 1.下载并配置Docker Desktop

此步不需要使用VPN。官网上不去可以自行搜索安装包。

运行下载的安装程序，按照安装向导的提示完成安装。安装结束后程序会要求重启计算机。

安装完成后，启动 Docker Desktop。启动时需要登录 Docker 账号，连不上Docker官网所以选择免登录的方式。

等待 Docker Desktop 启动完成，确保系统托盘中的 Docker 图标显示为运行状态。

<img width="437" height="722" alt="image-20250712005640730" src="https://github.com/user-attachments/assets/257e620e-53b1-4761-aaaf-c6bdddc1169b" />


此时会弹出命令行要求安装WSL。等待即可。

<img width="1920" height="1080" alt="a33121ae9047c01153edebe7ed666a06" src="https://github.com/user-attachments/assets/e83841b3-abd3-4aa6-b811-09ecdd08b905" />


本机使用VPN的时候Github一直都能ping通的，但是WSL的安装进度会卡在30%左右，

![c4c65346b2914b38da56a7ee5065702f](https://github.com/user-attachments/assets/6d91a444-587c-4920-a2ef-ce2ba0bd0e25)


安装完毕。

根据自己的网络状态自行配置。

<img width="1590" height="900" alt="image-20250712005715579" src="https://github.com/user-attachments/assets/d60d7ed3-50ee-4ea1-82bb-84c45c9b9231" />



## 2.下载 MathModelAgent 项目

打开命令提示符或 PowerShell，执行以下命令克隆项目：

```bash
git clone https://github.com/jihe520/MathModelAgent.git
cd MathModelAgent
```

连不上Github就找同学帮忙或者干脆tb代下。笔者直接下载的整个代码压缩包。



## 3.配置环境变量

1. **后端配置**
   - 在`backend/`目录下，复制`.env.dev.example`为`.env.dev`
   - 编辑 `.env.dev`，填入模型 API 密钥等配置（如 OpenAI API 密钥）。
2. **前端配置**
   - 在`frontend/`目录下，复制`.env.example`为`.env.development`



## 4.使用 Docker 构建并启动服务

1. **打开终端**
   进入项目根目录（包含 `docker-compose.yml` 的目录）。

2. **构建 Docker 镜像**
   执行以下命令构建后端和前端镜像：

   ```bash
   docker-compose build
   ```

   - 若提示 `docker-compose` 命令不存在，可尝试使用 `docker compose`（注意中间有空格）。

   实际上网不好就会有这种情况：
   ```bash
   D:\mmaS\MathModelAgent>docker-compose build
   [+] Building 21.6s (6/6) FINISHED
    => [internal] load local bake definitions                                                                         0.0s
    => => reading from stdin 678B                                                                                     0.0s
    => [backend internal] load build definition from Dockerfile                                                       0.1s
    => => transferring dockerfile: 799B                                                                               0.0s
    => [frontend internal] load build definition from Dockerfile                                                      0.1s
    => => transferring dockerfile: 363B                                                                               0.0s
    => ERROR [frontend internal] load metadata for docker.io/library/node:20                                         21.1s
    => [backend internal] load metadata for ghcr.io/astral-sh/uv:latest                                               4.3s
    => ERROR [backend internal] load metadata for docker.io/library/python:3.12-slim                                 21.1s
   ------
    > [frontend internal] load metadata for docker.io/library/node:20:
   ------
   ------
    > [backend internal] load metadata for docker.io/library/python:3.12-slim:
   ------
   Dockerfile:2
   
   --------------------
   
      1 |     # 构建阶段
   
      2 | >>> FROM node:20 AS build
   
      3 |
   
      4 |     WORKDIR /app
   
   --------------------
   
   target frontend: failed to solve: node:20: failed to resolve source metadata for docker.io/library/node:20: failed to do request: Head "https://registry-1.docker.io/v2/library/node/manifests/20": dialing registry-1.docker.io:443 container via direct connection because disabled has no HTTPS proxy: connecting to registry-1.docker.io:443: dial tcp 108.160.169.46:443: connectex: A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond.
   ```

Docker 在拉取镜像时无法连接到 Docker Hub 镜像仓库。

笔者在修改Docker设置中的镜像源后仍然不行。

可以尝试手动拉取。

```bash
docker pull node:20
docker pull python:3.12-slim
docker pull ghcr.io/astral-sh/uv:latest
```

网不好的时候手动拉取都不行。

在自己的Windows上随意修改Dockerfile可能会有奇奇怪怪的错误。

所以其实不妨

```bash
C:\Users\Nova>docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/node:20
20: Pulling from ddn-k8s/docker.io/library/node
ca4e5d672725: Pull complete
30b93c12a9c9: Pull complete
10d643a5fa82: Pull complete
d6dc1019d793: Pull complete
ea8e6f2ca326: Pull complete
19951d6e9461: Pull complete
247e8d31d16f: Pull complete
282ebe8f0e48: Pull complete
Digest: sha256:7f0e372e66623dd26aa7e7156dab18e3bb02f10f08c69aca1ecba7c538f4d6d4
Status: Downloaded newer image for swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/node:20
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/node:20

C:\Users\Nova>docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim
3.12-slim: Pulling from ddn-k8s/docker.io/python
f11c1adaa26e: Pull complete
a64cae28bf14: Pull complete
0e903b6a67b0: Pull complete
808ac08b1607: Pull complete
c4e9078483aa: Pull complete
Digest: sha256:8d86cd5ae705baa369b0a74881b4811f28a60d2a2900d2a6221b65be7d481101
Status: Downloaded newer image for swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim

C:\Users\Nova>docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/astral-sh/uv:latest
latest: Pulling from ddn-k8s/ghcr.io/astral-sh/uv
d34f8c7c82d2: Pull complete
ac8f40aa894b: Pull complete
Digest: sha256:d6a9c6668bb8fc51bcb0b452a1d9e98252c36cd1e4705a056f92a97bcbabfb73
Status: Downloaded newer image for swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/astral-sh/uv:latest
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/astral-sh/uv:latest
```

使用一般都可靠的华为云。

此时拉取的镜像来自华为云仓库（`swr.cn-north-4.myhuaweicloud.com/ddn-k8s/...`），但项目的`Dockerfile`中引用的是默认镜像名（如`node:20`、`python:3.12-slim`）。需要给这些镜像添加与`Dockerfile`一致的标签，让 Docker 构建时直接使用本地镜像。

**在执行拉取的目录下**：

```powershell
# 为node镜像添加标签（匹配Dockerfile中的node:20）
docker tag swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/node:20 node:20

# 为python镜像添加标签（匹配Dockerfile中的python:3.12-slim）
docker tag swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.12-slim python:3.12-slim

# 为uv镜像添加标签（匹配Dockerfile中的ghcr.io/astral-sh/uv:latest）
docker tag swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/astral-sh/uv:latest ghcr.io/astral-sh/uv:latest
```

然后检查：

```powershell
C:\Users\Nova>docker images | findstr "node python uv"
ghcr.io/astral-sh/uv                                              latest      25a2dfe6d423   2 months ago    40.9MB
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/ghcr.io/astral-sh/uv     latest      25a2dfe6d423   2 months ago    40.9MB
node                                                              20          1a8e51cfa7a5   11 months ago   1.1GB
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/library/node   20          1a8e51cfa7a5   11 months ago   1.1GB
python                                                            3.12-slim   36d84f5948d0   12 months ago   129MB
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python         3.12-slim   36d84f5948d0   12 months ago   129MB
```

华为云原镜像也会显示，不影响。

把终端关了，切换到项目根目录（包含`docker-compose.yml`的文件夹）再打开终端。

执行构建命令（强制使用本地镜像，不联网拉取）：

```powershell
docker-compose build --no-cache
```

- `--no-cache`参数确保不使用缓存，直接基于本地镜像构建，避免网络请求。

这个过程要5-15分钟，笔者用了11分钟左右。

```powershell
D:\mmaS\MathModelAgent>docker-compose build --no-cache
[+] Building 686.8s (28/28) FINISHED
 => [internal] load local bake definitions                                                                         0.0s
 => => reading from stdin 726B                                                                                     0.0s
 => [frontend internal] load build definition from Dockerfile                                                      0.0s
 => => transferring dockerfile: 363B                                                                               0.0s
 => [backend internal] load build definition from Dockerfile                                                       0.0s
 => => transferring dockerfile: 799B                                                                               0.0s
 => [frontend internal] load metadata for docker.io/library/node:20                                                0.0s
 => [frontend internal] load .dockerignore                                                                         0.1s
 => => transferring context: 633B                                                                                  0.0s
 => [backend internal] load metadata for ghcr.io/astral-sh/uv:latest                                               0.0s
 => [backend internal] load metadata for docker.io/library/python:3.12-slim                                        0.0s
 => [backend internal] load .dockerignore                                                                          0.1s
 => => transferring context: 248B                                                                                  0.0s
 => [frontend 1/6] FROM docker.io/library/node:20                                                                  0.6s
 => [frontend internal] load build context                                                                         0.5s
 => => transferring context: 9.92MB                                                                                0.4s
 => [backend] FROM ghcr.io/astral-sh/uv:latest                                                                     0.2s
 => [backend builder 1/7] FROM docker.io/library/python:3.12-slim                                                  0.5s
 => [backend internal] load build context                                                                          2.1s
 => => transferring context: 89.14MB                                                                               2.0s
 => [backend builder 2/7] COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/                                   0.3s
 => [frontend 2/6] WORKDIR /app                                                                                    0.1s
 => [frontend 3/6] COPY package.json pnpm-lock.yaml ./                                                             0.2s
 => [backend builder 3/7] WORKDIR /app                                                                             0.2s
 => [frontend 4/6] RUN npm install -g pnpm                                                                         7.5s
 => [backend builder 4/7] COPY pyproject.toml uv.lock ./                                                           0.4s
 => [backend builder 5/7] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --locked --no-install-proje  157.1s
 => [frontend 5/6] RUN pnpm install                                                                              670.7s
 => [backend builder 6/7] COPY . .                                                                                 0.2s
 => [backend builder 7/7] RUN --mount=type=cache,target=/root/.cache/uv     uv sync --locked                       0.3s
 => [backend] exporting to image                                                                                   4.4s
 => => exporting layers                                                                                            4.3s
 => => writing image sha256:d32f0070b82bad9a6a5b65eae10fe1aea6db669ef5f9d6a0bcf08964f337786e                       0.0s
 => => naming to docker.io/library/mathmodelagent-backend                                                          0.0s
 => [backend] resolving provenance for metadata file                                                               0.0s
 => [frontend 6/6] COPY . .                                                                                        0.1s
 => [frontend] exporting to image                                                                                  7.0s
 => => exporting layers                                                                                            6.9s
 => => writing image sha256:31813222c752a29ce4b26e2268abefa43ed5e224edb03a843955d0ca71085afe                       0.0s
 => => naming to docker.io/library/mathmodelagent-frontend                                                         0.0s
 => [frontend] resolving provenance for metadata file                                                              0.0s
[+] Building 2/2
 ✔ backend   Built                                                                                                 0.0s
 ✔ frontend  Built                                                                                                 0.0s
```

这样就算构建好了。

3. **构建完成后，启动容器**

```bash
docker-compose up -d
```

- `-d` 表示后台运行。

网络不好时就会有：

```powershell
D:\mmaS\MathModelAgent>docker-compose up -d
[+] Running 1/1
 ✘ redis Error Get "https://registry-1.docker.io/v2/": context deadline exceeded                                  16.0s
Error response from daemon: Get "https://registry-1.docker.io/v2/": context deadline exceeded
```

即Docker 无法连接到 Docker 官方镜像仓库（`registry-1.docker.io`），导致拉取`redis`镜像时超时。

还是只能使用镜像。

```bash
D:\mmaS\MathModelAgent>docker pull swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis:latest
latest: Pulling from ddn-k8s/docker.io/redis
d2eb42b4a5eb: Pull complete
5de2dd3ff2ef: Pull complete
6c334acf232e: Pull complete
3090e1a50a6c: Pull complete
f5bc47c37726: Pull complete
20eea55b3ebb: Pull complete
4f4fb700ef54: Pull complete
d128ccd842a6: Pull complete
Digest: sha256:00d8139cc831c0cdbac83efe93b3089b1c714bda4ea6c4f533cd60b69a6ef8bc
Status: Downloaded newer image for swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis:latest
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis:latest

D:\mmaS\MathModelAgent>docker tag swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis:latest redis:latest

D:\mmaS\MathModelAgent>docker images | grep redis
'grep' 不是内部或外部命令，也不是可运行的程序
或批处理文件。
```

此时可能仍会有：

```powershell
D:\mmaS\MathModelAgent>docker-compose up -d
[+] Running 1/1
 ✘ redis Error Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting fo...             15.9s
Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
```

即已经手动拉取并标签化了 Redis 镜像，但`docker-compose`仍在尝试从 Docker Hub 拉取 Redis（可能是配置缓存或镜像引用优先级问题）。解决办法是直接在`docker-compose.yml`中指定使用华为云的 Redis 镜像，跳过标签依赖。

换一种方式验证镜像的存在：

```powershell
D:\mmaS\MathModelAgent>docker images | findstr "redis"
redis                                                             latest      fa310398637f   6 months ago     117MB
swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis          latest      fa310398637f   6 months ago     117MB
```

能看到`redis:latest`，说明镜像已正确标签化。

直接在配置文件中指定 Redis 镜像的完整地址，避免 Docker 尝试从默认仓库拉取：

1. 在项目根目录找到`docker-compose.yml`文件，用记事本或编辑器打开。

2. 找到`redis`服务的配置，在本项目中：

   ```yaml
   # docker-compose.yml
   
   services:
     redis:
       image: redis:alpine
       container_name: mathmodelagent_redis
       ports:
         - "6379:6379" # 将 Redis 容器的 6379 端口映射到主机的 6379 端口
       volumes:
         - redis_data:/data # Redis 数据的持久化存储卷
   
     backend:
       build:
         context: ./backend # Dockerfile 的上下文路径
         dockerfile: Dockerfile # Dockerfile 文件名
       container_name: mathmodelagent_backend
       ports:
         - "8000:8000" # 将后端容器的 8000 端口映射到主机的 8000 端口
       env_file:
         - ./backend/.env.dev #从此文件加载环境变量
       environment:
         - ENV=DEV # 为后端显式设置 ENV
         # .env.dev 文件中的 REDIS_URL 应为 redis://redis:6379/0
       volumes:
         - ./backend:/app # 挂载后端代码以实现热重载 (开发环境)
         - ./backend/project/work_dir:/app/project/work_dir # 持久化生成的文件
         - backend_venv:/app/.venv # 可选：持久化 venv 以在依赖不变时加快后续构建速度
       depends_on:
         - redis # 确保 Redis 在后端启动前启动
       stdin_open: true # 保持标准输入打开
       tty: true      # 分配一个伪终端
   
     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       container_name: mathmodelagent_frontend
       ports:
         - "5173:5173" # 将前端容器的 5173 端口 (Vite 默认) 映射到主机的 5173 端口
       env_file:
         - ./frontend/.env.development # 加载前端的环境变量
       volumes:
         - ./frontend:/app # 挂载前端代码以实现热重载 (开发环境)
         - /app/node_modules # 匿名卷，防止主机的 node_modules 覆盖容器内的
       depends_on:
         - backend # 确保后端可用 (尽管前端通常只需要其 URL)
       stdin_open: true
       tty: true
   
   volumes:
     redis_data: # 定义用于 Redis 持久化的命名卷
     backend_venv: # 定义用于后端 venv 的命名卷
   ```

3. 修改`image`字段为华为云镜像地址：

   这一段

   ```yaml
   services:
     redis:
       image: redis:alpine  # 这里就是需要修改的 image 字段
       container_name: mathmodelagent_redis
       ports:
         - "6379:6379"
       volumes:
         - redis_data:/data
   ```

修改为：

```yaml
services:
  redis:
    image: swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis:alpine  # 修改后的镜像地址
    container_name: mathmodelagent_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
```

然后保存。

注意**YAML 要求 `key: value` 中冒号后必须有空格**，不然就会像我这样：

```powershell
D:\mmaS\MathModelAgent>docker-compose down
yaml: line 6: mapping values are not allowed in this context
```

yaml文件格式错误导致关不掉。

改好了就再重启服务：

```powershell
D:\mmaS\MathModelAgent>docker-compose down

D:\mmaS\MathModelAgent>docker-compose up -d
[+] Running 9/9
 ✔ redis Pulled                                                                                                    5.3s
   ✔ da9db072f522 Pull complete                                                                                    1.3s
   ✔ dd8d46bd4047 Pull complete                                                                                    1.4s
   ✔ 5057e26f1a86 Pull complete                                                                                    1.6s
   ✔ be83d0fd33a3 Pull complete                                                                                    2.6s
   ✔ b3d150cb1b6c Pull complete                                                                                    4.0s
   ✔ 369ad5b9119b Pull complete                                                                                    4.0s
   ✔ 4f4fb700ef54 Pull complete                                                                                    4.1s
   ✔ 37d63ae71d35 Pull complete                                                                                    4.1s
[+] Running 6/6
 ✔ Network mathmodelagent_default        Created                                                                   0.1s
 ✔ Volume "mathmodelagent_backend_venv"  Created                                                                   0.0s
 ✔ Volume "mathmodelagent_redis_data"    Created                                                                   0.0s
 ✔ Container mathmodelagent_redis        Started                                                                  28.2s
 ✔ Container mathmodelagent_backend      Started                                                                  28.4s
 ✔ Container mathmodelagent_frontend     Started                                                                  11.9s

D:\mmaS\MathModelAgent>docker ps | findstr "redis"
0947be7781cc   swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/redis:alpine   "docker-entrypoint.s鈥?   43 seconds ago   Up 15 seconds   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   mathmodelagent_redis
FINDSTR: 写入错误
```

所有容器（`redis`、`backend`、`frontend`）都已成功启动，那个`FINDSTR: 写入错误`是 Windows 命令行的临时小问题，不影响服务运行，不用在意。



## 5.启动项目

### 1. 访问项目前端界面

打开浏览器，输入以下地址：`http://localhost:5173`

如果一切正常，会看到`MathModelAgent`的前端界面，此时可以尝试使用项目功能（比如输入数学建模问题，让系统自动处理）。

<img width="1920" height="1020" alt="image-20250712013002471" src="https://github.com/user-attachments/assets/b69265d7-d207-4938-b0b5-fddbe0992774" />

### 2. 验证后端服务是否正常

访问后端 API 地址，确认服务运行：`http://localhost:8000`

如果后端正常启动，会看到类似 API 文档或状态提示的页面（具体取决于项目设计）。

<img width="1920" height="1020" alt="image-20250712013024423" src="https://github.com/user-attachments/assets/977a5989-b8cb-4c9a-b227-9d4942fc602d" />


### 3. 检查服务日志（若有问题）

如果访问时出现空白页、报错等情况，可以查看容器日志排查问题：

```powershell
# 查看前端日志（比如前端无法加载、报错）
docker logs mathmodelagent_frontend
```

<img width="1482" height="762" alt="image-20250712013102332" src="https://github.com/user-attachments/assets/381ff9db-2582-438d-872f-3d769e91002d" />

```powershell
# 查看Redis日志（比如启动失败）
docker logs mathmodelagent_redis
```

<img width="1482" height="762" alt="image-20250712013128563" src="https://github.com/user-attachments/assets/028b41fc-f9d8-454a-b18e-e604641bc099" />

日志中会显示具体错误信息（如依赖缺失、配置错误等），根据提示调整即可。

### 4. 停止服务（如需）

如果后续需要停止项目，执行：

```powershell
docker-compose down
```

