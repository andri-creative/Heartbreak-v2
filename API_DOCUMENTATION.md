# 📖 Heartbreak AI V3 — Dokumentasi & Integrasi REST API

REST API modern berbasis **FastAPI** untuk melayani inferensi model keparahan patah hati (*Heartbreak Severity Classifier V3*) dengan Formula Proporsional Relasional, Tahap Perkembangan Kognitif Usia & Pendidikan, serta Konseling AI Psychologist Coach.

---

## 🚀 1. Cara Menjalankan Server API

### A. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### B. Menjalankan Server
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Server akan aktif di: **`http://localhost:8000`**
Dokumentasi Interaktif (Swagger UI): **`http://localhost:8000/docs`**

---

## 📡 2. Daftar Endpoint REST API

### 1️⃣ Health Check
* **Method**: `GET`
* **URL**: `/health`
* **Response**:
```json
{
  "status": "healthy",
  "model_ready": true,
  "version": "3.0.0",
  "model_architecture": "Soft Voting Ensemble (Calibrated V3)",
  "timestamp": "2026-08-18 09:30:00"
}
```

---

### 2️⃣ Metadata Opsi Dropdown Frontend
* **Method**: `GET`
* **URL**: `/api/options`
* **Deskripsi**: Mengambil daftar opsi pilihan resmi untuk form dropdown di UI.
* **Response**:
```json
{
  "satuan_durasi_tersedia": ["hari", "minggu", "bulan", "tahun"],
  "jenis_kelamin_options": ["Laki-laki", "Perempuan"],
  "pendidikan_options": [
    "SMP/Sederajat",
    "SMA/Sederajat",
    "SMA / SMK",
    "Diploma (D1/D2/D3)",
    "Diploma (D3)",
    "S1",
    "S2",
    "S2 / S3",
    "S3"
  ],
  "siapa_mengakhiri_options": [
    "Saya yang mengakhiri",
    "Pasangan yang mengakhiri",
    "Keputusan bersama",
    "Tidak jelas"
  ],
  "masih_komunikasi_options": [
    "Tidak sama sekali",
    "Jarang",
    "Kadang-kadang",
    "Sering",
    "Setiap hari"
  ],
  "frekuensi_medsos_options": [
    "Tidak pernah",
    "Jarang",
    "Kadang-kadang",
    "Sekali sehari",
    "Hampir setiap hari",
    "Beberapa kali sehari"
  ]
}
```

---

### 3️⃣ Prediksi Keparahan Patah Hati (Main Endpoint V3)
* **Method**: `POST`
* **URL**: `/api/predict`
* **Header**: `Content-Type: application/json`

#### 📥 Request Body (JSON)
```json
{
  "nama": "Rian Pratama",
  "umur": 22,
  "pendidikan": "S1",
  "lama_hubungan_nilai": 2,
  "lama_hubungan_satuan": "tahun",
  "sejak_putus_nilai": 6,
  "sejak_putus_satuan": "bulan",
  "jenis_kelamin": "Laki-laki",
  "siapa_mengakhiri": "Pasangan yang mengakhiri",
  "masih_komunikasi": "Tidak sama sekali",
  "frekuensi_medsos": "Jarang"
}
```

#### 📤 Response Body (JSON)
```json
{
  "success": true,
  "message": "Analisis keparahan patah hati dan konsultasi kognitif AI V3 berhasil dilakukan.",
  "version": "3.0.0",
  "timestamp": "2026-08-18 09:30:00",
  "data": {
    "nama": "Rian Pratama",
    "umur": 22.0,
    "pendidikan": "S1",
    "kategori_severity": "Ringan",
    "badge": "🟢",
    "deskripsi_status": "Keparahan Patah Hati Rendah (Fase Pemulihan Adaptif / Pulih / Move On)",
    "probabilitas_ringan": 85.0,
    "probabilitas_distres": 15.0,
    "detail_durasi": {
      "durasi_hubungan_bulan": 24.0,
      "durasi_putus_bulan": 6.0,
      "kategori_lama_hubungan": "1 - 3 tahun",
      "kategori_sejak_putus": "6 - 12 bulan",
      "rasio_pemulihan": 0.25,
      "target_ringan_bulan": 4.8,
      "life_stage_label": "Dewasa Awal / Kuliah-Kerja Baru (Fase Transisi Kemandirian & Quarter-Life)",
      "fallback_opsional_digunakan": false
    },
    "profil_kognitif": "🧠 Profil Kognitif Usia 22 Tahun (S1)...",
    "rekomendasi_psikologis": [
      "Pertahankan rutinitas positif harian dan aktivitas produktif yang sedang berjalan.",
      "Fokus pada pengembangan diri, hobi baru, dan pencapaian target masa depan.",
      "Buka diri secara perlahan untuk memperluas lingkaran sosial yang sehat."
    ],
    "ai_psychologist_insight": {
      "headline_empati": "Langkah Menuju Kestabilan Baru...",
      "analisis_kondisi": "Dalam 6 bulan masa pemulihan, nalar kognitif Anda telah bekerja efektif...",
      "langkah_pemulihan_personal": [
        "Terus fokus pada target karir dan pengembangan skill mandiri.",
        "Bangun koneksi pertemanan dan ruang sosial yang bermakna."
      ],
      "afirmasi_harian": "Setiap hari membawa peluang baru untuk bertumbuh lebih kuat.",
      "peringatan_psikologis": null
    }
  }
}
```

---

## 💻 3. Contoh Integrasi di Frontend (JavaScript / React / Next.js)

```javascript
async function checkHeartbreakSeverity(formData) {
  try {
    const response = await fetch("http://localhost:8000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nama: formData.nama,
        umur: Number(formData.umur),
        pendidikan: formData.pendidikan || "S1",
        lama_hubungan_nilai: Number(formData.lamaHubunganNilai),
        lama_hubungan_satuan: formData.lamaHubunganSatuan,
        sejak_putus_nilai: Number(formData.sejakPutusNilai),
        sejak_putus_satuan: formData.sejakPutusSatuan,
        jenis_kelamin: formData.jenisKelamin || null,
        siapa_mengakhiri: formData.siapaMengakhiri || null,
        masih_komunikasi: formData.masihKomunikasi || null,
        frekuensi_medsos: formData.frekuensiMedsos || null,
      }),
    });

    const result = await response.json();
    if (result.success) {
      console.log("Status Severity V3:", result.data.kategori_severity);
      console.log("Skor Distres:", result.data.probabilitas_distres, "%");
      console.log("Target Pulih:", result.data.detail_durasi.target_ringan_bulan, "bulan");
      return result.data;
    }
  } catch (error) {
    console.error("Error koneksi API:", error);
  }
}
```
