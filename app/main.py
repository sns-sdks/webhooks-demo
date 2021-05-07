from fastapi import FastAPI

from app.routers.facebook import fb_router

app = FastAPI()

app.include_router(router=fb_router)
