"""文件管理路由模块，提供文件下载、列表和目录打开等接口。"""

from fastapi import APIRouter
from app.utils.common_utils import get_current_files, get_work_dir
import os
import subprocess
from icecream import ic  # type: ignore[import-unresolved]
from fastapi import HTTPException

router = APIRouter()


@router.get("/download_url")
async def get_download_url(task_id: str, filename: str):
    return {"download_url": f"http://localhost:8000/static/{task_id}/{filename}"}


@router.get("/download_all_url")
async def get_download_all_url(task_id: str):
    return {"download_url": f"http://localhost:8000/static/{task_id}/all.zip"}


@router.get("/files")
async def get_files(task_id: str):
    work_dir = get_work_dir(task_id)
    files = get_current_files(work_dir, "all")
    file_all = []

    for i in files:
        file_type = i.split(".")[-1]
        file_all.append({"filename": i, "file_type": file_type})

    return file_all


@router.get("/open_folder")
async def open_folder(task_id: str):
    ic(task_id)
    # 打开工作目录
    work_dir = get_work_dir(task_id)

    # 打开工作目录
    if os.name == "nt":
        subprocess.run(["explorer", work_dir])
    elif os.name == "posix":
        subprocess.run(["open", work_dir])
    else:
        raise HTTPException(status_code=500, detail=f"不支持的操作系统: {os.name}")

    return {"message": "打开工作目录成功", "work_dir": work_dir}
