from fastapi import APIRouter

router = APIRouter()


@router.get("/execute_code")
async def execute_code():
    return {}
