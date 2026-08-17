# ❤️‍🩹 Heartbreak AI V2 — Modular Backend REST API

Layanan REST API modern berbasis **FastAPI** dengan arsitektur modular yang rapi, menggabungkan:
1. **Machine Learning Classifier V2** (Ensemble Calibrated Model dengan 8 Fitur Demografis).
2. **AI Psychologist & Recovery Coach Service** (Analisis kognitif empatik, langkah pemulihan adaptif, dan afirmasi harian personal).

---

## 📂 Struktur Arsitektur Modular

```text
api/
├── app/
│   ├── __init__.py
│   ├── config.py              # Konfigurasi aplikasi & threshold klinis
│   ├── schemas.py             # Skema Pydantic Request & Response
│   │
│   ├── services/              # Business Logic & Core AI
│   │   ├── __init__.py
│   │   ├── preprocessor.py    # Transformer durasi alami (hari/minggu/bulan/tahun) & scaling
│   │   ├── ml_service.py      # Loader Model Bundle & Inferensi 3-Tier Severity
│   │   └── ai_coach_service.py# AI Psychologist & Emotional Recovery Counselor
│   │
│   └── routers/               # API Endpoints
│       ├── __init__.py
│       ├── health.py          # GET /health & GET /api/options
│       └── predict.py         # POST /api/predict & POST /api/counsel
│
├── main.py                    # Entry Point Server FastAPI
├── requirements.txt           # Dependensi Python
└── README.md                  # Dokumentasi API
```

---

## ⚡ Cara Menjalankan Server

1. Masuk ke direktori `api`:
   ```bash
   cd api
   ```
2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Buka di browser:
   * **URL API Root**: `http://localhost:8000`
   * **Swagger UI (Interactive API Docs)**: `http://localhost:8000/docs`
   * **ReDoc**: `http://localhost:8000/redoc`

---

## 📡 Daftar Endpoint API

### 1️⃣ `GET /health`
Mengecek status kesehatan server dan kesiapan model bundle.

### 2️⃣ `GET /api/options`
Mengambil daftar opsi resmi untuk form dropdown di UI Frontend:
* Satuan durasi: `["hari", "minggu", "bulan", "tahun"]`
* Jenis kelamin, Pendidikan, Siapa yang mengakhiri, Komunikasi mantan, Medsos mantan.

### 3️⃣ `POST /api/predict` (Endpoint Utama)
Menganalisis tingkat keparahan patah hati (Ringan / Sedang / Berat) sekaligus menghasilkan analisis AI Psychologist personal.

#### 📥 Contoh Request Body (JSON):
```json
{
  "nama": "Dimas Anggara",
  "umur": 22,
  "lama_hubungan_nilai": 4,
  "lama_hubungan_satuan": "tahun",
  "sejak_putus_nilai": 2,
  "sejak_putus_satuan": "minggu",
  "jenis_kelamin": "Laki-laki",
  "pendidikan": "S1",
  "siapa_mengakhiri": "Pasangan yang mengakhiri",
  "masih_komunikasi": "Kadang-kadang",
  "frekuensi_medsos": "Sering"
}
```

> **Field Opsional**: `jenis_kelamin`, `pendidikan`, `siapa_mengakhiri`, `masih_komunikasi`, `frekuensi_medsos` bisa bernilai `null` jika tidak diisi user.

#### 📤 Contoh Response Body (JSON):
```json
{
  "success": true,
  "message": "Analisis tingkat keparahan patah hati dan konsultasi AI berhasil dilakukan.",
  "timestamp": "2026-08-17 20:50:00",
  "data": {
    "nama": "Dimas Anggara",
    "umur": 22.0,
    "kategori_severity": "Berat",
    "badge": "🔴",
    "deskripsi_status": "Keparahan Patah Hati Tinggi / Akut (Distres Emosional Intensif)",
    "probabilitas_ringan": 11.5,
    "probabilitas_distres": 88.5,
    "detail_durasi": {
      "durasi_hubungan_bulan": 48.0,
      "durasi_putus_bulan": 0.5,
      "kategori_lama_hubungan": "3 - 5 tahun",
      "kategori_sejak_putus": "< 1 bulan",
      "rasio_pemulihan": 0.0104,
      "fallback_opsional_digunakan": false
    },
    "rekomendasi_psikologis": [
      "Prioritas Utama: Sangat dianjurkan berkonsultasi dengan psikolog atau konselor profesional untuk pendampingan reguler.",
      "Terapkan STRICT NO-CONTACT: Blokir/mute semua akses media sosial mantan untuk memutus siklus distres.",
      "Jangan menahan beban sendirian; libatkan keluarga atau support system terdekat yang aman dan suportif.",
      "Jaga kebutuhan fisik esensial: istirahat cukup, hindari isolasi diri berkepanjangan, dan tunda keputusan hidup yang besar."
    ],
    "ai_psychologist_insight": {
      "headline_empati": "Hai Dimas Anggara, Tarik Napas Dalam-Dalam. Luka Ini Sangat Valid, dan Kamu Tidak Sendirian.",
      "analisis_kondisi": "Berdasarkan analisis AI, perpisahan setelah 4.0 tahun bersama dan baru berjarak 2.0 minggu menempatkan sistem saraf emosionalmu pada fase 'Acute Attachment Withdrawal'...",
      "langkah_pemulihan_personal": [
        "🛑 Terapkan Strict No-Contact...",
        "🧠 Grounding & Emotional Release...",
        "👥 Aktifkan Emergency Support System...",
        "🩺 Konsultasi Pendampingan..."
      ],
      "afirmasi_harian": "\"Rasa sakit ini adalah bukti bahwa aku pernah mencintai dengan tulus. Hari ini terasa berat, tapi aku berhak sembuh dan bangkit perlahan.\"",
      "peringatan_psikologis": "⚠️ Peringatan: Hindari membuat keputusan impulsif atau mencoba melampiaskan kesedihan ke pelarian negatif saat emosi belum stabil."
    }
  }
}
```

---

### 4️⃣ `POST /api/counsel` (Konseling Interaktif Lanjutan)
Endpoint untuk sesi curhat interaktif di mana pengguna dapat mengirimkan pesan teks bebas / pertanyaan emosional ke AI Psychologist Coach.

---

## 💻 Integrasi Frontend (JavaScript / React / Next.js)

```javascript
export async function getHeartbreakDiagnosis(userInput) {
  const response = await fetch("http://localhost:8000/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nama: userInput.nama,
      umur: Number(userInput.umur),
      lama_hubungan_nilai: Number(userInput.lamaHubunganNilai),
      lama_hubungan_satuan: userInput.lamaHubunganSatuan,
      sejak_putus_nilai: Number(userInput.sejakPutusNilai),
      sejak_putus_satuan: userInput.sejakPutusSatuan,
      jenis_kelamin: userInput.jenisKelamin || null,
      pendidikan: userInput.pendidikan || null,
      siapa_mengakhiri: userInput.siapaMengakhiri || null,
      masih_komunikasi: userInput.masihKomunikasi || null,
      frekuensi_medsos: userInput.frekuensiMedsos || null,
    }),
  });

  const result = await response.json();
  if (result.success) {
    const data = result.data;
    console.log("Severity:", data.kategori_severity); // "Ringan" | "Sedang" | "Berat"
    console.log("AI Insight:", data.ai_psychologist_insight.headline_empati);
    console.log("Afirmasi:", data.ai_psychologist_insight.afirmasi_harian);
    return data;
  }
}
```
