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
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, predict
from app.services.ml_service import MLService

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler untuk inisialisasi model saat startup."""
    try:
        MLService.load_bundle()
    except Exception:
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

# Mount Static Files (Mendukung lokal dan serverless cloud)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(os.getcwd(), "api", "static")
if not os.path.exists(STATIC_DIR):
    STATIC_DIR = os.path.join(os.getcwd(), "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Register API Routers
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(health.router)
app.include_router(predict.router, prefix=settings.API_PREFIX)
app.include_router(predict.router)  # Memungkinkan akses langsung /predict

def get_html_content() -> str:
    """Membaca isi file index.html dengan pencarian multi-path aman."""
    candidate_paths = [
        os.path.join(STATIC_DIR, "index.html"),
        os.path.join(os.path.dirname(__file__), "static", "index.html"),
        os.path.join(os.getcwd(), "api", "static", "index.html"),
        os.path.join(os.getcwd(), "static", "index.html"),
        "api/static/index.html",
        "static/index.html"
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return f"""
    <!DOCTYPE html>
    <html>
    <head><title>{settings.PROJECT_NAME}</title></head>
    <body style="font-family:sans-serif;text-align:center;padding:50px;">
      <h1>❤️‍🩹 Heartbreak AI V3 Online</h1>
      <p>API Version: {settings.VERSION} | Status: Healthy & Ready</p>
      <p><a href="/docs">Buka Dokumentasi Swagger API (/docs)</a></p>
    </body>
    </html>
    """

@app.get("/", tags=["Frontend Web UI"])
@app.get("/api", tags=["Frontend Web UI"])
@app.get("/api/", tags=["Frontend Web UI"])
@app.get("/index.py", tags=["Frontend Web UI"])
@app.get("/api/index.py", tags=["Frontend Web UI"])
def serve_ui():
    """Melayani Web UI Frontend Modern di semua alias routing Vercel."""
    html_content = get_html_content()
    return HTMLResponse(content=html_content, status_code=200)

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Heartbreak AI V3 Web App berjalan di http://localhost:{settings.PORT}")
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
