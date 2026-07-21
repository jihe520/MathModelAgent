"""文件管理路由模块，提供文件下载、列表和目录打开等接口。"""

import os
import subprocess
from urllib.parse import quote

from fastapi import APIRouter, HTTPException

from app.utils.common_utils import get_current_files, get_work_dir
from app.utils.path_utils import (
    ensure_safe_task_id,
    resolve_path_within,
)
from icecream import ic  # type: ignore[import-unresolved]

router = APIRouter()


def _require_work_dir(task_id: str) -> tuple[str, str]:
    """Return a validated task ID and its existing work directory."""
    try:
        safe_task_id = ensure_safe_task_id(task_id)
        return safe_task_id, get_work_dir(safe_task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="任务不存在") from exc


@router.get("/download_url")
async def get_download_url(task_id: str, filename: str):
    safe_task_id, work_dir = _require_work_dir(task_id)
    try:
        safe_filename = resolve_path_within(work_dir, filename).name
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "download_url": (
            "http://localhost:8000/static/"
            f"{quote(safe_task_id, safe='')}/{quote(safe_filename, safe='')}"
        )
    }


@router.get("/download_all_url")
async def get_download_all_url(task_id: str):
    safe_task_id, _ = _require_work_dir(task_id)
    return {
        "download_url": f"http://localhost:8000/static/{quote(safe_task_id, safe='')}/all.zip"
    }


@router.get("/files")
async def get_files(task_id: str):
    _, work_dir = _require_work_dir(task_id)
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
    _, work_dir = _require_work_dir(task_id)

    # 打开工作目录
    if os.name == "nt":
        subprocess.run(["explorer", work_dir])
    elif os.name == "posix":
        subprocess.run(["open", work_dir])
    else:
        raise HTTPException(status_code=500, detail=f"不支持的操作系统: {os.name}")

    return {"message": "打开工作目录成功", "work_dir": work_dir}
