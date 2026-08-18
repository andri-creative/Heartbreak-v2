"""
Machine Learning Classifier Service for Heartbreak AI V3
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from app.config import settings

class MLService:
    """Singleton service untuk memuat model bundle V3 dan menjalankan inferensi proporsional."""
    
    _bundle: Dict[str, Any] = {}
    
    @classmethod
    def load_bundle(cls) -> Dict[str, Any]:
        """Memuat bundle model ke memori dengan fallback aman."""
        if cls._bundle:
            return cls._bundle
            
        candidate_paths = [
            settings.MODEL_BUNDLE_PATH,
            os.path.join(os.path.dirname(__file__), "..", "..", "heartbreak_demographic_bundle_v3.pkl"),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "heartbreak_demographic_bundle_v3.pkl"),
            "heartbreak_demographic_bundle_v3.pkl",
            "heartbreak_demographic_bundle_v2.pkl",
            os.path.join(os.path.dirname(__file__), "..", "..", "heartbreak_demographic_bundle_v2.pkl")
        ]
        
        for path in candidate_paths:
            if os.path.exists(path):
                try:
                    cls._bundle = joblib.load(path)
                    return cls._bundle
                except Exception as e:
                    # Fallback jika unpickling error di lokal
                    pass
        
        # Fallback schema jika file bundle belum diekspor atau dependensi unpickle berbeda di environment lokal
        cls._bundle = {
            'feature_names': [
                'Umur', 'durasi_hubungan_bulan', 'durasi_putus_bulan', 'tingkat_pendidikan_ordinal',
                'life_stage_score', 'is_usia_sekolah', 'is_dewasa_awal', 'is_dewasa_matang',
                'recovery_ratio', 'log_recovery_index', 'umur_mulai_hubungan',
                'emotional_vulnerability_index', 'cognitive_resilience_ratio', 'relational_maturity_index'
            ],
            'scaler': None,
            'default_values': {
                'Jenis Kelamin': 'Perempuan',
                'Pendidikan': 'S1',
                'Siapa yang Mengakhiri Hubungan?': 'Pasangan yang mengakhiri',
                'Apakah Masih Berkomunikasi dengan Mantan?': 'Tidak sama sekali',
                'Seberapa Sering Melihat Media Sosial Mantan?': 'Jarang'
            },
            'metadata': {
                'version': settings.VERSION,
                'model_architecture': 'Proportional Relational & Cognitive Maturity AI V3'
            }
        }
        return cls._bundle

    @classmethod
    def get_psychological_profile(cls, umur: float, pendidikan: str, durasi_hub_bln: float, durasi_putus_bln: float) -> str:
        """Insight psikologi kognitif berbasis tahapan perkembangan dan rasio relasi."""
        rasio = durasi_putus_bln / (durasi_hub_bln + 1e-5)
        p_str = str(pendidikan) if pendidikan else 'Tidak Disebutkan'
        if umur <= 18.0:
            return (
                f"🧠 Profil Kognitif Usia {int(umur)} Tahun ({p_str}):\n"
                f"   • Fase Perkembangan : Remaja / Usia Sekolah (Prefrontal Cortex Masih Berkembang).\n"
                f"   • Dinamika Emosional: Hubungan {durasi_hub_bln:.1f} bulan di usia sekolah membentuk keterikatan identitas yang intens.\n"
                f"                         Masa putus {durasi_putus_bln:.1f} bulan (rasio {rasio:.2f}) memerlukan dukungan teman sebaya dan rutinitas belajar.\n"
                f"   • Fokus Pemulihan   : Batasi kontak mantan, fokus eksplorasi bakat/hobi, dan perkuat pertemanan positif."
            )
        elif umur <= 22.0:
            return (
                f"🧠 Profil Kognitif Usia {int(umur)} Tahun ({p_str}):\n"
                f"   • Fase Perkembangan : Dewasa Awal / Kuliah-Fresh Graduate (Quarter-Life Transition).\n"
                f"   • Dinamika Emosional: Nalar kognitif mandiri membantu menyeimbangkan pemulihan emosi dengan target masa depan.\n"
                f"                         Rasio pemulihan {rasio:.2f} menunjukkan transisi menuju kestabilan hidup yang terarah.\n"
                f"   • Fokus Pemulihan   : Akselerasi karir/studi, perluas networking profesional, dan tetapkan standar relasi yang lebih matang."
            )
        else:
            return (
                f"🧠 Profil Kognitif Usia {int(umur)} Tahun ({p_str}):\n"
                f"   • Fase Perkembangan : Dewasa Produktif / Matang (Regulasi Diri Stabil).\n"
                f"   • Dinamika Emosional: Kematangan emosional dan pemecahan masalah rasional membuat pemulihan lebih terstruktur.\n"
                f"   • Fokus Pemulihan   : Menjaga work-life balance dan merajut kembali visi masa depan jangka panjang."
            )

    @classmethod
    def predict_severity(
        cls,
        df_scaled: pd.DataFrame,
        umur: float,
        pendidikan: str,
        durasi_hub_bln: float,
        durasi_putus_bln: float
    ) -> Tuple[str, str, str, float, float, str, list]:
        """
        Menghitung keparahan patah hati menggunakan Formula Proporsional Relasional V3:
          1. Rasio Pemulihan (Durasi Putus / Durasi Hubungan)
          2. Faktor Kematangan Usia & Pendidikan
          3. Target Pemulihan Dinamis (3-Tier Clinical)
        """
        # 1. Faktor Kematangan Usia & Pendidikan
        maturity_factor = 1.25 if (umur >= 22.0 or pendidikan in ['S1', 'S2', 'S3']) else 0.85
        
        # 2. Ambang Batas Waktu Pemulihan Dinamis
        target_ringan_bulan = max(3.0, (durasi_hub_bln * 0.25) / maturity_factor)
        target_sedang_bulan = max(1.5, (durasi_hub_bln * 0.08) / maturity_factor)
        
        # 3. Perhitungan Distres Proporsional (%)
        if durasi_putus_bln <= target_sedang_bulan:
            progress_akut = durasi_putus_bln / target_sedang_bulan
            prob_distres = 75.0 + (20.0 * (1.0 - progress_akut))
            pred_label = "Berat"
            badge = "🔴"
            status_desc = "Keparahan Patah Hati Tinggi / Akut (Fase Shock & Distres Awal Putus)"
            saran = [
                "Prioritas Utama: Sangat dianjurkan berkonsultasi dengan psikolog atau konselor profesional untuk pendampingan reguler.",
                "Terapkan STRICT NO-CONTACT: Blokir/mute semua akses media sosial mantan untuk memutus siklus distres.",
                "Jangan menahan beban sendirian; libatkan keluarga atau support system terdekat yang aman dan suportif.",
                "Jaga kebutuhan fisik esensial: istirahat cukup, hindari isolasi diri berkepanjangan, dan tunda keputusan hidup yang besar."
            ]
        elif durasi_putus_bln < target_ringan_bulan:
            progress_transisi = (durasi_putus_bln - target_sedang_bulan) / (target_ringan_bulan - target_sedang_bulan + 1e-5)
            prob_distres = 68.0 - (33.0 * progress_transisi)
            pred_label = "Sedang"
            badge = "🟡"
            status_desc = "Keparahan Patah Hati Moderat (Fase Transisi & Adaptasi Emosional)"
            saran = [
                "Terapkan aturan No-Contact (batasi komunikasi dan hindari stalking media sosial mantan).",
                "Salurkan emosi kesedihan melalui journaling, olahraga rutin, atau bercerita ke sahabat terpercaya.",
                "Berikan waktu bagi diri sendiri untuk berduka tanpa merasa bersalah (self-compassion)."
            ]
        else:
            lewat_target = durasi_putus_bln - target_ringan_bulan
            prob_distres = 28.0 * np.exp(-lewat_target / 6.0)
            prob_distres = max(5.0, prob_distres)
            pred_label = "Ringan"
            badge = "🟢"
            status_desc = "Keparahan Patah Hati Rendah (Fase Pemulihan Adaptif / Pulih / Move On)"
            saran = [
                "Pertahankan rutinitas positif harian dan aktivitas produktif yang sedang berjalan.",
                "Fokus pada pengembangan diri, hobi baru, dan pencapaian target masa depan.",
                "Buka diri secara perlahan untuk memperluas lingkaran sosial yang sehat."
            ]
            
        prob_distres = float(round(np.clip(prob_distres, 5.0, 95.0), 1))
        prob_ringan = float(round(100.0 - prob_distres, 1))
        profil_kognitif = cls.get_psychological_profile(umur, pendidikan, durasi_hub_bln, durasi_putus_bln)
        
        return pred_label, badge, status_desc, prob_ringan, prob_distres, profil_kognitif, saran
