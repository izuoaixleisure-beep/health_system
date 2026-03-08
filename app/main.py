import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

# 自动建表（首次运行时）
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 配置：从环境变量读取，默认允许所有（方便 Docker 内网通信）
# 原因：Docker 容器间通过内网通信，前端是 Nginx 反向代理，源可能不同
# 生产环境建议设为具体域名，如 ["https://yourdomain.com"]
allow_origins = os.getenv("ALLOW_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import user, resident, health

app.include_router(user.router)
app.include_router(resident.router)
app.include_router(health.router)


# 公共健康检查端点（用于 Docker 健康检查，无需认证）
@app.get("/ping")
def ping():
    return {"status": "ok"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True)
