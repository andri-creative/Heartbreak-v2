"""
Machine Learning Classifier Service for Heartbreak AI V2
"""

import os
import joblib
import pandas as pd
from typing import Dict, Any, Tuple
from app.config import settings

class MLService:
    """Singleton service untuk memuat model bundle dan menjalankan inferensi."""
    
    _bundle: Dict[str, Any] = {}
    
    @classmethod
    def load_bundle(cls) -> Dict[str, Any]:
        """Memuat bundle model ke memori."""
        if cls._bundle:
            return cls._bundle
            
        candidate_paths = [
            settings.MODEL_BUNDLE_PATH,
            os.path.join(os.path.dirname(__file__), "..", "..", "heartbreak_demographic_bundle_v2.pkl"),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "heartbreak_demographic_bundle_v2.pkl"),
            "heartbreak_demographic_bundle_v2.pkl"
        ]
        
        for path in candidate_paths:
            if os.path.exists(path):
                cls._bundle = joblib.load(path)
                # print(f"✅ MLService: Model bundle berhasil dimuat dari '{path}'")
                return cls._bundle
                
        raise FileNotFoundError(
            f"❌ Model bundle tidak ditemukan di lokasi mana pun: {candidate_paths}. "
            "Pastikan file 'heartbreak_demographic_bundle_v2.pkl' sudah diekspor."
        )

    @classmethod
    def predict_severity(cls, df_scaled: pd.DataFrame) -> Tuple[str, str, str, float, float, list]:
        """
        Menghitung probabilitas terkalibrasi dan mengembalikan kategori 3-Tier Severity.
        """
        bundle = cls.load_bundle()
        model = bundle['model']
        
        pred_proba = model.predict_proba(df_scaled)[0]
        prob_ringan = round(float(pred_proba[0] * 100), 2)
        prob_distres = round(float(pred_proba[1] * 100) if len(pred_proba) > 1 else (100.0 - prob_ringan), 2)
        
        # 3-Tier Clinical Thresholding
        if prob_distres >= settings.THRESHOLD_BERAT:
            pred_label = "Berat"
            badge = "🔴"
            status_desc = "Keparahan Patah Hati Tinggi / Akut (Distres Emosional Intensif)"
            saran = [
                "Prioritas Utama: Sangat dianjurkan berkonsultasi dengan psikolog atau konselor profesional untuk pendampingan reguler.",
                "Terapkan STRICT NO-CONTACT: Blokir/mute semua akses media sosial mantan untuk memutus siklus distres.",
                "Jangan menahan beban sendirian; libatkan keluarga atau support system terdekat yang aman dan suportif.",
                "Jaga kebutuhan fisik esensial: istirahat cukup, hindari isolasi diri berkepanjangan, dan tunda keputusan hidup yang besar."
            ]
        elif prob_distres >= settings.THRESHOLD_SEDANG:
            pred_label = "Sedang"
            badge = "🟡"
            status_desc = "Keparahan Patah Hati Moderat (Fase Transisi & Adaptasi Emosional)"
            saran = [
                "Terapkan aturan No-Contact (batasi komunikasi dan hindari stalking media sosial mantan).",
                "Salurkan emosi kesedihan melalui journaling, olahraga rutin, atau bercerita ke sahabat terpercaya.",
                "Berikan waktu bagi diri sendiri untuk berduka tanpa merasa bersalah (self-compassion)."
            ]
        else:
            pred_label = "Ringan"
            badge = "🟢"
            status_desc = "Keparahan Patah Hati Rendah (Adaptif, Stabil, & Pulih)"
            saran = [
                "Pertahankan rutinitas positif harian dan aktivitas produktif yang sedang berjalan.",
                "Fokus pada pengembangan diri, hobi baru, dan pencapaian target masa depan.",
                "Buka diri secara perlahan untuk memperluas lingkaran sosial yang sehat."
            ]
            
        return pred_label, badge, status_desc, prob_ringan, prob_distres, saran
