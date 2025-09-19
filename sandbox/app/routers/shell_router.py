from fastapi import APIRouter

router = APIRouter()


@router.get("/exec")
async def exec_shell():
    """运行shell命令"""
    return {}
