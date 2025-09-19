from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import router
from contextlib import asynccontextmanager
import os
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Sandbox")

    PROJECT_FOLDER = "./project"
    os.makedirs(PROJECT_FOLDER, exist_ok=True)

    yield
    print("Stopping Sandbox")


app = FastAPI(
    title="Sandbox",
    description="Sandbox Service",
    version="0.1.0",
    lifespan=lifespan,
)

# 跨域 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(router.api_router)


app.mount(
    "/static",  # 这是访问时的前缀
    StaticFiles(directory="project/work_dir"),  # 这是本地文件夹路径
    name="static",
)
