"""文件管理路由模块，提供文件下载、列表和目录打开等接口。"""

import os
import shutil
import subprocess
import zipfile
from fastapi import APIRouter, HTTPException
from app.config.setting import settings
from app.utils.common_utils import get_current_files, get_work_dir
from app.utils.log_util import logger

router = APIRouter()


@router.get("/download_url")
async def get_download_url(task_id: str, filename: str):
    """获取指定任务文件的下载链接。"""
    work_dir = get_work_dir(task_id)
    safe_filename = os.path.basename(filename).strip()
    if not safe_filename or safe_filename != filename:
        raise HTTPException(status_code=400, detail="非法文件名")

    target_path = os.path.abspath(os.path.join(work_dir, safe_filename))
    if not target_path.startswith(os.path.abspath(work_dir)) or not os.path.isfile(target_path):
        raise HTTPException(status_code=404, detail="文件不存在")

    host = settings.SERVER_HOST.rstrip("/")
    return {"download_url": f"{host}/static/{task_id}/{safe_filename}"}


@router.get("/download_all_url")
async def get_download_all_url(task_id: str):
    """生成并获取任务所有文件的压缩包下载链接。"""
    work_dir = get_work_dir(task_id)
    zip_path = os.path.join(work_dir, "all.zip")

    # 打包工作目录中的有效生成文件（忽略已有的 all.zip）
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for item in os.listdir(work_dir):
                if item == "all.zip":
                    continue
                item_path = os.path.join(work_dir, item)
                if os.path.isfile(item_path):
                    zf.write(item_path, arcname=item)
                elif os.path.isdir(item_path):
                    for root, _, files in os.walk(item_path):
                        for f in files:
                            full_f = os.path.join(root, f)
                            rel_f = os.path.relpath(full_f, work_dir)
                            zf.write(full_f, arcname=rel_f)
    except Exception as e:
        logger.error(f"生成任务压缩包失败: {e}")
        raise HTTPException(status_code=500, detail="打包工作区文件失败")

    host = settings.SERVER_HOST.rstrip("/")
    return {"download_url": f"{host}/static/{task_id}/all.zip"}


@router.get("/files")
async def get_files(task_id: str):
    """获取工作目录下的所有文件列表。"""
    work_dir = get_work_dir(task_id)
    files = get_current_files(work_dir, "all")
    file_all = []

    for i in files:
        if i == "all.zip":
            continue
        file_type = i.split(".")[-1]
        file_all.append({"filename": i, "file_type": file_type})

    return file_all


@router.get("/open_folder")
async def open_folder(task_id: str):
    """在操作系统文件管理器中打开任务工作目录。"""
    work_dir = get_work_dir(task_id)
    abs_work_dir = os.path.abspath(work_dir)

    try:
        if os.name == "nt":
            # Windows explorer 需要绝对路径
            subprocess.run(["explorer", abs_work_dir], check=False)
        elif os.name == "posix":
            if shutil.which("xdg-open"):
                subprocess.run(["xdg-open", abs_work_dir], check=False)
            elif shutil.which("open"):
                subprocess.run(["open", abs_work_dir], check=False)
            else:
                logger.warning(f"posix 环境未找到 xdg-open 或 open: {abs_work_dir}")
        else:
            raise HTTPException(status_code=500, detail=f"不支持的操作系统: {os.name}")
    except Exception as e:
        logger.warning(f"打开文件资源管理器提示: {e}")

    return {"message": "打开工作目录成功", "work_dir": abs_work_dir}
