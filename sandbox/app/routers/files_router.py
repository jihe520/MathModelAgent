from fastapi import APIRouter

router = APIRouter()


@router.get("/list_files")
async def list_files():
    return {}
