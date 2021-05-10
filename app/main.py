from fastapi import FastAPI

from app.routers.facebook import fb_router
from app.routers.twitter import tw_router

app = FastAPI()

app.include_router(router=fb_router)
app.include_router(router=tw_router)
