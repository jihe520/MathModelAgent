from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World from Sandbox"}


@router.get("/config")
async def config():
    return {}


@router.get("/status")
async def get_service_status():
    """健康检查接口"""
    return {"status": "running", "message": "Sandbox service is running"}


@router.get("/info")
async def get_sandbox_info():
    """获取沙盒环境信息"""
    return {}
