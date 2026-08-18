"""
Pydantic Request & Response Schemas — Heartbreak AI V3
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# =====================================================================
# REQUEST SCHEMAS
# =====================================================================

class PredictionInput(BaseModel):
    # 4 Input Wajib / Kunci V3
    nama: str = Field(..., example="Rian Pratama", description="Nama responden / pengguna")
    umur: float = Field(..., ge=12, le=100, example=22, description="Usia responden (tahun)")
    pendidikan: Optional[str] = Field("S1", example="S1", description="'SMP/Sederajat' | 'SMA/Sederajat' | 'Diploma (D1/D2/D3)' | 'S1' | 'S2' | 'S3'")
    
    # Durasi Hubungan (Wajib)
    lama_hubungan_nilai: float = Field(..., gt=0, example=2, description="Nilai durasi hubungan")
    lama_hubungan_satuan: str = Field(..., example="tahun", description="Satuan durasi: 'hari' | 'minggu' | 'bulan' | 'tahun'")
    
    # Durasi Sejak Putus (Wajib)
    sejak_putus_nilai: float = Field(..., ge=0, example=6, description="Nilai durasi sejak putus")
    sejak_putus_satuan: str = Field(..., example="bulan", description="Satuan durasi: 'hari' | 'minggu' | 'bulan' | 'tahun'")
    
    # 4 Input Opsional Tambahan
    jenis_kelamin: Optional[str] = Field(None, example="Laki-laki", description="'Laki-laki' | 'Perempuan'")
    siapa_mengakhiri: Optional[str] = Field(None, example="Pasangan yang mengakhiri", description="'Saya yang mengakhiri' | 'Pasangan yang mengakhiri' | 'Keputusan bersama'")
    masih_komunikasi: Optional[str] = Field(None, example="Tidak sama sekali", description="'Tidak sama sekali' | 'Jarang' | 'Kadang-kadang' | 'Sering' | 'Setiap hari'")
    frekuensi_medsos: Optional[str] = Field(None, example="Jarang", description="'Tidak pernah' | 'Jarang' | 'Kadang-kadang' | 'Sekali sehari' | 'Hampir setiap hari' | 'Beberapa kali sehari'")


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
    target_ringan_bulan: float
    life_stage_label: str
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
    pendidikan: str
    kategori_severity: str
    badge: str
    deskripsi_status: str
    probabilitas_ringan: float
    probabilitas_distres: float
    detail_durasi: DurationDetail
    profil_kognitif: str
    rekomendasi_psikologis: List[str]
    ai_psychologist_insight: AICounselResponseData

class PredictionResponse(BaseModel):
    success: bool
    message: str
    version: str = "3.0.0"
    timestamp: str
    data: PredictionData

class OptionsResponse(BaseModel):
    satuan_durasi_tersedia: List[str]
    jenis_kelamin_options: List[str]
    pendidikan_options: List[str]
    siapa_mengakhiri_options: List[str]
    masih_komunikasi_options: List[str]
    frekuensi_medsos_options: List[str]
