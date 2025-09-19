from fastapi import APIRouter

from . import common_router, files_router, interpreter_router, shell_router

api_router = APIRouter()
api_router.include_router(common_router.router, tags=["common"])
api_router.include_router(files_router.router, prefix="/files", tags=["files"])
api_router.include_router(
    interpreter_router.router, prefix="/interpreter", tags=["interpreter"]
)
api_router.include_router(shell_router.router, prefix="/shell", tags=["shell"])
