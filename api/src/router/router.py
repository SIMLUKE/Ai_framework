from fastapi import APIRouter

global_router = APIRouter()

@global_router.get("/")
async def root():
    return "api called successfully"
