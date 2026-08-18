"""
Prediction & AI Psychologist Counsel Router — Heartbreak AI V3
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.schemas import PredictionInput, PredictionResponse, PredictionData, AICounselRequest, AICounselResponseData
from app.services.preprocessor import transform_user_input
from app.services.ml_service import MLService
from app.services.ai_coach_service import AICoachService

router = APIRouter(tags=["AI Inference & Recovery"])

@router.post("/predict", response_model=PredictionResponse)
def predict_heartbreak_severity(payload: PredictionInput):
    """
    Endpoint Utama Inferensi Heartbreak AI V3:
    - Menerima 4 input utama (Nama, Umur, Pendidikan, Durasi Hubungan, Durasi Sejak Putus) dan opsi demografis.
    - Menghitung klasifikasi 3-Tier Severity (Ringan / Sedang / Berat) berbasis Formula Proporsional Relasional V3.
    - Menghasilkan Profil Kognitif & Rekomendasi Pemulihan dari AI Psychologist Coach.
    """
    try:
        bundle = MLService.load_bundle()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Model bundle belum siap: {str(e)}"
        )
        
    feature_names = bundle['feature_names']
    scaler = bundle['scaler']
    default_values = bundle.get('default_values', {})
    
    try:
        df_scaled, duration_detail, resolved_demographics = transform_user_input(
            payload=payload,
            feature_names=feature_names,
            scaler=scaler,
            default_values=default_values
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    
    # 1. Inferensi Machine Learning & Formula Klinis V3
    pred_label, badge, status_desc, prob_ringan, prob_distres, profil_kognitif, saran = MLService.predict_severity(
        df_scaled=df_scaled,
        umur=payload.umur,
        pendidikan=resolved_demographics['pendidikan'],
        durasi_hub_bln=duration_detail.durasi_hubungan_bulan,
        durasi_putus_bln=duration_detail.durasi_putus_bulan
    )
    
    # 2. Generasi AI Psychologist Insight
    ai_insight = AICoachService.generate_ai_insight(
        payload=payload,
        kategori_severity=pred_label,
        prob_distres=prob_distres,
        resolved_demographics=resolved_demographics
    )
    
    prediction_data = PredictionData(
        nama=payload.nama,
        umur=payload.umur,
        pendidikan=resolved_demographics['pendidikan'],
        kategori_severity=pred_label,
        badge=badge,
        deskripsi_status=status_desc,
        probabilitas_ringan=prob_ringan,
        probabilitas_distres=prob_distres,
        detail_durasi=duration_detail,
        profil_kognitif=profil_kognitif,
        rekomendasi_psikologis=saran,
        ai_psychologist_insight=ai_insight
    )
    
    return PredictionResponse(
        success=True,
        message="Analisis keparahan patah hati dan konsultasi kognitif AI V3 berhasil dilakukan.",
        version="3.0.0",
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data=prediction_data
    )


@router.post("/counsel", response_model=AICounselResponseData)
def direct_ai_counsel(payload: AICounselRequest):
    """
    Endpoint Konseling Interaktif AI Psychologist:
    Menerima konteks data patah hati pengguna + pesan curhat bebas, lalu memberikan respons kognitif empatik.
    """
    bundle = MLService.load_bundle()
    feature_names = bundle['feature_names']
    scaler = bundle['scaler']
    default_values = bundle.get('default_values', {})
    
    df_scaled, duration_detail, resolved_demographics = transform_user_input(
        payload=payload.prediction_context,
        feature_names=feature_names,
        scaler=scaler,
        default_values=default_values
    )
    
    pred_label, _, _, _, prob_distres, _, _ = MLService.predict_severity(
        df_scaled=df_scaled,
        umur=payload.prediction_context.umur,
        pendidikan=resolved_demographics['pendidikan'],
        durasi_hub_bln=duration_detail.durasi_hubungan_bulan,
        durasi_putus_bln=duration_detail.durasi_putus_bulan
    )
    
    ai_insight = AICoachService.generate_ai_insight(
        payload=payload.prediction_context,
        kategori_severity=pred_label,
        prob_distres=prob_distres,
        resolved_demographics=resolved_demographics,
        user_curhat=payload.user_curhat
    )
    
    return ai_insight
