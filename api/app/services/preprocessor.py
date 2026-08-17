"""
Modul Preprocessing & Transformer Fitur Input Pengguna
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

def transform_user_input(
    payload: PredictionInput,
    feature_names: list,
    scaler: Any,
    default_values: dict
) -> Tuple[pd.DataFrame, DurationDetail, Dict[str, Any]]:
    """
    Mengubah payload input Pydantic menjadi DataFrame siap prediksi
    lengkap dengan feature engineering, encoding, dan standard scaling.
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
    
    recovery_ratio = durasi_putus_bulan / (durasi_hubungan_bulan + 1e-5)
    log_recovery_index = float(np.log1p(durasi_putus_bulan) / np.log1p(durasi_hubungan_bulan))
    umur_mulai_hubungan = max(10.0, float(payload.umur) - (durasi_hubungan_bulan / 12.0))
    
    feature_dict = {feat: 0.0 for feat in feature_names}
    feature_dict['Umur'] = float(payload.umur)
    feature_dict['durasi_hubungan_bulan'] = float(durasi_hubungan_bulan)
    feature_dict['durasi_putus_bulan'] = float(durasi_putus_bulan)
    feature_dict['recovery_ratio'] = float(recovery_ratio)
    feature_dict['log_recovery_index'] = float(log_recovery_index)
    feature_dict['umur_mulai_hubungan'] = float(umur_mulai_hubungan)
    
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
        payload.jenis_kelamin, payload.pendidikan, payload.siapa_mengakhiri,
        payload.masih_komunikasi, payload.frekuensi_medsos
    ])
    
    duration_detail = DurationDetail(
        durasi_hubungan_bulan=round(durasi_hubungan_bulan, 2),
        durasi_putus_bulan=round(durasi_putus_bulan, 2),
        kategori_lama_hubungan=kat_lama_hubungan,
        kategori_sejak_putus=kat_sejak_putus,
        rasio_pemulihan=round(recovery_ratio, 4),
        fallback_opsional_digunakan=is_fallback
    )
    
    resolved_demographics = {
        'jenis_kelamin': jk,
        'pendidikan': pend,
        'siapa_mengakhiri': pengakhiri,
        'masih_komunikasi': komunikasi,
        'frekuensi_medsos': medsos
    }
    
    return df_scaled, duration_detail, resolved_demographics
