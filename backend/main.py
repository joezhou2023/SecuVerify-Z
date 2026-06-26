"""
安鉴·周 / SecuVerify-Z — ISO 27001 AI 审核助手
后端主应用入口
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import chat, file_audit, clause_match

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="安鉴·周 / SecuVerify-Z",
    description="ISO 27001 AI 审核助手 — 文件审核、条款匹配、对话式审核引导",
    version="1.4.0",
)

# CORS 配置（开发环境允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传目录存在
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# 注册路由
app.include_router(chat.router, prefix="/api/chat", tags=["对话审核"])
app.include_router(file_audit.router, prefix="/api/file-audit", tags=["文件审核"])
app.include_router(clause_match.router, prefix="/api/clause-match", tags=["条款匹配"])


@app.get("/")
async def root():
    return {
        "name": "安鉴·周 / SecuVerify-Z",
        "version": "1.4.0",
        "description": "ISO 27001 AI 审核助手",
        "docs": "/docs",
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "SecuVerify-Z"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
