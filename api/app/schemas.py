"""
Pydantic Request & Response Schemas
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# =====================================================================
# REQUEST SCHEMAS
# =====================================================================

class PredictionInput(BaseModel):
    # 3 Input Wajib
    nama: str = Field(..., example="Dimas Anggara", description="Nama responden / pengguna")
    umur: float = Field(..., ge=12, le=100, example=22, description="Usia responden (tahun)")
    
    # Durasi Hubungan (Wajib)
    lama_hubungan_nilai: float = Field(..., gt=0, example=2, description="Nilai durasi hubungan")
    lama_hubungan_satuan: str = Field(..., example="tahun", description="Satuan durasi: 'hari' | 'minggu' | 'bulan' | 'tahun'")
    
    # Durasi Sejak Putus (Wajib)
    sejak_putus_nilai: float = Field(..., ge=0, example=3, description="Nilai durasi sejak putus")
    sejak_putus_satuan: str = Field(..., example="bulan", description="Satuan durasi: 'hari' | 'minggu' | 'bulan' | 'tahun'")
    
    # 5 Input Opsional (Fallback otomatis jika None)
    jenis_kelamin: Optional[str] = Field(None, example="Laki-laki", description="'Laki-laki' | 'Perempuan'")
    pendidikan: Optional[str] = Field(None, example="S1", description="'SMA / SMK' | 'Diploma (D3)' | 'S1' | 'S2 / S3'")
    siapa_mengakhiri: Optional[str] = Field(None, example="Pasangan yang mengakhiri", description="'Saya yang mengakhiri' | 'Pasangan yang mengakhiri' | 'Keputusan bersama'")
    masih_komunikasi: Optional[str] = Field(None, example="Kadang-kadang", description="'Tidak sama sekali' | 'Jarang' | 'Kadang-kadang' | 'Sering'")
    frekuensi_medsos: Optional[str] = Field(None, example="Kadang-kadang", description="'Tidak pernah' | 'Jarang' | 'Kadang-kadang' | 'Sering'")


class AICounselRequest(BaseModel):
    prediction_context: PredictionInput
    user_curhat: Optional[str] = Field(
        None,
        example="Saya masih sering kepikiran dia dan susah tidur setiap malam. Apa yang harus saya lakukan?",
        description="Pesan curhat atau pertanyaan emosional dari pengguna ke AI Psychologist Coach"
    )

# =====================================================================
# RESPONSE SCHEMAS
# =====================================================================

class DurationDetail(BaseModel):
    durasi_hubungan_bulan: float
    durasi_putus_bulan: float
    kategori_lama_hubungan: str
    kategori_sejak_putus: str
    rasio_pemulihan: float
    fallback_opsional_digunakan: bool

class AICounselResponseData(BaseModel):
    headline_empati: str
    analisis_kondisi: str
    langkah_pemulihan_personal: List[str]
    afirmasi_harian: str
    peringatan_psikologis: Optional[str] = None

class PredictionData(BaseModel):
    nama: str
    umur: float
    kategori_severity: str
    badge: str
    deskripsi_status: str
    probabilitas_ringan: float
    probabilitas_distres: float
    detail_durasi: DurationDetail
    rekomendasi_psikologis: List[str]
    ai_psychologist_insight: AICounselResponseData

class PredictionResponse(BaseModel):
    success: bool
    message: str
    timestamp: str
    data: PredictionData

class OptionsResponse(BaseModel):
    satuan_durasi_tersedia: List[str]
    jenis_kelamin_options: List[str]
    pendidikan_options: List[str]
    siapa_mengakhiri_options: List[str]
    masih_komunikasi_options: List[str]
    frekuensi_medsos_options: List[str]
