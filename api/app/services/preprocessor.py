"""
Modul Preprocessing & Transformer Fitur Input Pengguna — Heartbreak AI V3
"""

import re
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from app.schemas import PredictionInput, DurationDetail

def convert_ke_bulan(nilai: float, satuan: str) -> float:
    """Mengonversi input durasi alami (hari/minggu/bulan/tahun) ke skala bulan."""
    satuan = str(satuan).strip().lower()
    konversi = {
        'hari': 1.0 / 30.0,
        'hari-hari': 1.0 / 30.0,
        'day': 1.0 / 30.0,
        'days': 1.0 / 30.0,
        'minggu': 1.0 / 4.0,
        'week': 1.0 / 4.0,
        'weeks': 1.0 / 4.0,
        'bulan': 1.0,
        'month': 1.0,
        'months': 1.0,
        'tahun': 12.0,
        'year': 12.0,
        'years': 12.0
    }
    if satuan not in konversi:
        raise ValueError(f"Satuan durasi '{satuan}' tidak valid! Pilih: 'hari', 'minggu', 'bulan', atau 'tahun'.")
    return float(nilai) * konversi[satuan]

def kategori_lama_hubungan(durasi_bulan: float) -> str:
    """Memetakan durasi hubungan ke kategori ordinal dataset."""
    if durasi_bulan < 6.0:
        return '< 6 bulan'
    elif durasi_bulan < 12.0:
        return '6 bulan - 1 tahun'
    elif durasi_bulan < 36.0:
        return '1 - 3 tahun'
    elif durasi_bulan < 60.0:
        return '3 - 5 tahun'
    else:
        return '> 5 tahun'

def kategori_sejak_putus(durasi_bulan: float) -> str:
    """Memetakan durasi sejak perpisahan ke kategori ordinal dataset."""
    if durasi_bulan < 1.0:
        return '< 1 bulan'
    elif durasi_bulan < 3.0:
        return '1 - 3 bulan'
    elif durasi_bulan < 6.0:
        return '3 - 6 bulan'
    elif durasi_bulan < 12.0:
        return '6 - 12 bulan'
    else:
        return '> 1 tahun'

def clean_column_name(col_name: str) -> str:
    """Membersihkan format nama kolom untuk One-Hot Encoding yang konsisten."""
    col_name = str(col_name).strip()
    col_name = re.sub(r'[<>]+', '', col_name)
    col_name = re.sub(r'[?.,!()/]+', '', col_name)
    col_name = re.sub(r'\s+-\s+', '_', col_name)
    col_name = re.sub(r'\s+', '_', col_name)
    col_name = re.sub(r'_+', '_', col_name)
    return col_name.strip('_')

def hitung_life_stage(umur: float) -> Tuple[float, str]:
    """Menentukan skor tahap perkembangan kognitif dan label deskripsi psikososial."""
    if umur <= 18.0:
        return 1.0, 'Remaja / Usia Sekolah (Fase Pembentukan Identitas & Emosi Intens)'
    elif umur <= 22.0:
        return 2.0, 'Dewasa Awal / Kuliah-Kerja Baru (Fase Transisi Kemandirian & Quarter-Life)'
    elif umur <= 27.0:
        return 3.0, 'Dewasa Produktif / Meniti Karir (Fase Rasionalitas & Stabilitas)'
    else:
        return 4.0, 'Dewasa Matang (Fase Regulasi Emosi Stabil & Coping Terbentuk)'

MAP_PENDIDIKAN_ORDINAL = {
    'SMP/Sederajat': 1.0,
    'SMA/Sederajat': 2.0,
    'SMA / SMK': 2.0,
    'Diploma (D1/D2/D3)': 3.0,
    'Diploma (D3)': 3.0,
    'S1': 4.0,
    'S2': 5.0,
    'S2 / S3': 5.0,
    'S3': 6.0,
    'Lainnya': 2.5
}

def transform_user_input(
    payload: PredictionInput,
    feature_names: list,
    scaler: Any,
    default_values: dict
) -> Tuple[pd.DataFrame, DurationDetail, Dict[str, Any]]:
    """
    Mengubah payload input Pydantic menjadi DataFrame siap prediksi
    lengkap dengan feature engineering kognitif V3, encoding, dan scaling.
    """
    durasi_hubungan_bulan = convert_ke_bulan(payload.lama_hubungan_nilai, payload.lama_hubungan_satuan)
    durasi_putus_bulan = convert_ke_bulan(payload.sejak_putus_nilai, payload.sejak_putus_satuan)
    
    kat_lama_hubungan = kategori_lama_hubungan(durasi_hubungan_bulan)
    kat_sejak_putus = kategori_sejak_putus(durasi_putus_bulan)
    
    # Imputasi nilai default jika field opsional None
    jk = payload.jenis_kelamin if payload.jenis_kelamin else default_values.get('Jenis Kelamin', 'Perempuan')
    pend = payload.pendidikan if payload.pendidikan else default_values.get('Pendidikan', 'S1')
    pengakhiri = payload.siapa_mengakhiri if payload.siapa_mengakhiri else default_values.get('Siapa yang Mengakhiri Hubungan?', 'Pasangan yang mengakhiri')
    komunikasi = payload.masih_komunikasi if payload.masih_komunikasi else default_values.get('Apakah Masih Berkomunikasi dengan Mantan?', 'Tidak sama sekali')
    medsos = payload.frekuensi_medsos if payload.frekuensi_medsos else default_values.get('Seberapa Sering Melihat Media Sosial Mantan?', 'Jarang')
    
    # Rekayasa Fitur Rasio & Kematangan Kognitif V3
    recovery_ratio = durasi_putus_bulan / (durasi_hubungan_bulan + 1e-5)
    log_recovery_index = float(np.log1p(durasi_putus_bulan) / np.log1p(durasi_hubungan_bulan))
    umur_mulai_hubungan = max(10.0, float(payload.umur) - (durasi_hubungan_bulan / 12.0))
    
    life_stage_score, life_stage_label = hitung_life_stage(float(payload.umur))
    tingkat_pendidikan_ord = MAP_PENDIDIKAN_ORDINAL.get(pend, 4.0)
    
    is_usia_sekolah = 1.0 if payload.umur <= 18.0 else 0.0
    is_dewasa_awal = 1.0 if (19.0 <= payload.umur <= 22.0) else 0.0
    is_dewasa_matang = 1.0 if payload.umur > 22.0 else 0.0
    
    conscious_years = max(1.0, float(payload.umur) - 12.0)
    emotional_vulnerability_index = (durasi_hubungan_bulan / 12.0) / conscious_years
    cognitive_resilience_ratio = (tingkat_pendidikan_ord * life_stage_score) / (np.log1p(durasi_putus_bulan) + 1.0)
    relational_maturity_index = (life_stage_score * 0.5 + tingkat_pendidikan_ord * 0.5) / (np.log1p(durasi_hubungan_bulan) + 1.0)
    
    # Ambang Batas Target Pemulihan Dinamis V3
    maturity_factor = 1.25 if (payload.umur >= 22.0 or pend in ['S1', 'S2', 'S3']) else 0.85
    target_ringan_bulan = max(3.0, (durasi_hubungan_bulan * 0.25) / maturity_factor)
    
    feature_dict = {feat: 0.0 for feat in feature_names}
    if 'Umur' in feature_dict: feature_dict['Umur'] = float(payload.umur)
    if 'durasi_hubungan_bulan' in feature_dict: feature_dict['durasi_hubungan_bulan'] = float(durasi_hubungan_bulan)
    if 'durasi_putus_bulan' in feature_dict: feature_dict['durasi_putus_bulan'] = float(durasi_putus_bulan)
    if 'tingkat_pendidikan_ordinal' in feature_dict: feature_dict['tingkat_pendidikan_ordinal'] = float(tingkat_pendidikan_ord)
    if 'life_stage_score' in feature_dict: feature_dict['life_stage_score'] = float(life_stage_score)
    if 'is_usia_sekolah' in feature_dict: feature_dict['is_usia_sekolah'] = float(is_usia_sekolah)
    if 'is_dewasa_awal' in feature_dict: feature_dict['is_dewasa_awal'] = float(is_dewasa_awal)
    if 'is_dewasa_matang' in feature_dict: feature_dict['is_dewasa_matang'] = float(is_dewasa_matang)
    if 'recovery_ratio' in feature_dict: feature_dict['recovery_ratio'] = float(recovery_ratio)
    if 'log_recovery_index' in feature_dict: feature_dict['log_recovery_index'] = float(log_recovery_index)
    if 'umur_mulai_hubungan' in feature_dict: feature_dict['umur_mulai_hubungan'] = float(umur_mulai_hubungan)
    if 'emotional_vulnerability_index' in feature_dict: feature_dict['emotional_vulnerability_index'] = float(emotional_vulnerability_index)
    if 'cognitive_resilience_ratio' in feature_dict: feature_dict['cognitive_resilience_ratio'] = float(cognitive_resilience_ratio)
    if 'relational_maturity_index' in feature_dict: feature_dict['relational_maturity_index'] = float(relational_maturity_index)
    
    active_pairs = [
        ('Jenis Kelamin', jk),
        ('Pendidikan', pend),
        ('Lama Hubungan Sebelum Putus', kat_lama_hubungan),
        ('Sudah Berapa Lama Sejak Putus?', kat_sejak_putus),
        ('Siapa yang Mengakhiri Hubungan?', pengakhiri),
        ('Apakah Masih Berkomunikasi dengan Mantan?', komunikasi),
        ('Seberapa Sering Melihat Media Sosial Mantan?', medsos)
    ]
    
    for col, val in active_pairs:
        clean_name = clean_column_name(f"{col}_{val}")
        if clean_name in feature_dict:
            feature_dict[clean_name] = 1.0
        else:
            for fn in feature_names:
                if clean_column_name(str(col)) in fn and clean_column_name(str(val)) in fn:
                    feature_dict[fn] = 1.0
                    break
    
    df_single = pd.DataFrame([feature_dict])[feature_names]
    df_scaled = pd.DataFrame(scaler.transform(df_single), columns=feature_names)
    
    is_fallback = any(x is None for x in [
        payload.jenis_kelamin, payload.siapa_mengakhiri,
        payload.masih_komunikasi, payload.frekuensi_medsos
    ])
    
    duration_detail = DurationDetail(
        durasi_hubungan_bulan=round(durasi_hubungan_bulan, 2),
        durasi_putus_bulan=round(durasi_putus_bulan, 2),
        kategori_lama_hubungan=kat_lama_hubungan,
        kategori_sejak_putus=kat_sejak_putus,
        rasio_pemulihan=round(recovery_ratio, 4),
        target_ringan_bulan=round(target_ringan_bulan, 1),
        life_stage_label=life_stage_label,
        fallback_opsional_digunakan=is_fallback
    )
    
    resolved_demographics = {
        'jenis_kelamin': jk,
        'pendidikan': pend,
        'siapa_mengakhiri': pengakhiri,
        'masih_komunikasi': komunikasi,
        'frekuensi_medsos': medsos,
        'life_stage_label': life_stage_label,
        'target_ringan_bulan': round(target_ringan_bulan, 1)
    }
    
    return df_scaled, duration_detail, resolved_demographics
