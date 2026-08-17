# 📖 Heartbreak AI V2 — Dokumentasi & Integrasi REST API

REST API modern berbasis **FastAPI** untuk melayani inferensi model keparahan patah hati (*Heartbreak Severity Classifier V2*) ke berbagai antarmuka Frontend (React, Vue, Next.js, Flutter, Android/iOS, atau HTML/JS murni).

---

## 🚀 1. Cara Menjalankan Server API

### A. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### B. Menjalankan Server
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
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
  "model_loaded": true,
  "model_version": "2.0.0",
  "model_architecture": "Soft Voting Ensemble (Calibrated)"
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
  "pendidikan_options": ["SMA / SMK", "Diploma (D3)", "S1", "S2 / S3"],
  "siapa_mengakhiri_options": [
    "Saya yang mengakhiri",
    "Pasangan yang mengakhiri",
    "Keputusan bersama"
  ],
  "masih_komunikasi_options": ["Tidak sama sekali", "Jarang", "Kadang-kadang", "Sering"],
  "frekuensi_medsos_options": ["Tidak pernah", "Jarang", "Kadang-kadang", "Sering"]
}
```

---

### 3️⃣ Prediksi Keparahan Patah Hati (Main Endpoint)
* **Method**: `POST`
* **URL**: `/api/predict`
* **Header**: `Content-Type: application/json`

#### 📥 Request Body (JSON)
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

> [!TIP]
> **Field Opsional**: `jenis_kelamin`, `pendidikan`, `siapa_mengakhiri`, `masih_komunikasi`, dan `frekuensi_medsos` bisa dikirim sebagai `null` jika pengguna tidak mengisinya. Sistem otomatis menggunakan nilai fallback default.

#### 📤 Response Body (JSON)
```json
{
  "success": true,
  "message": "Analisis tingkat keparahan patah hati berhasil dilakukan.",
  "timestamp": "2026-08-17 20:45:00",
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
    ]
  }
}
```

---

## 💻 3. Contoh Integrasi di Frontend (JavaScript / React / Next.js)

```javascript
// Contoh fungsi pemanggilan API dari Frontend
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
        lama_hubungan_nilai: Number(formData.lamaHubunganNilai),
        lama_hubungan_satuan: formData.lamaHubunganSatuan, // "hari" | "minggu" | "bulan" | "tahun"
        sejak_putus_nilai: Number(formData.sejakPutusNilai),
        sejak_putus_satuan: formData.sejakPutusSatuan,
        jenis_kelamin: formData.jenisKelamin || null,
        pendidikan: formData.pendidikan || null,
        siapa_mengakhiri: formData.siapaMengakhiri || null,
        masih_komunikasi: formData.masihKomunikasi || null,
        frekuensi_medsos: formData.frekuensiMedsos || null,
      }),
    });

    const result = await response.json();
    if (result.success) {
      console.log("Status Keparahan:", result.data.kategori_severity); // "Ringan" | "Sedang" | "Berat"
      console.log("Skor Distres:", result.data.probabilitas_distres, "%");
      console.log("Rekomendasi:", result.data.rekomendasi_psikologis);
      return result.data;
    } else {
      console.error("Gagal menganalisis:", result.detail);
    }
  } catch (error) {
    console.error("Error koneksi API:", error);
  }
}
```
