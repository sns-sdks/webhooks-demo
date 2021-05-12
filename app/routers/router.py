from fastapi import APIRouter

from app.routers import facebook, twitter

router = APIRouter(prefix="/webhook")
router.include_router(router=facebook.router, tags=["facebook"])
router.include_router(router=twitter.router, tags=["twitter"])
