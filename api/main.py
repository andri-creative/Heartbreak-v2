"""
Entry Point Server FastAPI — Heartbreak AI V3
Melayani Web UI Frontend Interaktif dan REST API Endpoints.
"""

import os
import warnings
from contextlib import asynccontextmanager

warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, predict
from app.services.ml_service import MLService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler untuk inisialisasi model saat startup."""
    try:
        MLService.load_bundle()
    except Exception as e:
        pass
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Production-ready REST API & Web App untuk Klasifikasi Keparahan Patah Hati (V3) "
        "menggunakan Formula Relasional Dinamis, Tahap Perkembangan Kognitif Usia & Pendidikan, "
        "serta AI Emotional Recovery Psychologist Coach."
    ),
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Register API Routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(health.router)
app.include_router(predict.router, prefix=settings.API_PREFIX)

@app.get("/", tags=["Frontend Web UI"])
def serve_ui():
    """Melayani Web UI Frontend Modern di root URL."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Online & Ready (V3)",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Heartbreak AI V3 Web App berjalan di http://localhost:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
