import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import rooms, guests, business

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="酒店客房管理系统",
    description="简化且模块化的酒店管理系统后端 API (基于 FastAPI 和 SQL Server)",
    version="1.0.0",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册子模块路由
app.include_router(rooms.router, prefix="/rooms")
app.include_router(guests.router, prefix="/guests")
app.include_router(business.router, prefix="/business")

@app.get("/")
def read_root():
    return {"message": "欢迎使用酒店客房管理系统 API。请访问 /docs 查看 Swagger 文档。"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
