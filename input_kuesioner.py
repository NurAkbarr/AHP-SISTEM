# =============================================================================
# INPUT DATA KUESIONER AHP
# Sistem Informasi Dokumentasi dan Arsip Digital Kampus
# Matla Islamic Academy
# =============================================================================
#
# PANDUAN PENGISIAN:
# - Jalankan file ini untuk memasukkan data kuesioner secara manual
# - Atau impor data dari Excel menggunakan fungsi load_from_excel()
# - Hasil akan langsung digunakan oleh ahp_analysis.py
#
# SKALA SAATY:
# 1 = Sama penting (Equal importance)
# 2 = Antara 1 dan 3
# 3 = Sedikit lebih penting (Moderate importance)
# 4 = Antara 3 dan 5
# 5 = Lebih penting (Strong importance)
# 6 = Antara 5 dan 7
# 7 = Sangat lebih penting (Very strong importance)
# 8 = Antara 7 dan 9
# 9 = Mutlak lebih penting (Extreme importance)
#
# Jika faktor j lebih penting dari i → gunakan 1/nilai (contoh: 1/3)
# =============================================================================

import numpy as np
import pandas as pd
import os
import sys

# Tambahkan path agar bisa import ahp_analysis
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ahp_analysis import (
    AHPAnalysis, FAKTOR, FAKTOR_SHORT, FAKTOR_KODE,
    buat_visualisasi_lengkap, buat_visualisasi_detail_responden
)


# ──────────────────────────────────────────────────────────────────────────────
# KONSTANTA FAKTOR
# ──────────────────────────────────────────────────────────────────────────────

PENJELASAN_FAKTOR = {
    "K1": "Kemudahan Penggunaan (Ease of Use)\n"
          "     → Kemudahan pengguna memahami, mengoperasikan, dan memanfaatkan fitur sistem",
    "K2": "Kelengkapan Fitur (Feature Completeness)\n"
          "     → Ketersediaan fitur yang dibutuhkan dalam mengelola dokumentasi & arsip",
    "K3": "Kecepatan Akses (Access Speed)\n"
          "     → Kemampuan sistem merespons permintaan, membuka halaman, dan menampilkan data",
    "K4": "Keamanan Data (Data Security)\n"
          "     → Perlindungan data dari kehilangan, kerusakan, atau akses tidak berwenang",
    "K5": "Kemudahan Pencarian Arsip (Archive Retrieval Ease)\n"
          "     → Kemudahan menemukan, menelusuri, dan memperoleh kembali dokumen/arsip",
}


# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI INPUT MANUAL
# ──────────────────────────────────────────────────────────────────────────────

def tampilkan_skala():
    """Menampilkan panduan skala Saaty."""
    print("\n" + "="*60)
    print("📏 SKALA PERBANDINGAN SAATY")
    print("="*60)
    skala = [
        (1, "Sama penting"),
        (2, "Antara 1 dan 3"),
        (3, "Sedikit lebih penting"),
        (4, "Antara 3 dan 5"),
        (5, "Lebih penting"),
        (6, "Antara 5 dan 7"),
        (7, "Sangat lebih penting"),
        (8, "Antara 7 dan 9"),
        (9, "Mutlak lebih penting"),
    ]
    for nilai, keterangan in skala:
        print(f"  {nilai}  →  {keterangan}")
    print("\n  💡 Gunakan pecahan (1/3, 1/5) jika faktor kolom lebih penting dari faktor baris")
    print("="*60)


def tampilkan_faktor():
    """Menampilkan daftar faktor yang akan dibandingkan."""
    print("\n" + "="*60)
    print("📋 FAKTOR-FAKTOR KEPUASAN PENGGUNA")
    print("="*60)
    for kode, penjelasan in PENJELASAN_FAKTOR.items():
        print(f"\n  {kode}: {penjelasan}")
    print("="*60)


def input_matriks_manual(nama_responden: str = "Responden") -> np.ndarray:
    """
    Mode interaktif untuk memasukkan nilai matriks perbandingan berpasangan.
    Pengguna hanya perlu memasukkan nilai segitiga atas (n*(n-1)/2 nilai).
    """
    n = len(FAKTOR_KODE)
    matriks = np.ones((n, n))

    tampilkan_skala()
    tampilkan_faktor()

    print(f"\n📝 Masukkan nilai perbandingan berpasangan untuk: {nama_responden}")
    print("   (Anda hanya perlu mengisi segitiga atas matriks - 10 pasangan)\n")

    pasangan = 0
    total_pasangan = n * (n - 1) // 2

    for i in range(n):
        for j in range(i + 1, n):
            pasangan += 1
            print(f"  [{pasangan}/{total_pasangan}] Perbandingan:")
            print(f"    {FAKTOR_KODE[i]}: {PENJELASAN_FAKTOR[FAKTOR_KODE[i]].split(chr(10))[0]}")
            print(f"    vs")
            print(f"    {FAKTOR_KODE[j]}: {PENJELASAN_FAKTOR[FAKTOR_KODE[j]].split(chr(10))[0]}")
            print(f"\n  Seberapa penting {FAKTOR_KODE[i]} dibanding {FAKTOR_KODE[j]}?")
            print(f"  (Jika {FAKTOR_KODE[j]} lebih penting, masukkan 1/3, 1/5, dll.)")

            while True:
                try:
                    nilai_str = input(f"  Nilai [{FAKTOR_KODE[i]} vs {FAKTOR_KODE[j]}]: ").strip()
                    if '/' in nilai_str:
                        parts = nilai_str.split('/')
                        nilai = float(parts[0]) / float(parts[1])
                    else:
                        nilai = float(nilai_str)

                    if nilai <= 0 or nilai > 9:
                        print("  ⚠️  Nilai harus antara 1/9 dan 9. Coba lagi.")
                        continue

                    matriks[i][j] = nilai
                    matriks[j][i] = 1.0 / nilai
                    print(f"  ✅ Disimpan: {FAKTOR_KODE[i]} vs {FAKTOR_KODE[j]} = {nilai:.4f}\n")
                    break
                except (ValueError, ZeroDivisionError):
                    print("  ⚠️  Format tidak valid. Contoh: 3, 5, 1/3, 1/5")

    return matriks


# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI IMPORT DARI EXCEL
# ──────────────────────────────────────────────────────────────────────────────

def load_from_excel(filepath: str, sheet_name: str = "Sheet1") -> dict:
    """
    Membaca data kuesioner dari file Excel.
    
    Format Excel yang diharapkan:
    - Baris 1: Header (nama kolom)
    - Kolom A: Nama Responden
    - Kolom B-K: Nilai perbandingan berpasangan (10 kolom untuk 5 faktor)
    
    Urutan kolom (10 perbandingan berpasangan):
    K1vsK2, K1vsK3, K1vsK4, K1vsK5,
    K2vsK3, K2vsK4, K2vsK5,
    K3vsK4, K3vsK5,
    K4vsK5
    
    Returns:
        dict berisi 'responden' (list of dict) dan 'metadata'
    """
    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        print(f"✅ Berhasil membaca file: {filepath}")
        print(f"   Jumlah responden: {len(df)}")
        print(f"   Kolom: {list(df.columns)}")

        n = len(FAKTOR_KODE)
        pasangan_cols = []
        for i in range(n):
            for j in range(i + 1, n):
                col_name = f"{FAKTOR_KODE[i]}vs{FAKTOR_KODE[j]}"
                pasangan_cols.append((i, j, col_name))

        hasil_responden = []
        for _, row in df.iterrows():
            nama = str(row.iloc[0]) if len(row) > 0 else "Unknown"
            matriks = np.ones((n, n))

            for idx, (i, j, col_name) in enumerate(pasangan_cols):
                try:
                    # Coba ambil berdasarkan nama kolom
                    if col_name in df.columns:
                        val = float(row[col_name])
                    else:
                        # Fallback: ambil berdasarkan posisi kolom
                        val = float(row.iloc[idx + 1])

                    if val > 0:
                        matriks[i][j] = val
                        matriks[j][i] = 1.0 / val
                    else:
                        print(f"  ⚠️  Nilai tidak valid untuk {nama}: {col_name} = {val}")
                except (ValueError, IndexError) as e:
                    print(f"  ⚠️  Error baca {col_name} untuk {nama}: {e}")

            hasil_responden.append({'nama': nama, 'matriks': matriks})

        return {
            'responden': hasil_responden,
            'metadata': {
                'filepath': filepath,
                'jumlah_responden': len(hasil_responden),
                'faktor': FAKTOR_SHORT
            }
        }

    except FileNotFoundError:
        print(f"❌ File tidak ditemukan: {filepath}")
        return None
    except Exception as e:
        print(f"❌ Error membaca Excel: {e}")
        return None


def buat_template_excel(filepath: str = "template_kuesioner_ahp.xlsx"):
    """
    Membuat template Excel untuk pengisian kuesioner AHP.
    Responden dapat mengisi nilai perbandingan berpasangan langsung di Excel.
    """
    n = len(FAKTOR_KODE)
    
    # Header pasangan perbandingan
    pasangan_headers = []
    pasangan_desc = []
    for i in range(n):
        for j in range(i + 1, n):
            pasangan_headers.append(f"{FAKTOR_KODE[i]}vs{FAKTOR_KODE[j]}")
            pasangan_desc.append(
                f"Seberapa penting {FAKTOR_SHORT[i]} dibanding {FAKTOR_SHORT[j]}? "
                f"(1-9, atau 1/3, 1/5 jika {FAKTOR_SHORT[j]} lebih penting)"
            )
    
    # Data contoh (3 responden)
    data_contoh = [
        ["Responden 1 (Admin)", 3, 5, 2, 4, 3, 1/2, 2, 1/4, 1/2, 3],
        ["Responden 2 (Dosen)", 4, 6, 3, 5, 3, 1/2, 2, 1/5, 1/3, 3],
        ["Responden 3 (Mahasiswa)", 3, 4, 2, 4, 2, 1/2, 2, 1/4, 1/2, 3],
    ]
    
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Sheet 1: Form Kuesioner
        df_form = pd.DataFrame(
            data_contoh,
            columns=["Nama Responden"] + pasangan_headers
        )
        df_form.to_excel(writer, sheet_name='Data Kuesioner', index=False)
        
        # Sheet 2: Panduan
        panduan_data = {
            'Kolom': ["Nama Responden"] + pasangan_headers,
            'Keterangan': ["Nama atau ID responden"] + pasangan_desc
        }
        pd.DataFrame(panduan_data).to_excel(writer, sheet_name='Panduan', index=False)
        
        # Sheet 3: Referensi Skala Saaty
        skala_data = {
            'Nilai': [1, 2, 3, 4, 5, 6, 7, 8, 9,
                      '1/2', '1/3', '1/4', '1/5', '1/6', '1/7', '1/8', '1/9'],
            'Keterangan': [
                'Sama penting',
                'Antara 1 dan 3',
                'Sedikit lebih penting',
                'Antara 3 dan 5',
                'Lebih penting',
                'Antara 5 dan 7',
                'Sangat lebih penting',
                'Antara 7 dan 9',
                'Mutlak lebih penting',
                'Kebalikan dari 2',
                'Kebalikan dari 3',
                'Kebalikan dari 4',
                'Kebalikan dari 5',
                'Kebalikan dari 6',
                'Kebalikan dari 7',
                'Kebalikan dari 8',
                'Kebalikan dari 9',
            ]
        }
        pd.DataFrame(skala_data).to_excel(writer, sheet_name='Skala Saaty', index=False)
        
        # Sheet 4: Daftar Faktor
        faktor_data = {
            'Kode': list(PENJELASAN_FAKTOR.keys()),
            'Nama Faktor': FAKTOR_SHORT,
            'Deskripsi': [p.split('\n')[0] for p in PENJELASAN_FAKTOR.values()]
        }
        pd.DataFrame(faktor_data).to_excel(writer, sheet_name='Daftar Faktor', index=False)
    
    print(f"✅ Template Excel dibuat: {filepath}")
    print(f"   Isi data kuesioner pada sheet 'Data Kuesioner'")
    print(f"   Lihat panduan pada sheet 'Panduan'")
    return filepath


# ──────────────────────────────────────────────────────────────────────────────
# MAIN: INPUT DATA DAN ANALISIS
# ──────────────────────────────────────────────────────────────────────────────

def jalankan_dari_excel(filepath_excel: str):
    """
    Menjalankan analisis AHP dari file Excel yang sudah terisi.
    Gunakan fungsi ini setelah mengisi template_kuesioner_ahp.xlsx
    """
    print(f"\n🔄 Memuat data dari: {filepath_excel}")
    data = load_from_excel(filepath_excel)

    if not data:
        print("❌ Gagal memuat data!")
        return

    ahp = AHPAnalysis(
        nama_penelitian="Analisis Prioritas Kepuasan Pengguna - Matla Islamic Academy",
        faktor=FAKTOR,
        faktor_kode=FAKTOR_KODE
    )

    # Tambahkan semua responden
    for resp in data['responden']:
        ahp.tambah_matriks_responden(resp['matriks'], resp['nama'])

    # Agregasi menggunakan rata-rata geometrik
    ahp.agregasi_geometric_mean()

    # Jalankan analisis
    ahp.jalankan_semua()

    # Tampilkan dan ekspor hasil
    ahp.cetak_matriks()
    ahp.cetak_normalisasi()
    ahp.cetak_hasil()

    # Ekspor ke Excel
    ahp.ekspor_excel("HASIL_ANALISIS_AHP.xlsx")

    # Buat visualisasi
    buat_visualisasi_lengkap(ahp, "VISUALISASI_AHP_FINAL.png")
    buat_visualisasi_detail_responden(ahp, "VISUALISASI_PER_RESPONDEN.png")

    print("\n✅ Analisis selesai!")
    return ahp


def jalankan_input_manual():
    """Menjalankan input data secara manual (interaktif)."""
    print("\n🎯 MODE INPUT MANUAL")
    print("Masukkan data kuesioner untuk setiap responden\n")

    ahp = AHPAnalysis(
        nama_penelitian="Analisis Prioritas Kepuasan Pengguna - Matla Islamic Academy",
        faktor=FAKTOR,
        faktor_kode=FAKTOR_KODE
    )

    n_responden = int(input("Berapa jumlah responden? "))

    for i in range(1, n_responden + 1):
        nama = input(f"\nNama/ID Responden ke-{i}: ").strip() or f"Responden {i}"
        matriks = input_matriks_manual(nama)
        ahp.tambah_matriks_responden(matriks, nama)
        print(f"✅ Data {nama} berhasil ditambahkan.\n")

    # Agregasi
    ahp.agregasi_geometric_mean()
    ahp.jalankan_semua()

    # Tampilkan hasil
    ahp.cetak_matriks()
    ahp.cetak_normalisasi()
    ahp.cetak_hasil()

    # Ekspor
    ahp.ekspor_excel("HASIL_ANALISIS_AHP.xlsx")
    buat_visualisasi_lengkap(ahp, "VISUALISASI_AHP_FINAL.png")

    return ahp


if __name__ == "__main__":
    print("=" * 65)
    print("  SISTEM INPUT KUESIONER AHP")
    print("  Analisis Kepuasan Pengguna - Matla Islamic Academy")
    print("=" * 65)

    print("\nPilih mode input:")
    print("  1. Buat template Excel (untuk diisi responden)")
    print("  2. Analisis dari file Excel yang sudah diisi")
    print("  3. Input manual langsung di terminal")

    pilihan = input("\nMasukkan pilihan (1/2/3): ").strip()

    if pilihan == "1":
        buat_template_excel("template_kuesioner_ahp.xlsx")
        print("\n📋 Langkah selanjutnya:")
        print("  1. Buka file 'template_kuesioner_ahp.xlsx'")
        print("  2. Isi nilai perbandingan berpasangan untuk setiap responden")
        print("  3. Simpan file")
        print("  4. Jalankan program ini lagi dan pilih opsi 2")

    elif pilihan == "2":
        filepath = input("Masukkan nama file Excel (atau tekan Enter untuk 'template_kuesioner_ahp.xlsx'): ").strip()
        if not filepath:
            filepath = "template_kuesioner_ahp.xlsx"
        jalankan_dari_excel(filepath)

    elif pilihan == "3":
        jalankan_input_manual()

    else:
        print("❌ Pilihan tidak valid!")
