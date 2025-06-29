from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List
from contextlib import asynccontextmanager
from database.connection import conn

from routes.users import user_router
from routes.events import event_router

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup 이벤트
    conn()
    yield
    # shutdown 이벤트 시 정리 작업이 필요하면 여기에 작성

app = FastAPI(lifespan=lifespan)

# 라우트 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.get("/")
async def home():
    return RedirectResponse(url="/event")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)