"""
Health Check & Metadata Router
"""

from datetime import datetime
from fastapi import APIRouter
from app.schemas import OptionsResponse
from app.services.ml_service import MLService
from app.config import settings

router = APIRouter(tags=["General & Metadata"])

@router.get("/health")
def health_check():
    """Mengecek status kesehatan server dan status kesiapan model AI."""
    try:
        bundle = MLService.load_bundle()
        meta = bundle.get("metadata", {})
        return {
            "status": "healthy",
            "model_ready": True,
            "version": meta.get("version", settings.VERSION),
            "model_architecture": meta.get("model_architecture", "Soft Voting Ensemble (Calibrated)"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as err:
        return {
            "status": "degraded",
            "model_ready": False,
            "error": str(err),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

@router.get("/options", response_model=OptionsResponse)
def get_dropdown_options():
    """Mengambil daftar pilihan resmi untuk komponen form dropdown di antarmuka Frontend."""
    return OptionsResponse(
        satuan_durasi_tersedia=["hari", "minggu", "bulan", "tahun"],
        jenis_kelamin_options=["Laki-laki", "Perempuan"],
        pendidikan_options=["SMA / SMK", "Diploma (D3)", "S1", "S2 / S3"],
        siapa_mengakhiri_options=["Saya yang mengakhiri", "Pasangan yang mengakhiri", "Keputusan bersama"],
        masih_komunikasi_options=["Tidak sama sekali", "Jarang", "Kadang-kadang", "Sering"],
        frekuensi_medsos_options=["Tidak pernah", "Jarang", "Kadang-kadang", "Sering"]
    )
