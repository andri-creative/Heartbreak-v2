"""
Prediction & AI Psychologist Counsel Router
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
    Endpoint Utama Inferensi Heartbreak AI V2:
    - Menerima 3 input wajib (Umur, Durasi Hubungan, Durasi Sejak Putus) dan opsi demografis opsional.
    - Menghitung klasifikasi 3-Tier Severity (Ringan / Sedang / Berat) & Probabilitas Terkalibrasi.
    - Menghasilkan Insight Psikologis Personal & Rekomendasi Pemulihan Otomatis dari AI Coach.
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
    default_values = bundle['default_values']
    
    try:
        df_scaled, duration_detail, resolved_demographics = transform_user_input(
            payload=payload,
            feature_names=feature_names,
            scaler=scaler,
            default_values=default_values
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    
    # 1. Inferensi Machine Learning
    pred_label, badge, status_desc, prob_ringan, prob_distres, saran = MLService.predict_severity(df_scaled)
    
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
        kategori_severity=pred_label,
        badge=badge,
        deskripsi_status=status_desc,
        probabilitas_ringan=prob_ringan,
        probabilitas_distres=prob_distres,
        detail_durasi=duration_detail,
        rekomendasi_psikologis=saran,
        ai_psychologist_insight=ai_insight
    )
    
    return PredictionResponse(
        success=True,
        message="Analisis tingkat keparahan patah hati dan konsultasi AI berhasil dilakukan.",
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
    default_values = bundle['default_values']
    
    df_scaled, _, resolved_demographics = transform_user_input(
        payload=payload.prediction_context,
        feature_names=feature_names,
        scaler=scaler,
        default_values=default_values
    )
    
    pred_label, _, _, _, prob_distres, _ = MLService.predict_severity(df_scaled)
    
    ai_insight = AICoachService.generate_ai_insight(
        payload=payload.prediction_context,
        kategori_severity=pred_label,
        prob_distres=prob_distres,
        resolved_demographics=resolved_demographics,
        user_curhat=payload.user_curhat
    )
    
    return ai_insight
