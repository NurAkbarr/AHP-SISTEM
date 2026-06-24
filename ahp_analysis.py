# -*- coding: utf-8 -*-
# =============================================================================
# ANALISIS PRIORITAS FAKTOR KEPUASAN PENGGUNA
# Sistem Informasi Dokumentasi dan Arsip Digital Kampus Berbasis Web
# Matla Islamic Academy
# Metode: Analytical Hierarchy Process (AHP)
# =============================================================================

import sys
import io
# Konfigurasi output UTF-8 untuk Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────────────────────────────────────
# KONFIGURASI GLOBAL
# ──────────────────────────────────────────────────────────────────────────────

# Faktor-faktor kepuasan pengguna (5 kriteria utama)
FAKTOR = [
    "Kemudahan\nPenggunaan",
    "Kelengkapan\nFitur",
    "Kecepatan\nAkses",
    "Keamanan\nData",
    "Kemudahan\nPencarian Arsip"
]

FAKTOR_SHORT = [
    "Kemudahan Penggunaan",
    "Kelengkapan Fitur",
    "Kecepatan Akses",
    "Keamanan Data",
    "Kemudahan Pencarian Arsip"
]

FAKTOR_KODE = ["K1", "K2", "K3", "K4", "K5"]

# Random Index (RI) untuk uji konsistensi AHP (Saaty, 1980)
RI_TABLE = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
}

# Skala perbandingan Saaty
SKALA_SAATY = {
    1: "Sama penting",
    2: "Antara 1 dan 3",
    3: "Sedikit lebih penting",
    4: "Antara 3 dan 5",
    5: "Lebih penting",
    6: "Antara 5 dan 7",
    7: "Sangat lebih penting",
    8: "Antara 7 dan 9",
    9: "Mutlak lebih penting"
}

# Konversi skala kuesioner 1-5 (bipolar) ke nilai AHP Saaty
# Referensi: skala disederhanakan untuk kemudahan responden
KONVERSI_FORM_AHP = {
    1: 5.0,        # Kiri jauh lebih penting  → Saaty 5
    2: 3.0,        # Kiri lebih penting       → Saaty 3
    3: 1.0,        # Sama penting             → Saaty 1
    4: 1/3,        # Kanan lebih penting      → Saaty 1/3
    5: 1/5,        # Kanan jauh lebih penting → Saaty 1/5
}

FORM_LABELS = [
    "1 – Kiri jauh lebih penting",
    "2 – Kiri lebih penting",
    "3 – Sama penting",
    "4 – Kanan lebih penting",
    "5 – Kanan jauh lebih penting",
]


def konversi_skala_form(nilai: int) -> float:
    """
    Konversi nilai kuesioner skala 1-5 (bipolar) ke nilai AHP Saaty.

    Skala kuesioner:
      1 = Faktor kiri jauh lebih penting  → AHP 5.0
      2 = Faktor kiri lebih penting       → AHP 3.0
      3 = Sama penting                    → AHP 1.0
      4 = Faktor kanan lebih penting      → AHP 1/3
      5 = Faktor kanan jauh lebih penting → AHP 1/5

    Parameter:
        nilai (int): Jawaban responden (1-5)
    Returns:
        float: Nilai AHP untuk entri matriks a_ij
    """
    return KONVERSI_FORM_AHP.get(int(nilai), 1.0)


def konversi_matriks_form(matriks_form: np.ndarray) -> np.ndarray:
    """
    Konversi matriks berisi jawaban form skala 1-5 (hanya segitiga atas)
    ke matriks AHP penuh (segitiga bawah diisi reciprocal otomatis).

    Parameter:
        matriks_form: matriks n×n berisi nilai 1-5 di segitiga atas,
                      diagonal = 3 (tidak digunakan), bawah = 0 atau apapun
    Returns:
        matriks AHP n×n dengan nilai Saaty yang benar
    """
    n = matriks_form.shape[0]
    m = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            ahp_val = konversi_skala_form(int(matriks_form[i][j]))
            m[i][j] = ahp_val
            m[j][i] = 1.0 / ahp_val
    np.fill_diagonal(m, 1.0)
    return m


# ──────────────────────────────────────────────────────────────────────────────
# KELAS UTAMA AHP
# ──────────────────────────────────────────────────────────────────────────────

class AHPAnalysis:
    """
    Kelas utama untuk melakukan analisis Analytical Hierarchy Process (AHP).
    Mencakup:
    - Konstruksi matriks perbandingan berpasangan
    - Normalisasi matriks
    - Perhitungan bobot prioritas (Priority Vector)
    - Uji konsistensi (CI dan CR)
    - Visualisasi hasil analisis
    """

    def __init__(self, nama_penelitian: str, faktor: list, faktor_kode: list):
        self.nama_penelitian = nama_penelitian
        self.faktor = faktor
        self.faktor_kode = faktor_kode
        self.n = len(faktor)
        self.matriks = None
        self.matriks_normalized = None
        self.bobot_prioritas = None
        self.lambda_max = None
        self.CI = None
        self.CR = None
        self.RI = RI_TABLE.get(self.n, 1.12)
        self.hasil_responden = []

    def set_matriks(self, matriks: np.ndarray):
        """
        Mengatur matriks perbandingan berpasangan.
        Matriks harus berukuran n×n dan bersifat reciprocal (a_ji = 1/a_ij).
        """
        assert matriks.shape == (self.n, self.n), \
            f"Matriks harus berukuran {self.n}×{self.n}"
        self.matriks = matriks.astype(float)
        # Pastikan diagonal = 1
        np.fill_diagonal(self.matriks, 1.0)
        # Pastikan reciprocal: a_ji = 1/a_ij
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.matriks[j][i] = 1.0 / self.matriks[i][j]
        return self

    def tambah_matriks_responden(self, matriks: np.ndarray, nama_responden: str = ""):
        """
        Menambahkan matriks dari satu responden ke daftar.
        Digunakan untuk agregasi matriks multi-responden.
        """
        m = matriks.astype(float)
        np.fill_diagonal(m, 1.0)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                m[j][i] = 1.0 / m[i][j]
        self.hasil_responden.append({
            'nama': nama_responden,
            'matriks': m
        })

    def agregasi_geometric_mean(self):
        """
        Mengagregasi matriks dari semua responden menggunakan rata-rata geometrik.
        Ini adalah metode yang direkomendasikan untuk AHP grup.
        """
        if not self.hasil_responden:
            raise ValueError("Belum ada data responden yang ditambahkan!")

        n_resp = len(self.hasil_responden)
        matriks_agg = np.ones((self.n, self.n))

        for i in range(self.n):
            for j in range(self.n):
                nilai_list = [r['matriks'][i][j] for r in self.hasil_responden]
                # Rata-rata geometrik
                matriks_agg[i][j] = np.exp(np.mean(np.log(nilai_list)))

        self.matriks = matriks_agg
        print(f"[OK] Agregasi {n_resp} responden berhasil menggunakan rata-rata geometrik.")
        return self

    def hitung_normalisasi(self):
        """
        Normalisasi matriks perbandingan berpasangan.
        Setiap elemen dibagi dengan jumlah kolomnya.
        """
        if self.matriks is None:
            raise ValueError("Matriks belum diatur!")

        # Hitung jumlah setiap kolom
        jumlah_kolom = self.matriks.sum(axis=0)

        # Normalisasi: setiap elemen dibagi jumlah kolomnya
        self.matriks_normalized = self.matriks / jumlah_kolom

        return self

    def hitung_bobot_prioritas(self):
        """
        Menghitung vektor prioritas (bobot) dari matriks ternormalisasi.
        Bobot = rata-rata setiap baris dari matriks ternormalisasi.
        """
        if self.matriks_normalized is None:
            self.hitung_normalisasi()

        # Priority vector = rata-rata baris
        self.bobot_prioritas = self.matriks_normalized.mean(axis=1)

        return self

    def hitung_konsistensi(self):
        """
        Menghitung Consistency Index (CI) dan Consistency Ratio (CR).
        - λmax = rata-rata dari (Aw)_i / w_i
        - CI = (λmax - n) / (n - 1)
        - CR = CI / RI
        - CR ≤ 0.1 → konsisten
        """
        if self.bobot_prioritas is None:
            self.hitung_bobot_prioritas()

        # Weighted sum vector: A × w
        weighted_sum = np.dot(self.matriks, self.bobot_prioritas)

        # λmax
        self.lambda_max = np.mean(weighted_sum / self.bobot_prioritas)

        # Consistency Index
        self.CI = (self.lambda_max - self.n) / (self.n - 1)

        # Consistency Ratio
        self.CR = self.CI / self.RI

        return self

    def jalankan_semua(self):
        """Menjalankan seluruh tahapan AHP secara berurutan."""
        self.hitung_normalisasi()
        self.hitung_bobot_prioritas()
        self.hitung_konsistensi()
        return self

    def cetak_matriks(self):
        """Mencetak matriks perbandingan berpasangan ke konsol."""
        df = pd.DataFrame(
            self.matriks,
            index=self.faktor_kode,
            columns=self.faktor_kode
        )
        print("\n" + "="*60)
        print("[MATRIKS] MATRIKS PERBANDINGAN BERPASANGAN")
        print("="*60)
        print(df.round(4).to_string())

    def cetak_normalisasi(self):
        """Mencetak matriks ternormalisasi."""
        df = pd.DataFrame(
            self.matriks_normalized,
            index=self.faktor_kode,
            columns=self.faktor_kode
        )
        print("\n" + "="*60)
        print("[GRAFIK] MATRIKS TERNORMALISASI")
        print("="*60)
        print(df.round(4).to_string())

    def cetak_hasil(self):
        """Mencetak hasil lengkap analisis AHP."""
        print("\n" + "="*60)
        print("[HASIL] HASIL ANALISIS AHP - BOBOT PRIORITAS")
        print("="*60)

        # Tabel bobot prioritas
        data = {
            'Kode': self.faktor_kode,
            'Faktor': FAKTOR_SHORT,
            'Bobot (%)': (self.bobot_prioritas * 100).round(4),
            'Peringkat': None
        }
        df_hasil = pd.DataFrame(data)
        df_hasil = df_hasil.sort_values('Bobot (%)', ascending=False)
        df_hasil['Peringkat'] = range(1, self.n + 1)
        print(df_hasil.to_string(index=False))

        print("\n" + "="*60)
        print("[UJI] UJI KONSISTENSI")
        print("="*60)
        print(f"  λmax (Lambda Max)        : {self.lambda_max:.6f}")
        print(f"  n (Jumlah Kriteria)      : {self.n}")
        print(f"  CI (Consistency Index)   : {self.CI:.6f}")
        print(f"  RI (Random Index)        : {self.RI}")
        print(f"  CR (Consistency Ratio)   : {self.CR:.6f}")
        print()

        if self.CR <= 0.1:
            print(f"  [OK] CR = {self.CR:.4f} ≤ 0.10 → KONSISTEN")
            print("  Penilaian responden DAPAT diterima dan digunakan.")
        else:
            print(f"  [X] CR = {self.CR:.4f} > 0.10 → TIDAK KONSISTEN")
            print("  Penilaian perlu DITINJAU KEMBALI oleh responden.")

        print("\n" + "="*60)
        print("[INFO] KESIMPULAN PRIORITAS")
        print("="*60)
        df_sorted = df_hasil.reset_index(drop=True)
        for _, row in df_sorted.iterrows():
            bar = "█" * int(row['Bobot (%)'] / 2)
            print(f"  {int(row['Peringkat'])}. {row['Kode']} - {FAKTOR_SHORT[self.faktor_kode.index(row['Kode'])]}")
            print(f"     {bar} {row['Bobot (%)']:.2f}%")
        print()

    def ekspor_excel(self, filename="hasil_ahp.xlsx"):
        """Mengekspor hasil analisis ke file Excel."""
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Matriks perbandingan
            df_matriks = pd.DataFrame(
                self.matriks,
                index=self.faktor_kode,
                columns=self.faktor_kode
            )
            df_matriks.round(4).to_excel(writer, sheet_name='Matriks Perbandingan')

            # Sheet 2: Matriks normalisasi
            df_norm = pd.DataFrame(
                self.matriks_normalized,
                index=self.faktor_kode,
                columns=self.faktor_kode
            )
            df_norm.round(4).to_excel(writer, sheet_name='Matriks Ternormalisasi')

            # Sheet 3: Hasil prioritas
            data_hasil = {
                'Kode': self.faktor_kode,
                'Faktor Kepuasan': FAKTOR_SHORT,
                'Bobot Prioritas': self.bobot_prioritas.round(6),
                'Bobot (%)': (self.bobot_prioritas * 100).round(4)
            }
            df_hasil = pd.DataFrame(data_hasil)
            df_hasil = df_hasil.sort_values('Bobot Prioritas', ascending=False)
            df_hasil['Peringkat'] = range(1, self.n + 1)
            df_hasil.to_excel(writer, sheet_name='Hasil Prioritas', index=False)

            # Sheet 4: Uji konsistensi
            data_ci = {
                'Parameter': ['Lambda Max (λmax)', 'Jumlah Kriteria (n)', 
                               'Consistency Index (CI)', 'Random Index (RI)',
                               'Consistency Ratio (CR)', 'Batas CR', 'Status'],
                'Nilai': [
                    round(self.lambda_max, 6),
                    self.n,
                    round(self.CI, 6),
                    self.RI,
                    round(self.CR, 6),
                    0.1,
                    "KONSISTEN" if self.CR <= 0.1 else "TIDAK KONSISTEN"
                ]
            }
            pd.DataFrame(data_ci).to_excel(writer, sheet_name='Uji Konsistensi', index=False)

        print(f"\n[OK] Hasil telah diekspor ke: {filename}")


# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI VISUALISASI
# ──────────────────────────────────────────────────────────────────────────────

def buat_visualisasi_lengkap(ahp: AHPAnalysis, save_path="hasil_visualisasi_ahp.png"):
    """
    Membuat visualisasi komprehensif hasil analisis AHP.
    Mencakup: Bar chart, Pie chart, Heatmap matriks, dan Gauge konsistensi.
    """
    # Warna tema - menggunakan palet biru-ungu profesional
    WARNA_UTAMA = ['#2563EB', '#7C3AED', '#0EA5E9', '#10B981', '#F59E0B']
    WARNA_BG = '#0F172A'
    WARNA_CARD = '#1E293B'
    WARNA_TEXT = '#F8FAFC'
    WARNA_SUBTEXT = '#94A3B8'

    # Sort faktor berdasarkan bobot
    idx_sorted = np.argsort(ahp.bobot_prioritas)[::-1]
    bobot_sorted = ahp.bobot_prioritas[idx_sorted]
    faktor_sorted = [FAKTOR_SHORT[i] for i in idx_sorted]
    kode_sorted = [ahp.faktor_kode[i] for i in idx_sorted]
    warna_sorted = [WARNA_UTAMA[i % len(WARNA_UTAMA)] for i in idx_sorted]

    # Setup figure
    fig = plt.figure(figsize=(20, 24), facecolor=WARNA_BG)
    gs = GridSpec(4, 2, figure=fig, hspace=0.45, wspace=0.35,
                  top=0.94, bottom=0.04, left=0.06, right=0.97)

    # ── JUDUL ──────────────────────────────────────────────────────────────────
    fig.text(0.5, 0.97, 'ANALISIS AHP – PRIORITAS FAKTOR KEPUASAN PENGGUNA',
             ha='center', va='top', fontsize=18, fontweight='bold',
             color=WARNA_TEXT, fontfamily='DejaVu Sans')
    fig.text(0.5, 0.955,
             'Sistem Informasi Dokumentasi & Arsip Digital Kampus Berbasis Web\n'
             'Matla Islamic Academy',
             ha='center', va='top', fontsize=12, color=WARNA_SUBTEXT,
             fontfamily='DejaVu Sans')

    # ── PANEL 1: Bar Chart Horizontal ─────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(WARNA_CARD)
    bars = ax1.barh(range(ahp.n), bobot_sorted * 100,
                    color=warna_sorted, height=0.6, edgecolor='none')

    # Tambahkan label nilai
    for bar, val, kode in zip(bars, bobot_sorted, kode_sorted):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                 f'{val * 100:.2f}%', va='center', ha='left',
                 fontsize=13, fontweight='bold', color=WARNA_TEXT)
        ax1.text(0.3, bar.get_y() + bar.get_height() / 2,
                 kode, va='center', ha='left',
                 fontsize=11, fontweight='bold', color='white', alpha=0.9)

    ax1.set_yticks(range(ahp.n))
    ax1.set_yticklabels(faktor_sorted, fontsize=12, color=WARNA_TEXT)
    ax1.set_xlabel('Bobot Prioritas (%)', fontsize=12, color=WARNA_SUBTEXT)
    ax1.set_title('Peringkat Bobot Prioritas Faktor Kepuasan Pengguna',
                  fontsize=14, fontweight='bold', color=WARNA_TEXT, pad=12)
    ax1.tick_params(colors=WARNA_SUBTEXT)
    ax1.spines[:].set_color(WARNA_CARD)
    ax1.set_xlim(0, max(bobot_sorted * 100) * 1.15)
    ax1.invert_yaxis()
    ax1.grid(axis='x', color='#334155', linestyle='--', alpha=0.5)

    # ── PANEL 2: Pie Chart ─────────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(WARNA_CARD)
    _pie_result = ax2.pie(
        bobot_sorted,
        colors=warna_sorted,
        autopct='%1.2f%%',
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(edgecolor=WARNA_BG, linewidth=2.5)
    )
    wedges, texts, autotexts = _pie_result[0], _pie_result[1], _pie_result[2]
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(10)
        at.set_fontweight('bold')
    for t in texts:
        t.set_color(WARNA_TEXT)

    # Legend
    legend_labels = [f"{kode}: {fk}" for kode, fk in zip(kode_sorted, faktor_sorted)]
    ax2.legend(wedges, legend_labels, loc='lower center', bbox_to_anchor=(0.5, -0.18),
               fontsize=9, frameon=False, labelcolor=WARNA_TEXT, ncol=1)
    ax2.set_title('Distribusi Bobot Kepuasan', fontsize=13,
                  fontweight='bold', color=WARNA_TEXT, pad=12)

    # ── PANEL 3: Heatmap Matriks Perbandingan ─────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(WARNA_CARD)
    mask = np.zeros_like(ahp.matriks, dtype=bool)
    log_matriks = np.log(ahp.matriks + 1e-10)
    sns.heatmap(
        log_matriks,
        ax=ax3,
        cmap='coolwarm',
        annot=ahp.matriks.round(2),
        fmt='.2f',
        xticklabels=ahp.faktor_kode,
        yticklabels=ahp.faktor_kode,
        linewidths=0.5,
        linecolor=WARNA_BG,
        cbar_kws={'label': 'Log(nilai perbandingan)'}
    )
    ax3.set_title('Heatmap Matriks Perbandingan Berpasangan',
                  fontsize=12, fontweight='bold', color=WARNA_TEXT, pad=12)
    ax3.tick_params(colors=WARNA_TEXT)
    ax3.set_xticklabels(ahp.faktor_kode, color=WARNA_TEXT, fontsize=10)
    ax3.set_yticklabels(ahp.faktor_kode, color=WARNA_TEXT, fontsize=10, rotation=0)

    # ── PANEL 4: Tabel Normalisasi ─────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[2, :])
    ax4.set_facecolor(WARNA_CARD)
    ax4.axis('off')

    # Data tabel
    col_labels = ahp.faktor_kode + ['Bobot\nPrioritas', 'Bobot\n(%)']
    table_data = []
    for i, (kode, fname) in enumerate(zip(ahp.faktor_kode, FAKTOR_SHORT)):
        row = [f"{v:.4f}" for v in ahp.matriks_normalized[i]]
        row.append(f"{ahp.bobot_prioritas[i]:.4f}")
        row.append(f"{ahp.bobot_prioritas[i]*100:.2f}%")
        table_data.append(row)

    table = ax4.table(
        cellText=table_data,
        colLabels=col_labels,
        rowLabels=[f"{k}\n({FAKTOR_SHORT[j][:20]}...)" if len(FAKTOR_SHORT[j]) > 20
                   else f"{k}\n({FAKTOR_SHORT[j]})"
                   for j, k in enumerate(ahp.faktor_kode)],
        loc='center',
        cellLoc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)

    # Styling tabel
    for (row, col), cell in table.get_celld().items():
        cell.set_facecolor(WARNA_BG if row == 0 or col == -1 else WARNA_CARD)
        cell.set_text_props(color=WARNA_TEXT, fontsize=9)
        cell.set_edgecolor('#334155')

        # Highlight kolom bobot
        if col >= ahp.n:
            cell.set_facecolor('#1E3A5F')
            cell.set_text_props(color='#60A5FA', fontweight='bold')

    ax4.set_title('Matriks Ternormalisasi & Bobot Prioritas',
                  fontsize=13, fontweight='bold', color=WARNA_TEXT,
                  pad=12, loc='left', x=0.01)

    # ── PANEL 5: Gauge Konsistensi + Info Kotak ───────────────────────────────
    ax5 = fig.add_subplot(gs[3, 0])
    ax5.set_facecolor(WARNA_CARD)
    ax5.set_aspect('equal')

    # Gauge berbentuk setengah lingkaran
    theta = np.linspace(np.pi, 0, 200)
    cr_val = min(ahp.CR, 0.2)
    cr_pct = cr_val / 0.2

    # Latar gauge
    ax5.fill_between(np.cos(theta), np.sin(theta),
                     0.8 * np.cos(theta), 0.8 * np.sin(theta),
                     alpha=0.0)

    for i, (start, end, color) in enumerate([(np.pi, np.pi * 0.5, '#10B981'),
                                              (np.pi * 0.5, np.pi * 0.0, '#EF4444')]):
        t = np.linspace(start, end, 100)
        ax5.fill_between(np.cos(t), 0.8 * np.sin(t), np.sin(t),
                         color=color, alpha=0.3)

    # Jarum
    angle = np.pi - (cr_pct * np.pi)
    ax5.annotate('', xy=(0.7 * np.cos(angle), 0.7 * np.sin(angle)),
                 xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color='white', lw=3))

    # Label
    ax5.text(0, -0.15, f'CR = {ahp.CR:.4f}',
             ha='center', fontsize=16, fontweight='bold',
             color='#10B981' if ahp.CR <= 0.1 else '#EF4444')
    ax5.text(0, -0.35,
             '[OK] KONSISTEN' if ahp.CR <= 0.1 else '[X] TIDAK KONSISTEN',
             ha='center', fontsize=13, fontweight='bold',
             color='#10B981' if ahp.CR <= 0.1 else '#EF4444')
    ax5.text(-1.0, 0.05, '0.0\n(Ideal)', ha='center', fontsize=8, color='#64748B')
    ax5.text(1.0, 0.05, '0.2+\n(Buruk)', ha='center', fontsize=8, color='#64748B')
    ax5.text(0, 0.08, '0.1\n(Batas)', ha='center', fontsize=8, color='#94A3B8')

    ax5.set_xlim(-1.2, 1.2)
    ax5.set_ylim(-0.5, 1.15)
    ax5.axis('off')
    ax5.set_title('Uji Konsistensi (Consistency Ratio)',
                  fontsize=12, fontweight='bold', color=WARNA_TEXT)

    # ── PANEL 6: Ringkasan Statistik ──────────────────────────────────────────
    ax6 = fig.add_subplot(gs[3, 1])
    ax6.set_facecolor(WARNA_CARD)
    ax6.axis('off')

    info_items = [
        ("λmax (Lambda Max)", f"{ahp.lambda_max:.6f}"),
        ("Jumlah Kriteria (n)", f"{ahp.n}"),
        ("Consistency Index (CI)", f"{ahp.CI:.6f}"),
        ("Random Index (RI)", f"{ahp.RI}"),
        ("Consistency Ratio (CR)", f"{ahp.CR:.6f}"),
        ("Batas Konsistensi", "≤ 0.10"),
        ("Status", "KONSISTEN [OK]" if ahp.CR <= 0.1 else "TIDAK KONSISTEN [X]"),
        ("Prioritas Utama", f"{FAKTOR_SHORT[np.argmax(ahp.bobot_prioritas)]}"),
        ("Bobot Tertinggi", f"{ahp.bobot_prioritas.max()*100:.2f}%"),
    ]

    y_pos = 0.95
    ax6.text(0.05, y_pos, "[GRAFIK] Ringkasan Hasil Analisis AHP",
             transform=ax6.transAxes, fontsize=12, fontweight='bold',
             color=WARNA_TEXT, va='top')

    for label, value in info_items:
        y_pos -= 0.09
        ax6.text(0.05, y_pos, f"  {label}",
                 transform=ax6.transAxes, fontsize=9.5, color=WARNA_SUBTEXT, va='top')
        ax6.text(0.95, y_pos, value,
                 transform=ax6.transAxes, fontsize=9.5, color='#60A5FA',
                 fontweight='bold', va='top', ha='right')
        # Garis pemisah antar baris (menggunakan plot agar kompatibel)
        ax6.plot([0.03, 0.97], [y_pos - 0.012, y_pos - 0.012],
                 color='#334155', linewidth=0.5, transform=ax6.transAxes)

    plt.savefig(save_path, dpi=150, bbox_inches='tight',
                facecolor=WARNA_BG, edgecolor='none')
    print(f"\n[OK] Visualisasi disimpan: {save_path}")
    plt.show()
    plt.close()


def buat_visualisasi_detail_responden(ahp: AHPAnalysis, save_path="detail_responden.png"):
    """Membuat visualisasi perbandingan matriks tiap responden (jika ada multi-responden)."""
    if not ahp.hasil_responden:
        print("Tidak ada data responden individual untuk divisualisasikan.")
        return

    n_resp = len(ahp.hasil_responden)
    WARNA_BG = '#0F172A'
    WARNA_CARD = '#1E293B'
    WARNA_TEXT = '#F8FAFC'

    fig, axes = plt.subplots(
        (n_resp + 1) // 2, 2,
        figsize=(16, 5 * ((n_resp + 1) // 2)),
        facecolor=WARNA_BG
    )
    axes = axes.flatten() if n_resp > 1 else [axes]

    fig.suptitle('Matriks Perbandingan Per Responden',
                 fontsize=16, fontweight='bold', color=WARNA_TEXT, y=1.01)

    for idx, resp in enumerate(ahp.hasil_responden):
        ax = axes[idx]
        ax.set_facecolor(WARNA_CARD)
        sns.heatmap(
            np.log(resp['matriks'] + 1e-10),
            ax=ax,
            cmap='RdYlGn',
            annot=resp['matriks'].round(2),
            fmt='.2f',
            xticklabels=ahp.faktor_kode,
            yticklabels=ahp.faktor_kode,
            linewidths=0.3,
            cbar=False
        )
        ax.set_title(f"Responden: {resp['nama']}", fontsize=10,
                     color=WARNA_TEXT, fontweight='bold')
        ax.tick_params(colors=WARNA_TEXT)

    # Sembunyikan axis yang tidak terpakai
    for idx in range(n_resp, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.savefig(save_path, dpi=120, bbox_inches='tight', facecolor=WARNA_BG)
    print(f"[OK] Visualisasi responden disimpan: {save_path}")
    plt.show()
    plt.close()


# ──────────────────────────────────────────────────────────────────────────────
# DATA KUESIONER (CONTOH - GANTI DENGAN DATA ASLI ANDA)
# ──────────────────────────────────────────────────────────────────────────────

def muat_data_contoh():
    """
    Contoh matriks perbandingan berpasangan untuk demo.
    
    PETUNJUK PENGISIAN:
    Faktor yang dibandingkan:
      K1 = Kemudahan Penggunaan
      K2 = Kelengkapan Fitur
      K3 = Kecepatan Akses
      K4 = Keamanan Data
      K5 = Kemudahan Pencarian Arsip
    
    Skala Saaty:
      1   = Sama penting
      3   = Sedikit lebih penting
      5   = Lebih penting
      7   = Sangat lebih penting
      9   = Mutlak lebih penting
      2,4,6,8 = Nilai antara
    
    Cara baca: baris[i][j] = "Seberapa penting faktor i dibanding faktor j?"
    Jika faktor j lebih penting dari i, gunakan pecahan (1/3, 1/5, dst.)
    """
    
    # ── CONTOH MATRIKS AGREGASI (dari rata-rata responden) ──
    # Ganti nilai ini dengan hasil kuesioner Anda yang sudah diisi!
    # Format: matriks[i][j] = tingkat kepentingan faktor ke-i terhadap ke-j
    matriks_agregasi = np.array([
        # K1    K2    K3    K4    K5
        [1.000, 3.000, 5.000, 2.000, 4.000],  # K1: Kemudahan Penggunaan
        [1/3,   1.000, 3.000, 1/2,   2.000],  # K2: Kelengkapan Fitur
        [1/5,   1/3,   1.000, 1/4,   1/2  ],  # K3: Kecepatan Akses
        [1/2,   2.000, 4.000, 1.000, 3.000],  # K4: Keamanan Data
        [1/4,   1/2,   2.000, 1/3,   1.000],  # K5: Kemudahan Pencarian Arsip
    ])
    
    return matriks_agregasi


def muat_data_multi_responden():
    """
    Contoh data multi-responden. 
    Setiap responden mengisi kuesioner perbandingan berpasangan secara terpisah.
    
    Ganti dengan data kuesioner asli Anda!
    """
    responden = [
        {
            "nama": "Responden 1 (Admin)",
            "matriks": np.array([
                [1, 3, 5, 2, 4],
                [1/3, 1, 3, 1/2, 2],
                [1/5, 1/3, 1, 1/4, 1/2],
                [1/2, 2, 4, 1, 3],
                [1/4, 1/2, 2, 1/3, 1],
            ])
        },
        {
            "nama": "Responden 2 (Dosen)",
            "matriks": np.array([
                [1, 4, 6, 3, 5],
                [1/4, 1, 3, 1/2, 2],
                [1/6, 1/3, 1, 1/5, 1/3],
                [1/3, 2, 5, 1, 3],
                [1/5, 1/2, 3, 1/3, 1],
            ])
        },
        {
            "nama": "Responden 3 (Mahasiswa)",
            "matriks": np.array([
                [1, 3, 4, 2, 4],
                [1/3, 1, 2, 1/2, 2],
                [1/4, 1/2, 1, 1/3, 1],
                [1/2, 2, 3, 1, 3],
                [1/4, 1/2, 1, 1/3, 1],
            ])
        },
        {
            "nama": "Responden 4 (Staf)",
            "matriks": np.array([
                [1, 2, 5, 3, 4],
                [1/2, 1, 3, 1, 2],
                [1/5, 1/3, 1, 1/4, 1/2],
                [1/3, 1, 4, 1, 3],
                [1/4, 1/2, 2, 1/3, 1],
            ])
        },
        {
            "nama": "Responden 5 (Pimpinan)",
            "matriks": np.array([
                [1, 5, 7, 3, 5],
                [1/5, 1, 3, 1/2, 2],
                [1/7, 1/3, 1, 1/4, 1/3],
                [1/3, 2, 4, 1, 3],
                [1/5, 1/2, 3, 1/3, 1],
            ])
        },
    ]
    return responden


# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("  SISTEM ANALISIS AHP - KEPUASAN PENGGUNA SISTEM INFORMASI")
    print("  Matla Islamic Academy")
    print("  Python-Based Analytical Hierarchy Process Analysis")
    print("=" * 65)

    print("\n[MODE 1] Analisis Matriks Agregasi (Rata-rata semua responden)")
    print("-" * 65)

    # Inisialisasi objek AHP
    ahp = AHPAnalysis(
        nama_penelitian="Analisis Prioritas Faktor Kepuasan Pengguna Sistem Informasi Dokumentasi dan Arsip Digital Kampus",
        faktor=FAKTOR,
        faktor_kode=FAKTOR_KODE
    )

    # Muat matriks (ganti dengan data kuesioner asli Anda)
    matriks_input = muat_data_contoh()
    ahp.set_matriks(matriks_input)

    # Jalankan perhitungan AHP
    ahp.jalankan_semua()

    # Tampilkan hasil
    ahp.cetak_matriks()
    ahp.cetak_normalisasi()
    ahp.cetak_hasil()

    # Ekspor ke Excel
    ahp.ekspor_excel("hasil_ahp_agregasi.xlsx")

    # Buat visualisasi
    print("\n[GRAFIK] Membuat visualisasi...")
    buat_visualisasi_lengkap(ahp, "visualisasi_ahp_agregasi.png")

    print("\n" + "=" * 65)
    print("[MODE 2] Analisis Multi-Responden (Per Responden)")
    print("-" * 65)

    # AHP Multi-Responden
    ahp_multi = AHPAnalysis(
        nama_penelitian="AHP Multi-Responden",
        faktor=FAKTOR,
        faktor_kode=FAKTOR_KODE
    )

    # Tambahkan data tiap responden
    data_responden = muat_data_multi_responden()
    for resp in data_responden:
        ahp_multi.tambah_matriks_responden(resp['matriks'], resp['nama'])

    # Agregasi menggunakan rata-rata geometrik
    ahp_multi.agregasi_geometric_mean()

    # Jalankan perhitungan
    ahp_multi.jalankan_semua()
    ahp_multi.cetak_hasil()

    # Ekspor hasil multi-responden
    ahp_multi.ekspor_excel("hasil_ahp_multi_responden.xlsx")

    # Visualisasi per responden
    buat_visualisasi_detail_responden(ahp_multi, "visualisasi_per_responden.png")
    buat_visualisasi_lengkap(ahp_multi, "visualisasi_ahp_multi_responden.png")

    print("\n" + "=" * 65)
    print("[OK] ANALISIS SELESAI!")
    print("=" * 65)
    print("\nFile yang dihasilkan:")
    print("  [GRAFIK] hasil_ahp_agregasi.xlsx          → Hasil matriks agregasi")
    print("  [GRAFIK] hasil_ahp_multi_responden.xlsx   → Hasil multi-responden")
    print("  [PNG]  visualisasi_ahp_agregasi.png     → Grafik analisis agregasi")
    print("  [PNG]  visualisasi_ahp_multi_responden.png → Grafik multi-responden")
    print("  [PNG]  visualisasi_per_responden.png    → Heatmap tiap responden")


if __name__ == "__main__":
    main()
