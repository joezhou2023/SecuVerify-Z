"""
安鉴·周 / SecuVerify-Z — ISO 27001 AI 审核助手
后端主应用入口（单进程部署模式：后端 API + 前端静态文件）
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import chat, file_audit, clause_match

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="安鉴·周 / SecuVerify-Z",
    description="ISO 27001 AI 审核助手 — 文件审核、条款匹配、对话式审核引导",
    version="1.5.0",
)

# CORS 配置
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传目录存在
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# 静态文件目录（前端构建产物）
STATIC_DIR = Path(__file__).parent / "static"
IS_PROD = STATIC_DIR.exists() and (STATIC_DIR / "index.html").exists()

# 注册路由（必须先注册 API 路由，再注册静态文件）
app.include_router(chat.router, prefix="/api/chat", tags=["对话审核"])
app.include_router(file_audit.router, prefix="/api/file-audit", tags=["文件审核"])
app.include_router(clause_match.router, prefix="/api/clause-match", tags=["条款匹配"])


@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "SecuVerify-Z"}


if IS_PROD:
    # 生产模式：挂载静态文件 + SPA fallback
    app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # API 路径已在上面注册，不会走到这里
        # 返回 index.html 支持 SPA 路由
        index_file = STATIC_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"error": "Frontend not found"}
else:
    # 开发模式
    @app.get("/")
    async def root():
        return {
            "name": "安鉴·周 / SecuVerify-Z",
            "version": "1.5.0",
            "description": "ISO 27001 AI 审核助手",
            "docs": "/docs",
        }


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload_mode = os.getenv("RELOAD", "true").lower() == "true"
    uvicorn.run("main:app", host=host, port=port, reload=reload_mode)
