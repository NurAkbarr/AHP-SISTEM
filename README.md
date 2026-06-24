# SISTEM ANALISIS AHP
## Analisis Prioritas Faktor Kepuasan Pengguna
### Sistem Informasi Dokumentasi dan Arsip Digital Kampus Berbasis Web
### Matla Islamic Academy

---

## 📁 Struktur File

```
SISTEM/
├── ahp_analysis.py          ← Script utama analisis AHP
├── input_kuesioner.py       ← Modul input data kuesioner
├── template_kuesioner_ahp.xlsx  ← Template untuk pengisian kuesioner (dibuat otomatis)
├── HASIL_ANALISIS_AHP.xlsx  ← Output hasil analisis (dibuat otomatis)
├── VISUALISASI_AHP_FINAL.png    ← Grafik hasil analisis (dibuat otomatis)
└── README.md                ← Panduan ini
```

---

## 🔢 Faktor-Faktor Kepuasan Pengguna (5 Kriteria)

| Kode | Nama Faktor | Deskripsi |
|------|-------------|-----------|
| K1 | Kemudahan Penggunaan | Kemudahan memahami, mengoperasikan, dan memanfaatkan fitur sistem |
| K2 | Kelengkapan Fitur | Ketersediaan fitur yang dibutuhkan dalam mengelola dokumentasi & arsip |
| K3 | Kecepatan Akses | Kemampuan sistem merespons permintaan dan menampilkan data arsip |
| K4 | Keamanan Data | Perlindungan data dari kehilangan, kerusakan, atau akses tidak berwenang |
| K5 | Kemudahan Pencarian Arsip | Kemudahan menemukan dan memperoleh kembali dokumen/arsip |

---

## 📏 Skala Perbandingan Saaty

| Nilai | Keterangan |
|-------|-----------|
| 1 | Sama penting |
| 3 | Sedikit lebih penting |
| 5 | Lebih penting |
| 7 | Sangat lebih penting |
| 9 | Mutlak lebih penting |
| 2, 4, 6, 8 | Nilai antara |
| 1/3, 1/5, 1/7, 1/9 | Kebalikan (faktor lain lebih penting) |

---

## 🚀 Cara Penggunaan

### Cara 1: Langsung Jalankan Demo
```bash
python ahp_analysis.py
```
Akan menggunakan data contoh dan menghasilkan semua output.

### Cara 2: Input dari Excel (DIREKOMENDASIKAN)

**Langkah 1:** Buat template Excel
```bash
python input_kuesioner.py
# Pilih: 1 (Buat template Excel)
```

**Langkah 2:** Buka `template_kuesioner_ahp.xlsx` dan isi data kuesioner

Format pengisian:
- Kolom A: Nama responden
- Kolom B-K: Nilai perbandingan (10 pasangan faktor)

**Langkah 3:** Jalankan analisis
```bash
python input_kuesioner.py
# Pilih: 2 (Analisis dari Excel)
```

### Cara 3: Input Manual di Terminal
```bash
python input_kuesioner.py
# Pilih: 3 (Input manual)
```

---

## 📐 Tahapan Perhitungan AHP

### 1. Matriks Perbandingan Berpasangan
- Dari jawaban kuesioner n responden
- Agregasi menggunakan **rata-rata geometrik**

### 2. Normalisasi Matriks
```
a_norm[i][j] = a[i][j] / sum_kolom[j]
```

### 3. Bobot Prioritas (Priority Vector)
```
w[i] = rata-rata baris ke-i dari matriks ternormalisasi
```

### 4. Uji Konsistensi
```
λmax  = rata-rata dari (A × w)[i] / w[i]
CI    = (λmax - n) / (n - 1)
CR    = CI / RI
```

| n (Kriteria) | RI (Random Index) |
|:---:|:---:|
| 3 | 0.58 |
| 4 | 0.90 |
| **5** | **1.12** |
| 6 | 1.24 |

**Ketentuan:** CR ≤ 0.1 → Penilaian KONSISTEN ✅

---

## 📊 Output yang Dihasilkan

| File | Isi |
|------|-----|
| `HASIL_ANALISIS_AHP.xlsx` | Matriks perbandingan, normalisasi, bobot, uji konsistensi |
| `VISUALISASI_AHP_FINAL.png` | Bar chart, pie chart, heatmap, gauge konsistensi |
| `VISUALISASI_PER_RESPONDEN.png` | Heatmap matriks tiap responden |

---

## ⚠️ Catatan Penting

1. **Nilai CR harus ≤ 0.1** → jika > 0.1, data perlu dikumpulkan ulang
2. **Diagonal matriks = 1** (otomatis diatur)
3. **Reciprocal otomatis** → jika K1vsK2 = 3, maka K2vsK1 = 1/3 (otomatis)
4. **Agregasi** → gunakan rata-rata geometrik untuk multi-responden
5. **Interpretasi** → faktor dengan bobot tertinggi = prioritas utama pengembangan sistem

---

## 🎓 Referensi

- Saaty, T.L. (1980). The Analytic Hierarchy Process. McGraw-Hill.
- Saka & Hasugian (2024). AHP Method to Determine Student Satisfaction Level.
- NumPy, Pandas, Matplotlib Documentation
