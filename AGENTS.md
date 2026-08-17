# AGENTS.md — Heartbreak AI V2 Master Documentation & Guidelines

## 📌 Aturan Kerja (Core Rules)
1. **Mode Perencanaan (Plan Before Build)**: Selalu gunakan mode perencanaan/konfirmasi rencana terlebih dahulu sebelum mengeksekusi perubahan besar atau membuat file baru.
2. **Pemberian Kode Bertahap (Step-by-Step Delivery)**: 
   - Berikan kode per tahap/cell secara terstruktur sehingga user dapat menjalankan dan memvalidasi setiap tahapan di Google Colab.
   - Jangan langsung menumpuk semua kode sekaligus tanpa penjelasan dan pemisahan cell yang jelas.
3. **Data Safety**:
   - Selalu gunakan penamaan versi `_v2` (`heartbreak_v2.ipynb`, `heartbreak_demographic_bundle_v2.pkl`, `test_model_v2.ipynb`).
   - Jangan menimpa (overwrite) file versi lama.
4. **Input Format (Inference / Testing)**:
   - Input durasi user dibuat fleksibel dan natural: angka + satuan (`hari`, `minggu`, `bulan`, `tahun`).
   - Tidak memaksa user memasukkan simbol `<` atau `>`.
   - Wajib: Umur, Lama Hubungan, Lama Sejak Putus. Opsional: Gender, Pendidikan, dll.
5. **Pelacakan Kemajuan (Progress Checklist)**:
   - Setiap kali memberikan kode atau menyelesaikan suatu tahapan, **selalu sertakan checklist status tahapan** (tahap mana yang sudah selesai `[x]`, tahap yang sedang dikerjakan `[ ]`, dan tahap selanjutnya) agar alur kerja terpantau dengan jelas.

---

## 🔁 Heartbreak AI V2 — Ringkasan Proyek
- **Tujuan**: Melatih ulang model klasifikasi keparahan patah hati (Heartbreak Severity) menggunakan **8 fitur demografis saja** mengikuti pipeline ML lengkap.
- **Target Akurasi**: ≥ 80%
- **Input Wajib Pengguna**:
  1. Umur (tahun)
  2. Lama Hubungan (angka + satuan: hari/minggu/bulan/tahun)
  3. Lama Sejak Putus (angka + satuan: hari/minggu/bulan/tahun)
- **Input Opsional Pengguna**: Jenis Kelamin, Pendidikan, Siapa Mengakhiri, Komunikasi Mantan, Medsos Mantan.

---

## 🗺️ Master Pipeline (From Dataset to Heartbreak AI)

```
RAW DATASET (data.xlsx)
     │
     ▼
DATA UNDERSTANDING
     │
     ▼
DATA QUALITY CHECK
     │
     ├── Missing Values
     ├── Duplicate
     └── Invalid Values
     │
     ▼
DATA CLEANING
     │
     ▼
OUTLIER DETECTION
     │
     ▼
DATA CONSISTENCY
     │
     ▼
QUESTIONNAIRE VALIDITY
     │
     ▼
QUESTIONNAIRE RELIABILITY
     │
     ▼
EDA (Exploratory Data Analysis)
     │
     ▼
DESCRIPTIVE STATISTICS
     │
     ▼
HEARTBREAK SCORE CONSTRUCTION
     │
     ▼
SEVERITY LABEL CONSTRUCTION
     │
     ├── RINGAN (0)
     ├── SEDANG (1)
     └── BERAT  (2)
     │
     ▼
MODELING DATASET (8 Demografis Saja)
     │
     ▼
FEATURE ENGINEERING
     │
     ▼
ENCODING
     │
     ▼
FEATURE SELECTION
     │
     ▼
TRAIN / VAL / TEST SPLIT (70 / 15 / 15)
     │
     ▼
PREPROCESSING (StandardScaler)
     │
     ▼
CLASS IMBALANCE (Class Weight / SMOTE Evaluation)
     │
     ▼
CROSS VALIDATION (Stratified 10-Fold)
     │
     ▼
BASELINE MODEL (Dummy & Logistic Regression)
     │
     ▼
MODEL TRAINING (8 Models)
  1. XGBoost
  2. LightGBM
  3. CatBoost
  4. Neural Network (MLP)
  5. Random Forest
  6. Gradient Boosting
  7. SVM
  8. AdaBoost
     │
     ▼
HYPERPARAMETER TUNING (RandomizedSearchCV)
     │
     ▼
MODEL COMPARISON & RANKING
     │
     ▼
FEATURE IMPORTANCE / SHAP VALUES
     │
     ▼
FINAL MODEL & ENSEMBLE (Soft Voting)
     │
     ▼
FINAL EVALUATION (Test Set Metrics, ROC-AUC, CM)
     │
     ▼
ERROR ANALYSIS
     │
     ▼
PROBABILITY CALIBRATION
     │
     ▼
SAVE MODEL BUNDLE (heartbreak_demographic_bundle_v2.pkl)
     │
     ▼
API PREPARATION
     │
     ▼
WEB / APP INTERFACE
     │
     ▼
HEARTBREAK AI ❤️‍🩹
```

---

## 📖 Detail Tahapan di Notebook `heartbreak_v2.ipynb`

### 📦 STEP 0 — Setup & Install Dependencies
- Menginstall pustaka yang dibutuhkan di Google Colab:
  `xgboost`, `lightgbm`, `catboost`, `scikit-learn`, `imbalanced-learn`, `openpyxl`, `pingouin`, `shap`, `matplotlib`, `seaborn`.

### 📥 STEP 1 — Load Data (RAW DATASET)
- Membaca file `data.xlsx` dari Google Drive.
- Memeriksa dimensi dataset (5052 baris, 49 kolom) dan tipe data setiap kolom.

### 🔍 STEP 2 — Data Understanding
- Menampilkan 5 baris pertama, struktur kolom, serta ringkasan informasi dataset.
- Mengidentifikasi 8 fitur demografis dan 40 item kuesioner psikometri.

### ✅ STEP 3 — Data Quality Check
- Pengecekan Missing Values (persentase data kosong per kolom).
- Pengecekan Duplicate Rows (duplikasi data responden).
- Pengecekan Invalid Values (nilai di luar skala 1–5 pada kolom kuesioner).

### 🧹 STEP 4 — Data Cleaning
- Menghapus baris duplikat jika ditemukan.
- Melakukan imputasi/penanganan nilai yang hilang.
- Melakukan stripping whitespace dan standardisasi penulisan teks pada kolom kategorik.

### 📦 STEP 5 — Outlier Detection & Handling
- Pengecekan outlier pada kolom numerik (`Umur`) menggunakan visualisasi Boxplot, Z-Score, dan metode IQR.
- Pengecekan batas rentang nilai kuesioner psikometri.

### 🔁 STEP 6 — Data Consistency Check
- Validasi keseragaman nilai kategorik (misalnya variasi ejaan jenis kelamin, pendidikan, dsb).
- Menyamakan format string agar seragam sebelum proses encoding.

### 📐 STEP 7 — Questionnaire Validity
- Uji validitas isi dan konstruk pada 7 dimensi kuesioner (Dimensi B, C, D, E, F, G, H).
- Analisis korelasi antar-item kuesioner dalam satu dimensi.

### 🔬 STEP 8 — Questionnaire Reliability
- Pengujian reliabilitas menggunakan **Cronbach's Alpha** per dimensi.
- Standar reliabilitas: $\alpha \ge 0.70$ dinyatakan reliabel.

### 📊 STEP 9 — EDA (Exploratory Data Analysis)
- Visualisasi distribusi umur (Histogram & KDE).
- Visualisasi frekuensi fitur demografis (Bar Chart).
- Cross-tabulation antara fitur demografis terhadap tingkat keparahan patah hati.

### 📈 STEP 10 — Descriptive Statistics
- Perhitungan Mean, Median, Standar Deviasi, Min, Max untuk data numerik.
- Tabel sebaran frekuensi dan persentase untuk data kategorik.

### 🧮 STEP 11 — Heartbreak Score Construction
- Menghitung rata-rata sub-score per dimensi dari 40 item kuesioner:
  - `score_B`: Ruminasi & Kesedihan Emosional (6 item)
  - `score_C`: Keterikatan Emosional (6 item)
  - `score_D`: Ruminasi Penyebab (6 item)
  - `score_E`: Dampak Fungsional & Fisik (6 item)
  - `score_F`: Penerimaan Hubungan (6 item)
  - `score_G`: Harapan Kembali (5 item)
  - `score_H`: Resiliensi & Coping Positif (5 item)
- Melakukan Reverse Scoring pada dimensi positif: `score_F_rev = 6 - score_F`, `score_H_rev = 6 - score_H`.
- Menghitung formula Heartbreak Severity Score (HSS):
  $$\text{HSS} = \frac{\text{score\_B} + \text{score\_C} + \text{score\_D} + \text{score\_E} + \text{score\_G} - \text{score\_F\_rev} - \text{score\_H\_rev}}{5}$$

### 🏷️ STEP 12 — Severity Label Construction
- Mengonversi nilai numerik HSS menjadi 3 kelas target:
  - **Ringan (0)**: $\text{HSS} \le 2.33$
  - **Sedang (1)**: $2.33 < \text{HSS} \le 3.66$
  - **Berat (2)**: $\text{HSS} > 3.66$
- Visualisasi sebaran proporsi kelas (Pie Chart & Bar Chart).

### 🗂️ STEP 13 — Modeling Dataset Extraction
- Memisahkan fitur masukan $X$ (hanya menggunakan 8 fitur demografis):
  1. `Umur` (Wajib)
  2. `Lama Hubungan Sebelum Putus` (Wajib)
  3. `Sudah Berapa Lama Sejak Putus?` (Wajib)
  4. `Jenis Kelamin` (Opsional)
  5. `Pendidikan` (Opsional)
  6. `Siapa yang Mengakhiri Hubungan?` (Opsional)
  7. `Apakah Masih Berkomunikasi dengan Mantan?` (Opsional)
  8. `Seberapa Sering Melihat Media Sosial Mantan?` (Opsional)
- Target $y$: `Kategori_HSS` (0, 1, 2).

### ⚙️ STEP 14 — Feature Engineering
- Membuat fitur numerik turunan dari durasi:
  - `lama_hubungan_bulan` (konversi ordinal ke satuan bulan)
  - `sejak_putus_bulan` (konversi ordinal ke satuan bulan)
  - `urgency_ratio` ($\text{sejak\_putus\_bulan} / \text{lama\_hubungan\_bulan}$)
- Evaluasi pengaruh fitur baru terhadap target klasifikasi.

### 🔢 STEP 15 — Encoding
- Menggunakan One-Hot Encoding pada fitur-fitur kategorik.
- Menghapus karakter khusus seperti `<`, `>`, spasi berlebih pada penamaan kolom untuk konsistensi inferensi.
- Menyimpan pemetaan daftar fitur (`feature_names`).

### 🎯 STEP 16 — Feature Selection
- Uji signifikansi statistik fitur terhadap target:
  - **Chi-Square Test** (fitur kategorik)
  - **ANOVA F-Test** (fitur numerik)
  - **Mutual Information** & **Cramér's V**
  - **RFE (Recursive Feature Elimination)**
- Menentukan himpunan fitur akhir yang optimal.

### ✂️ STEP 17 — Train / Val / Test Split
- Membagi dataset menjadi 3 bagian tersubset:
  - **Train Set**: 70% (data pelatihan model)
  - **Validation Set**: 15% (data penyesuaian hyperparameter)
  - **Test Set**: 15% (data evaluasi akhir yang tidak pernah dilihat model)
- Menggunakan `stratify=y` dan `random_state=42`.

### ⚖️ STEP 18 — Preprocessing
- Menggunakan `StandardScaler` untuk normalisasi skala fitur numerik.
- `StandardScaler` hanya di-`fit` pada Train Set, lalu di-`transform` pada Validation Set dan Test Set.

### ⚖️ STEP 19 — Class Imbalance Handling
- Evaluasi distribusi kelas pada data latih.
- Penanganan jika ada ketidakseimbangan kelas menggunakan `class_weight='balanced'` atau evaluasi `SMOTE`.

### 🔄 STEP 20 — Cross Validation
- Evaluasi performa model menggunakan **Stratified 10-Fold Cross Validation**.
- Pengecekan kestabilan skor akurasi dan F1-Score antar fold.

### 📏 STEP 21 — Baseline Model
- Membuat model pembanding dasar:
  - **Dummy Classifier** (Majority / Stratified baseline)
  - **Logistic Regression** (Linear baseline)
- Menjadi tolok ukur minimum yang harus dilampaui model utama.

### 🤖 STEP 22 — Model Training (8 Models)
- Melatih 8 arsitektur algoritma klasifikasi:
  1. **XGBoost Classifier**
  2. **LightGBM Classifier**
  3. **CatBoost Classifier**
  4. **Neural Network (MLP / Multi-Layer Perceptron)**
  5. **Random Forest Classifier**
  6. **Gradient Boosting Classifier**
  7. **Support Vector Machine (SVM)**
  8. **AdaBoost Classifier**

### 🔧 STEP 23 — Hyperparameter Tuning
- Optimasi parameter terbaik per model menggunakan `RandomizedSearchCV` (100 iterasi) dengan skor evaluasi pada validation set.

### 📊 STEP 24 — Model Comparison & Ranking
- Tabel perbandingan performa 8 model (Train Acc, Val Acc, Test Acc, CV Mean ± Std, F1-Macro).
- Visualisasi grafik ranking akurasi.

### 🔎 STEP 25 — Feature Importance & SHAP Analysis
- Analisis kontribusi fitur menggunakan Tree Feature Importance dan **SHAP (SHapley Additive exPlanations)**.
- SHAP Summary Plot & SHAP Waterfall Plot.

### 🏆 STEP 26 — Final Model & Soft Voting Ensemble
- Memilih model mandiri terbaik.
- Menggabungkan Top-3 model ke dalam **Soft Voting Classifier Ensemble**.
- Membandingkan hasil model terbaik vs ensemble untuk memilih model final.

### 📋 STEP 27 — Final Evaluation
- Pengujian akhir pada Test Set:
  - Confusion Matrix Heatmap
  - Classification Report (Precision, Recall, F1 per kelas)
  - ROC-AUC Curve (One-vs-Rest)

### 🧯 STEP 28 — Error Analysis
- Menganalisis sampel-sampel yang diprediksi salah untuk memahami batasan model.

### 📐 STEP 29 — Probability Calibration
- Kalibrasi probabilitas menggunakan CalibratedClassifierCV (Platt Scaling / Isotonic).
- Pengecekan Reliability Diagram dan Brier Score.

### 💾 STEP 30 — Save Model Bundle
- Mengekspor seluruh komponen ke dalam satu file bundle: `heartbreak_demographic_bundle_v2.pkl`.
  - Objek model final yang sudah terkalibrasi
  - Objek scaler
  - Label decoder (`{0: 'Ringan', 1: 'Sedang', 2: 'Berat'}`)
  - Daftar `feature_names`
  - Nilai `default_values` untuk field opsional
  - Metadata versi dan metrik akurasi

---

## 🧪 Detail Format Pengujian di `test_model_v2.ipynb`

### 1. Format Input User (Natural: Angka + Satuan)
Pengguna tidak perlu memasukkan simbol `<` atau `>`:

```python
# --- INPUT WAJIB ---
nama                 = "Budi Santoso"
umur                 = 22            # tahun

# Durasi Hubungan (bebas pilih satuan: 'hari' / 'minggu' / 'bulan' / 'tahun')
lama_hubungan_nilai  = 6
lama_hubungan_satuan = 'tahun'

# Durasi Sejak Putus (bebas pilih satuan: 'hari' / 'minggu' / 'bulan' / 'tahun')
sejak_putus_nilai    = 2
sejak_putus_satuan   = 'minggu'

# --- INPUT OPSIONAL (Bisa diisi None jika tidak tahu) ---
jenis_kelamin        = 'Laki-laki'   # atau None
pendidikan           = 'S1'          # atau None
siapa_mengakhiri     = 'Pasangan yang mengakhiri' # atau None
masih_komunikasi     = 'Kadang-kadang'            # atau None
frekuensi_medsos     = 'Kadang-kadang'            # atau None
```

### 2. Logika Auto-Converter di Sistem
```python
def convert_ke_bulan(nilai, satuan):
    konversi = {'hari': 1/30, 'minggu': 1/4, 'bulan': 1, 'tahun': 12}
    return nilai * konversi[satuan]

def kategori_lama_hubungan(nilai, satuan):
    b = convert_ke_bulan(nilai, satuan)
    if   b < 6:   return '< 6 bulan'
    elif b < 12:  return '6 bulan - 1 tahun'
    elif b < 36:  return '1 - 3 tahun'
    elif b < 60:  return '3 - 5 tahun'
    else:         return '> 5 tahun'

def kategori_sejak_putus(nilai, satuan):
    b = convert_ke_bulan(nilai, satuan)
    if   b < 1:   return '< 1 bulan'
    elif b < 3:   return '1 - 3 bulan'
    elif b < 6:   return '3 - 6 bulan'
    elif b < 12:  return '6 - 12 bulan'
    else:         return '> 1 tahun'
```

---

## 📋 Master Checklist Tracker

- [x] **Tahap 0**: Setup Environment & Install Dependencies
- [x] **Tahap 1**: Data Understanding (Load `data.xlsx`, inspeksi dimensi & tipe data)
- [x] **Tahap 2**: Data Quality Check (Missing Values, Duplicates, Invalid Values)
- [x] **Tahap 3**: Data Cleaning (Penanganan missing, drop duplikat, standardisasi string)
- [x] **Tahap 4**: Outlier Detection & Handling (Pemeriksaan Umur & item kuesioner)
- [x] **Tahap 5**: Data Consistency Check (Validasi kategori agar seragam)
- [x] **Tahap 6**: Questionnaire Validity (Validasi item kuesioner 7 dimensi)
- [x] **Tahap 7**: Questionnaire Reliability (Cronbach's Alpha per dimensi)
- [x] **Tahap 8**: EDA (Exploratory Data Analysis & Visualisasi)
- [x] **Tahap 9**: Descriptive Statistics
- [x] **Tahap 10**: Heartbreak Score Construction (Hitung sub-score B-H, Reverse F & H, Formula HSS)
- [x] **Tahap 11**: Severity Label Construction (Ringan: 0, Sedang: 1, Berat: 2)
- [x] **Tahap 12**: Modeling Dataset (Ekstraksi 8 Fitur Demografis)
- [x] **Tahap 13**: Feature Engineering (Fitur turunan rasio / numerik durasi)
- [x] **Tahap 14**: Encoding (One-Hot Encoding aman & konsisten)
- [x] **Tahap 15**: Feature Selection (Chi-Square, ANOVA, Mutual Info, RFE)
- [x] **Tahap 16**: Train / Val / Test Split (70 / 15 / 15 Stratified)
- [x] **Tahap 17**: Preprocessing (StandardScaler)
- [x] **Tahap 18**: Class Imbalance Handling (Class Weight / SMOTE)
- [x] **Tahap 19**: Cross Validation Setup (Stratified 10-Fold)
- [x] **Tahap 20**: Baseline Model (Dummy & Logistic Regression)
- [x] **Tahap 21**: Model Training (8 Models: XGB, LGBM, CatBoost, MLP, RF, GB, SVM, AdaBoost)
- [x] **Tahap 22**: Hyperparameter Tuning (RandomizedSearchCV)
- [x] **Tahap 23**: Model Comparison & Ranking Table
- [x] **Tahap 24**: Feature Importance & SHAP Analysis
- [x] **Tahap 25**: Final Model & Soft Voting Ensemble
- [x] **Tahap 26**: Final Evaluation (Test Set, Metrics, CM, ROC-AUC)
- [x] **Tahap 27**: Error Analysis
- [x] **Tahap 28**: Probability Calibration
- [x] **Tahap 29**: Save Model Bundle (`heartbreak_demographic_bundle_v2.pkl`)
- [x] **Tahap 30**: Test Model V2 (`test_model_v2.ipynb` dengan input natural: hari/minggu/bulan/tahun)
