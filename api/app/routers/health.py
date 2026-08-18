"""
Health Check & Metadata Router — Heartbreak AI V3
"""

from datetime import datetime
from fastapi import APIRouter
from app.schemas import OptionsResponse
from app.services.ml_service import MLService
from app.config import settings

router = APIRouter(tags=["General & Metadata"])

@router.get("/health")
def health_check():
    """Mengecek status kesehatan server dan status kesiapan model AI V3."""
    try:
        bundle = MLService.load_bundle()
        meta = bundle.get("metadata", {})
        return {
            "status": "healthy",
            "model_ready": True,
            "version": meta.get("version", settings.VERSION),
            "model_architecture": meta.get("model_architecture", "Soft Voting Ensemble (Calibrated V3)"),
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
        pendidikan_options=["SMP/Sederajat", "SMA/Sederajat", "SMA / SMK", "Diploma (D1/D2/D3)", "Diploma (D3)", "S1", "S2", "S2 / S3", "S3"],
        siapa_mengakhiri_options=["Saya yang mengakhiri", "Pasangan yang mengakhiri", "Keputusan bersama", "Tidak jelas"],
        masih_komunikasi_options=["Tidak sama sekali", "Jarang", "Kadang-kadang", "Sering", "Setiap hari"],
        frekuensi_medsos_options=["Tidak pernah", "Jarang", "Kadang-kadang", "Sekali sehari", "Hampir setiap hari", "Beberapa kali sehari"]
    )
