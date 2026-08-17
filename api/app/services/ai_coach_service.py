"""
AI Emotional Coach & Heartbreak Psychologist Service
Mengintegrasikan Google GenAI SDK & Direct Zero-Dependency HTTP Transport.
"""

import json
import re
import ssl
import os
import urllib.request
import urllib.error
import requests
from typing import Optional, Dict, Any, List
from app.schemas import PredictionInput, AICounselResponseData
from app.config import settings

# SSL Context bypass untuk kompatibilitas macOS Python
SSL_CONTEXT = ssl._create_unverified_context()

class AICoachService:
    """Service untuk menghasilkan insight psikologis AI berbasis OpenRouter (OpenAI GPT)."""
    
    @classmethod
    def generate_ai_insight(
        cls,
        payload: PredictionInput,
        kategori_severity: str,
        prob_distres: float,
        resolved_demographics: Dict[str, Any],
        user_curhat: Optional[str] = None
    ) -> AICounselResponseData:
        """
        Menghasilkan narasi psikologis komprehensif:
        1. Memanggil OpenRouter API (OpenAI GPT & Model Lain).
        2. Jika offline / limit -> Menggunakan Multi-Domain Contextual Intelligence Engine.
        """
        openrouter_key = getattr(settings, "OPENROUTER_API_KEY", "") or os.getenv("OPENROUTER_API_KEY", "")

        # print("\n" + "="*70)
        # print("🧠 [AI COACH] MEMPROSES KONSULTASI PSIKOLOGIS DENGAN OPENAI (OPENROUTER)")
        # print(f"👤 Responden: {payload.nama} ({int(payload.umur)} tahun) | Status: {kategori_severity} ({prob_distres}%)")
        # print(f"💬 Pertanyaan / Curhat: \"{user_curhat if user_curhat else 'Diagnosis Standar'}\"")
        # print("="*70)

        # 1. Prioritas Utama: OpenRouter (OpenAI GPT)
        if openrouter_key:
            llm_res = cls._try_openrouter_api(openrouter_key, payload, kategori_severity, prob_distres, user_curhat)
            if llm_res:
                # print("✅ [OpenRouter OpenAI GPT] Sukses menerima respon!")
                return llm_res

        # 2. Fallback: Contextual Intelligence Engine
        # print("ℹ️ [Fallback] Menggunakan Multi-Domain Contextual Intelligence Engine...")
        return cls._generate_contextual_counseling_response(payload, kategori_severity, prob_distres, user_curhat)

    @classmethod
    def _try_openrouter_api(
        cls,
        api_key: str,
        payload: PredictionInput,
        kategori_severity: str,
        prob_distres: float,
        user_curhat: Optional[str] = None
    ) -> Optional[AICounselResponseData]:
        """Memanggil OpenRouter API (OpenAI GPT & Model Lain)."""
        prompt = (
            f"Kamu adalah Pakar Psikologi Hubungan & Mental Health Coach AI (Heartbreak AI Coach).\n"
            f"Pasien: {payload.nama} ({int(payload.umur)} tahun), Pacaran {payload.lama_hubungan_nilai} {payload.lama_hubungan_satuan}, Putus {payload.sejak_putus_nilai} {payload.sejak_putus_satuan}.\n"
            f"Tingkat Keparahan: {kategori_severity} (Distres: {prob_distres}%).\n"
            f"PERTANYAAN / CURHAT PASIEN: \"{user_curhat if user_curhat else 'Diagnosis Standar'}\"\n\n"
            f"Jawab pertanyaan curhat di atas secara langsung, empatik, bijak, dan mendalam. Format output HANYA JSON persis tanpa markdown lain:\n"
            f"{{\n"
            f'  "headline_empati": "...",\n'
            f'  "analisis_kondisi": "...",\n'
            f'  "langkah_pemulihan_personal": ["...", "...", "...", "..."],\n'
            f'  "afirmasi_harian": "...",\n'
            f'  "peringatan_psikologis": null\n'
            f"}}"
        )

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "Heartbreak AI Coach"
        }

        # Model urutan OpenRouter (Default GPT)
        models_to_try = [
            "openai/gpt-4o-mini",
            "openai/gpt-5",
            "qwen/qwen3-coder-next",
            "openrouter/free"
        ]

        for model_name in models_to_try:
            try:
                # print(f"🔄 [OpenRouter] Mencoba model: {model_name}...")
                body = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1200,
                    "temperature": 0.7
                }
                response = requests.post(url, headers=headers, json=body, timeout=30)
                if response.status_code == 200:
                    res_json = response.json()
                    text_out = res_json.get("choices", [{}])[0].get("message", {}).get("content", "")
                    if text_out:
                        cleaned = re.sub(r'^```json\s*|\s*```$', '', text_out.strip(), flags=re.MULTILINE)
                        parsed = json.loads(cleaned)
                        return AICounselResponseData(
                            headline_empati=parsed.get("headline_empati", f"Hai {payload.nama}, kami mendengarmu."),
                            analisis_kondisi=parsed.get("analisis_kondisi", ""),
                            langkah_pemulihan_personal=parsed.get("langkah_pemulihan_personal", []),
                            afirmasi_harian=parsed.get("afirmasi_harian", ""),
                            peringatan_psikologis=parsed.get("peringatan_psikologis")
                        )
                else:
                    # print(f"⚠️ [OpenRouter {model_name}]: Status {response.status_code} - {response.text[:120]}")
                    pass
            except Exception as e:
                # print(f"⚠️ [OpenRouter Error {model_name}]: {e}")
                pass

        return None

    @classmethod
    def _generate_contextual_counseling_response(
        cls,
        payload: PredictionInput,
        kategori_severity: str,
        prob_distres: float,
        user_curhat: Optional[str] = None
    ) -> AICounselResponseData:
        """Multi-Domain Contextual Intelligence Engine bawaan."""
        nama = payload.nama
        lh = f"{payload.lama_hubungan_nilai} {payload.lama_hubungan_satuan}"
        lp = f"{payload.sejak_putus_nilai} {payload.sejak_putus_satuan}"
        q = (user_curhat or "").lower().strip()

        if any(w in q for w in ["hiburan", "liburan", "healing", "wisata", "jalan-jalan", "refreshing", "tempat main", "rekomendasi tempat", "jawa tengah", "jateng"]):
            headline = f"Rekomendasi Healing & Hiburan Terbaik di Jawa Tengah untuk {nama}"
            analisis = (
                f"Mencari suasana baru setelah perpisahan hubungan {lh} adalah langkah tepat untuk meregenerasi hormon dopamin alami dan meredakan kejenuhan mental.<br><br>"
                f"Berikut adalah destinasi hiburan & *nature healing* terbaik di <strong>Jawa Tengah</strong> yang sangat efektif membantu pemulihan emosionalmu:<br><br>"
                f"1. 🌲 <strong>Kawasan Dataran Tinggi Dieng (Wonosobo / Banjarnegara):</strong> Suasana sejuk Telaga Warna, Kawah Sikidang, dan matahari terbit di Bukit Sikunir.<br>"
                f"2. 🏰 <strong>Kota Budaya Solo & Tawangmangu (Karanganyar):</strong> Air Terjun Grojogan Sewu dan kafe lereng Gunung Lawu.<br>"
                f"3. 🌊 <strong>Kepulauan Karimunjawa (Jepara):</strong> Pantai pasir putih dan ketenangan laut tropis untuk *solo-trip*.<br>"
                f"4. 🌿 <strong>Kebun Teh Kemuning (Karanganyar) & Candi Gedong Songo (Bandungan):</strong> Lanskap hijau terbuka."
            )
            langkah = [
                "🎒 Ambil Liburan Singkat 2-3 Hari ke Dataran Tinggi Dieng atau Tawangmangu.",
                "📵 Terapkan Mini Digital Detox Saat Menikmati Pemandangan Alam.",
                "📸 Abadikan Momen Bahagia Baru Secara Mandiri.",
                "🍲 Cicipi Kuliner Khas Lokal Seperti Mie Ongklok Wonosobo atau Timlo Solo."
            ]
            afirmasi = f"\"Dunia ini luas dan indah. Aku berhak menikmati kebahagiaan dan menjelajahi tempat-tempat baru dengan sukacita.\""
            warning = None

        elif any(w in q for w in ["hiburan", "liburan", "healing", "wisata", "jalan-jalan", "refreshing", "jawa timur", "jatim", "malang", "batu", "bromo"]):
            headline = f"Rekomendasi Healing & Hiburan Terbaik di Jawa Timur untuk {nama}"
            analisis = (
                f"Berikut adalah destinasi hiburan & *nature healing* terbaik di <strong>Jawa Timur</strong> untuk {nama}:<br><br>"
                f"1. 🌲 <strong>Kota Wisata Batu & Malang:</strong> Udaranya sejuk pegunungan (*Selecta, Coban Rondo, Cafe Sawah Pujon*).<br>"
                f"2. 🌋 <strong>Kawasan Bromo:</strong> Menyaksikan matahari terbit lautan pasir Bromo.<br>"
                f"3. 🌊 <strong>Pantai Malang Selatan (Teluk Asmara, Balekambang):</strong> Suara ombak pantai (*blue space*) merilekskan saraf.<br>"
                f"4. 🌿 <strong>Banyuwangi (Kawah Ijen & TN Baluran):</strong> Suasana savana alam terbuka."
            )
            langkah = [
                "🎒 Ambil Liburan Singkat 2-3 Hari ke Kota Batu atau Bromo.",
                "📵 Hindari Membuka Chat Masa Lalu Selama Berlibur.",
                "🍲 Nikmati Kuliner Khas Bakso Malang & Pos Ketan Legenda Batu."
            ]
            afirmasi = f"\"Aku mengizinkan diriku untuk bersenang-senang dan menikmati hidup baru.\""
            warning = None

        elif any(w in q for w in ["balikan", "clbk", "kembali", "ngajak balikan", "tidak mau", "dia nolak", "dia gak mau", "gimana"]):
            headline = f"Hai {nama}, Menghadapi Penolakan Balikan Memang Menyakitkan, Tapi Ini Kunci Menjaga Harga Dirimu."
            analisis = (
                f"Jawaban langsung untuk dilemamu: <strong>Ketika kamu ingin balikan namun pihak pasangan secara tegas menyatakan tidak mau, langkah terbaik yang harus kamu ambil adalah BERHENTI MENGEJAR DAN MENERIMA KEPUTUSANNYA DENGAN TEGAK.</strong><br><br>"
                f"Secara psikologis, cinta dan komitmen membutuhkan persetujuan dua arah (*mutual consent*). "
                f"Setelah hubungan selama {lh} dan perpisahan sudah berjalan {lp}, memaksakan atau memohon balikan hanya akan merusak *self-worth* (harga diri) dan daya tarikmu di matanya.<br><br>"
                f"Hargai dirimu sendiri dengan tidak mengemis cinta yang sudah tidak lagi untukku."
            )
            langkah = [
                "🛑 Hentikan Segala Permohonan: Jangan lagi mengirim pesan memohon atau bertanya alasan perpisahan berulang kali.",
                "🚪 Terapkan Radical Acceptance: Menerima kenyataan adalah langkah awal untuk kembali dihormati.",
                "🛡️ Tarik Diri Sepenuhnya (Full No-Contact): Putus semua kontak untuk menyembuhkan luka penolakan.",
                "👑 Reclaim Your Power: Fokuskan energimu ke peningkatan kualitas diri, karier, dan kebahagiaan pribadimu."
            ]
            afirmasi = f"\"Aku layak dicintai oleh seseorang yang memilihku tanpa ragu. Aku tidak perlu mengemis cinta yang sudah tidak lagi untukku.\""
            warning = "⚠️ Peringatan Keras: Jangan pernah merendahkan martabatmu demi meminta seseorang kembali."

        else:
            curhat_display = user_curhat if user_curhat else "analisis pemulihan emosi"
            headline = f"Panduan Psikologis untuk {nama}: Menanggapi Pertanyaan Ini"
            analisis = (
                f"Mengenai apa yang kamu sampaikan: <em>\"{curhat_display}\"</em>,<br><br>"
                f"Setelah melalui hubungan selama {lh} dan kini berjarak {lp}, adalah hal yang sangat manusiawi jika kamu mencari arahan atau jawaban terbaik. "
                f"Prinsip utama yang perlu kamu pegang adalah: <strong>Fokuskan 100% energimu pada hal-hal yang dapat kamu kendalikan</strong> (kesehatan mentalmu, tindakan harianmu, dan batas toleransimu), "
                f"serta lepaskan hal-hal di luar kuasamu."
            )
            langkah = [
                "🎯 Tetapkan Batasan Diri yang Tegas: Hindari situasi yang memicu kecemasan berulang.",
                "📝 Tuliskan Isi Pikiranmu di Jurnal: Mengeluarkan uneg-uneg secara tertulis membantu meredakan ketegangan otak.",
                "🌱 Berikan Waktu Bagi Proses Healing: Pemulihan emosi adalah proses bertahap, rawat dirimu dengan sabar."
            ]
            afirmasi = f"\"Aku fokus merawat diriku hari ini, dan percaya bahwa setiap langkah membawaku pada kedamaian hati.\""
            warning = None

        return AICounselResponseData(
            headline_empati=headline,
            analisis_kondisi=analisis,
            langkah_pemulihan_personal=langkah,
            afirmasi_harian=afirmasi,
            peringatan_psikologis=warning
        )
