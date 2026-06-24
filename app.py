# -*- coding: utf-8 -*-
# =============================================================================
# STREAMLIT WEB APP - ANALISIS AHP
# Sistem Informasi Dokumentasi dan Arsip Digital Kampus
# Matla Islamic Academy
# =============================================================================

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.gridspec import GridSpec
import io
import warnings
warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AHP – Kepuasan Pengguna | Matla Islamic Academy",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────────────────────
# CSS CUSTOM
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background utama */
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #0F172A 100%);
    background-attachment: fixed;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #F8FAFC !important;
}

/* Card / container */
.ahp-card {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

/* Header hero */
.hero-header {
    background: linear-gradient(135deg, #1E3A5F, #2D1B69);
    border: 1px solid #3B82F6;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin-bottom: 28px;
}

.hero-header h1 {
    color: #F8FAFC;
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    background: linear-gradient(90deg, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-header p {
    color: #94A3B8;
    font-size: 1rem;
    margin: 0;
}

/* Metric cards */
.metric-box {
    background: rgba(30, 41, 59, 0.9);
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 16px 20px;
    text-align: center;
}

.metric-box .label {
    color: #94A3B8;
    font-size: 0.75rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

.metric-box .value {
    color: #60A5FA;
    font-size: 1.6rem;
    font-weight: 700;
}

/* Badge konsistensi */
.badge-ok {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid #10B981;
    color: #34D399;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.9rem;
    display: inline-block;
}

.badge-fail {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid #EF4444;
    color: #F87171;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 0.9rem;
    display: inline-block;
}

/* Rank table */
.rank-row {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    border-radius: 10px;
    margin-bottom: 8px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid #334155;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4) !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tab"] {
    color: #94A3B8 !important;
    font-weight: 500;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #60A5FA !important;
    font-weight: 600;
}

/* Data editor */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid #334155;
    margin: 24px 0;
}

/* Info box */
.info-box {
    background: rgba(37, 99, 235, 0.1);
    border: 1px solid #2563EB;
    border-radius: 10px;
    padding: 14px 18px;
    color: #93C5FD;
    font-size: 0.9rem;
}

.warning-box {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid #EF4444;
    border-radius: 10px;
    padding: 14px 18px;
    color: #FCA5A5;
    font-size: 0.9rem;
}

.success-box {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid #10B981;
    border-radius: 10px;
    padding: 14px 18px;
    color: #6EE7B7;
    font-size: 0.9rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1E293B; }
::-webkit-scrollbar-thumb { background: #475569; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# KONSTANTA
# ──────────────────────────────────────────────────────────────────────────────

FAKTOR_SHORT = [
    "Kemudahan Penggunaan",
    "Kelengkapan Fitur",
    "Kecepatan Akses",
    "Keamanan Data",
    "Kemudahan Pencarian Arsip"
]
FAKTOR_KODE = ["K1", "K2", "K3", "K4", "K5"]
N = 5

RI_TABLE = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

WARNA = ['#2563EB', '#7C3AED', '#0EA5E9', '#10B981', '#F59E0B']
WARNA_BG = '#0F172A'
WARNA_CARD = '#1E293B'
WARNA_TEXT = '#F8FAFC'
WARNA_SUBTEXT = '#94A3B8'

SKALA_SAATY = {
    "1 – Sama penting": 1,
    "2": 2,
    "3 – Sedikit lebih penting": 3,
    "4": 4,
    "5 – Lebih penting": 5,
    "6": 6,
    "7 – Sangat lebih penting": 7,
    "8": 8,
    "9 – Mutlak lebih penting": 9,
}

# Konversi skala kuesioner 1-5 bipolar → nilai AHP Saaty
KONVERSI_FORM_AHP = {
    1: 5.0,   # Kiri jauh lebih penting  → Saaty 5
    2: 3.0,   # Kiri lebih penting       → Saaty 3
    3: 1.0,   # Sama penting             → Saaty 1
    4: 1/3,   # Kanan lebih penting      → Saaty 1/3
    5: 1/5,   # Kanan jauh lebih penting → Saaty 1/5
}

FORM_LABELS = [
    "1 – Kiri jauh lebih penting",
    "2 – Kiri lebih penting",
    "3 – Sama penting",
    "4 – Kanan lebih penting",
    "5 – Kanan jauh lebih penting",
]

def konversi_skala_form(nilai: int) -> float:
    """Konversi jawaban form 1-5 ke nilai AHP Saaty."""
    return KONVERSI_FORM_AHP.get(int(nilai), 1.0)

def konversi_matriks_form(matriks_form: np.ndarray) -> np.ndarray:
    """Konversi matriks form 1-5 (segitiga atas) ke matriks AHP penuh."""
    n = matriks_form.shape[0]
    m = np.ones((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            ahp_val = konversi_skala_form(int(round(matriks_form[i][j])))
            m[i][j] = ahp_val
            m[j][i] = 1.0 / ahp_val
    np.fill_diagonal(m, 1.0)
    return m

# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI AHP CORE
# ──────────────────────────────────────────────────────────────────────────────

def enforce_reciprocal(matriks: np.ndarray) -> np.ndarray:
    m = matriks.astype(float).copy()
    np.fill_diagonal(m, 1.0)
    for i in range(N):
        for j in range(i + 1, N):
            m[j][i] = 1.0 / m[i][j]
    return m

def hitung_ahp(matriks: np.ndarray):
    m = enforce_reciprocal(matriks)
    jumlah_kolom = m.sum(axis=0)
    m_norm = m / jumlah_kolom
    bobot = m_norm.mean(axis=1)
    weighted_sum = np.dot(m, bobot)
    lambda_max = np.mean(weighted_sum / bobot)
    ci = (lambda_max - N) / (N - 1)
    ri = RI_TABLE.get(N, 1.12)
    cr = ci / ri
    return m, m_norm, bobot, lambda_max, ci, ri, cr

def agregasi_geometric_mean(list_matriks: list) -> np.ndarray:
    matriks_agg = np.ones((N, N))
    for i in range(N):
        for j in range(N):
            vals = [m[i][j] for m in list_matriks]
            matriks_agg[i][j] = np.exp(np.mean(np.log(vals)))
    return matriks_agg

# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI VISUALISASI MATPLOTLIB
# ──────────────────────────────────────────────────────────────────────────────

def buat_chart_lengkap(matriks, m_norm, bobot, lambda_max, ci, ri, cr, judul=""):
    idx_sorted = np.argsort(bobot)[::-1]
    bobot_sorted = bobot[idx_sorted]
    faktor_sorted = [FAKTOR_SHORT[i] for i in idx_sorted]
    kode_sorted = [FAKTOR_KODE[i] for i in idx_sorted]
    warna_sorted = [WARNA[i % len(WARNA)] for i in idx_sorted]

    fig = plt.figure(figsize=(18, 20), facecolor=WARNA_BG)
    gs = GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35,
                  top=0.94, bottom=0.04, left=0.07, right=0.97)

    if judul:
        fig.text(0.5, 0.97, judul, ha='center', va='top',
                 fontsize=15, fontweight='bold', color=WARNA_TEXT)

    # Bar chart
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_facecolor(WARNA_CARD)
    bars = ax1.barh(range(N), bobot_sorted * 100,
                    color=warna_sorted, height=0.55, edgecolor='none')
    for bar, val, kode in zip(bars, bobot_sorted, kode_sorted):
        ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                 f'{val * 100:.2f}%', va='center', ha='left',
                 fontsize=12, fontweight='bold', color=WARNA_TEXT)
        ax1.text(0.3, bar.get_y() + bar.get_height() / 2,
                 kode, va='center', ha='left',
                 fontsize=10, fontweight='bold', color='white', alpha=0.9)
    ax1.set_yticks(range(N))
    ax1.set_yticklabels(faktor_sorted, fontsize=11, color=WARNA_TEXT)
    ax1.set_xlabel('Bobot Prioritas (%)', fontsize=11, color=WARNA_SUBTEXT)
    ax1.set_title('Peringkat Bobot Prioritas Faktor Kepuasan Pengguna',
                  fontsize=13, fontweight='bold', color=WARNA_TEXT, pad=10)
    ax1.tick_params(colors=WARNA_SUBTEXT)
    ax1.spines[:].set_color(WARNA_CARD)
    ax1.set_xlim(0, max(bobot_sorted * 100) * 1.15)
    ax1.invert_yaxis()
    ax1.grid(axis='x', color='#334155', linestyle='--', alpha=0.5)

    # Pie chart
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor(WARNA_CARD)
    _pie_result = ax2.pie(
        bobot_sorted, colors=warna_sorted, autopct='%1.2f%%',
        startangle=90, pctdistance=0.75,
        wedgeprops=dict(edgecolor=WARNA_BG, linewidth=2.5))
    wedges, texts, autotexts = _pie_result[0], _pie_result[1], _pie_result[2]
    for at in autotexts:
        at.set_color('white'); at.set_fontsize(9); at.set_fontweight('bold')
    legend_labels = [f"{k}: {f}" for k, f in zip(kode_sorted, faktor_sorted)]
    ax2.legend(wedges, legend_labels, loc='lower center',
               bbox_to_anchor=(0.5, -0.20), fontsize=8,
               frameon=False, labelcolor=WARNA_TEXT, ncol=1)
    ax2.set_title('Distribusi Bobot', fontsize=12,
                  fontweight='bold', color=WARNA_TEXT, pad=10)

    # Heatmap
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor(WARNA_CARD)
    log_m = np.log(matriks + 1e-10)
    sns.heatmap(log_m, ax=ax3, cmap='coolwarm',
                annot=matriks.round(2), fmt='.2f',
                xticklabels=FAKTOR_KODE, yticklabels=FAKTOR_KODE,
                linewidths=0.5, linecolor=WARNA_BG,
                cbar_kws={'label': 'Log(nilai)'})
    ax3.set_title('Heatmap Matriks Perbandingan',
                  fontsize=12, fontweight='bold', color=WARNA_TEXT, pad=10)
    ax3.tick_params(colors=WARNA_TEXT)
    ax3.set_xticklabels(FAKTOR_KODE, color=WARNA_TEXT, fontsize=9)
    ax3.set_yticklabels(FAKTOR_KODE, color=WARNA_TEXT, fontsize=9, rotation=0)

    # Gauge konsistensi
    ax5 = fig.add_subplot(gs[2, 0])
    ax5.set_facecolor(WARNA_CARD)
    ax5.set_aspect('equal')
    theta = np.linspace(np.pi, 0, 200)
    cr_pct = min(cr, 0.2) / 0.2
    for start, end, color in [(np.pi, np.pi * 0.5, '#10B981'),
                               (np.pi * 0.5, np.pi * 0.0, '#EF4444')]:
        t = np.linspace(start, end, 100)
        ax5.fill_between(np.cos(t), 0.8 * np.sin(t), np.sin(t), color=color, alpha=0.3)
    angle = np.pi - (cr_pct * np.pi)
    ax5.annotate('', xy=(0.7 * np.cos(angle), 0.7 * np.sin(angle)),
                 xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='white', lw=3))
    cr_color = '#10B981' if cr <= 0.1 else '#EF4444'
    ax5.text(0, -0.15, f'CR = {cr:.4f}', ha='center', fontsize=15,
             fontweight='bold', color=cr_color)
    ax5.text(0, -0.35, 'KONSISTEN ✓' if cr <= 0.1 else 'TIDAK KONSISTEN ✗',
             ha='center', fontsize=12, fontweight='bold', color=cr_color)
    ax5.text(-1.0, 0.05, '0.0\n(Ideal)', ha='center', fontsize=8, color='#64748B')
    ax5.text(1.0, 0.05, '0.2+\n(Buruk)', ha='center', fontsize=8, color='#64748B')
    ax5.set_xlim(-1.2, 1.2); ax5.set_ylim(-0.5, 1.15); ax5.axis('off')
    ax5.set_title('Uji Konsistensi (CR)', fontsize=12,
                  fontweight='bold', color=WARNA_TEXT)

    # Ringkasan
    ax6 = fig.add_subplot(gs[2, 1])
    ax6.set_facecolor(WARNA_CARD)
    ax6.axis('off')
    prioritas_utama = FAKTOR_SHORT[np.argmax(bobot)]
    info_items = [
        ("λmax (Lambda Max)", f"{lambda_max:.6f}"),
        ("Jumlah Kriteria (n)", f"{N}"),
        ("Consistency Index (CI)", f"{ci:.6f}"),
        ("Random Index (RI)", f"{ri}"),
        ("Consistency Ratio (CR)", f"{cr:.6f}"),
        ("Batas Konsistensi", "≤ 0.10"),
        ("Status", "KONSISTEN ✓" if cr <= 0.1 else "TIDAK KONSISTEN ✗"),
        ("Prioritas Utama", prioritas_utama),
        ("Bobot Tertinggi", f"{bobot.max()*100:.2f}%"),
    ]
    y_pos = 0.95
    ax6.text(0.05, y_pos, "Ringkasan Hasil Analisis AHP",
             transform=ax6.transAxes, fontsize=11, fontweight='bold',
             color=WARNA_TEXT, va='top')
    for label, value in info_items:
        y_pos -= 0.09
        ax6.text(0.05, y_pos, f"  {label}", transform=ax6.transAxes,
                 fontsize=9, color=WARNA_SUBTEXT, va='top')
        val_color = '#F87171' if ("TIDAK" in value) else '#60A5FA'
        ax6.text(0.95, y_pos, value, transform=ax6.transAxes,
                 fontsize=9, color=val_color, fontweight='bold', va='top', ha='right')
        ax6.plot([0.03, 0.97], [y_pos - 0.012, y_pos - 0.012],
                 color='#334155', linewidth=0.5, transform=ax6.transAxes)

    return fig


def buat_chart_per_responden(list_matriks, list_nama):
    n_resp = len(list_matriks)
    cols = 2
    rows = (n_resp + 1) // 2
    fig, axes = plt.subplots(rows, cols, figsize=(14, 5 * rows), facecolor=WARNA_BG)
    axes = axes.flatten() if n_resp > 1 else [axes]
    fig.suptitle('Matriks Perbandingan Per Responden',
                 fontsize=14, fontweight='bold', color=WARNA_TEXT, y=1.01)
    for idx, (mat, nama) in enumerate(zip(list_matriks, list_nama)):
        ax = axes[idx]
        ax.set_facecolor(WARNA_CARD)
        sns.heatmap(np.log(mat + 1e-10), ax=ax, cmap='RdYlGn',
                    annot=mat.round(2), fmt='.2f',
                    xticklabels=FAKTOR_KODE, yticklabels=FAKTOR_KODE,
                    linewidths=0.3, cbar=False)
        ax.set_title(f"Responden: {nama}", fontsize=10, color=WARNA_TEXT, fontweight='bold')
        ax.tick_params(colors=WARNA_TEXT)
    for idx in range(n_resp, len(axes)):
        axes[idx].axis('off')
    plt.tight_layout()
    return fig


# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI EXPORT EXCEL
# ──────────────────────────────────────────────────────────────────────────────

def export_excel(matriks, m_norm, bobot, lambda_max, ci, ri, cr) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        pd.DataFrame(matriks.round(4), index=FAKTOR_KODE, columns=FAKTOR_KODE) \
            .to_excel(writer, sheet_name='Matriks Perbandingan')
        pd.DataFrame(m_norm.round(4), index=FAKTOR_KODE, columns=FAKTOR_KODE) \
            .to_excel(writer, sheet_name='Matriks Ternormalisasi')
        df_hasil = pd.DataFrame({
            'Kode': FAKTOR_KODE,
            'Faktor': FAKTOR_SHORT,
            'Bobot Prioritas': bobot.round(6),
            'Bobot (%)': (bobot * 100).round(4)
        }).sort_values('Bobot Prioritas', ascending=False)
        df_hasil['Peringkat'] = range(1, N + 1)
        df_hasil.to_excel(writer, sheet_name='Hasil Prioritas', index=False)
        pd.DataFrame({
            'Parameter': ['Lambda Max', 'n', 'CI', 'RI', 'CR', 'Batas', 'Status'],
            'Nilai': [round(lambda_max, 6), N, round(ci, 6), ri,
                      round(cr, 6), 0.1, "KONSISTEN" if cr <= 0.1 else "TIDAK KONSISTEN"]
        }).to_excel(writer, sheet_name='Uji Konsistensi', index=False)
    return buf.getvalue()

def export_chart(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=WARNA_BG, edgecolor='none')
    buf.seek(0)
    return buf.getvalue()

# ──────────────────────────────────────────────────────────────────────────────
# KOMPONEN UI BERULANG
# ──────────────────────────────────────────────────────────────────────────────

def tampil_hasil(matriks, m_norm, bobot, lambda_max, ci, ri, cr, mode_label=""):
    """Menampilkan seluruh hasil AHP: metrics, ranking, chart, download."""

    # Metrics row
    idx_top = int(np.argmax(bobot))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="metric-box">
            <div class="label">CR (Consistency Ratio)</div>
            <div class="value" style="color:{'#34D399' if cr<=0.1 else '#F87171'}">{cr:.4f}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-box">
            <div class="label">λmax</div>
            <div class="value">{lambda_max:.4f}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-box">
            <div class="label">Prioritas Utama</div>
            <div class="value" style="font-size:1rem;color:#A78BFA">{FAKTOR_KODE[idx_top]}</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        status_html = ('<span class="badge-ok">✓ KONSISTEN</span>'
                       if cr <= 0.1 else '<span class="badge-fail">✗ TIDAK KONSISTEN</span>')
        st.markdown(f"""<div class="metric-box">
            <div class="label">Status</div>
            <div style="margin-top:6px">{status_html}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabel ranking + tabs grafik
    tab_rank, tab_chart, tab_matrix = st.tabs(["🏆 Peringkat", "📊 Grafik", "🔢 Matriks Detail"])

    with tab_rank:
        st.markdown("#### Bobot Prioritas Faktor Kepuasan Pengguna")
        idx_sorted = np.argsort(bobot)[::-1]
        emoji_rank = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
        for rank, i in enumerate(idx_sorted):
            pct = bobot[i] * 100
            bar_width = int(pct * 2)
            bar_html = f'<div style="background:linear-gradient(90deg,{WARNA[i]},transparent);height:8px;width:{bar_width}%;border-radius:4px;margin-top:4px;"></div>'
            st.markdown(f"""
            <div class="rank-row">
                <span style="font-size:1.4rem;margin-right:12px">{emoji_rank[rank]}</span>
                <div style="flex:1">
                    <div style="color:#F8FAFC;font-weight:600">{FAKTOR_SHORT[i]}</div>
                    <div style="color:#94A3B8;font-size:0.8rem">{FAKTOR_KODE[i]}</div>
                    {bar_html}
                </div>
                <span style="color:{WARNA[i]};font-size:1.3rem;font-weight:700;margin-left:16px">{pct:.2f}%</span>
            </div>""", unsafe_allow_html=True)

    with tab_chart:
        with st.spinner("Membuat grafik..."):
            fig = buat_chart_lengkap(matriks, m_norm, bobot, lambda_max, ci, ri, cr,
                                     judul=f"Analisis AHP – {mode_label}" if mode_label else "")
            st.pyplot(fig, use_container_width=True)
            chart_bytes = export_chart(fig)
            plt.close(fig)
        st.download_button(
            label="⬇️ Download Grafik (PNG)",
            data=chart_bytes,
            file_name=f"ahp_{mode_label.lower().replace(' ', '_')}_grafik.png" if mode_label else "ahp_grafik.png",
            mime="image/png"
        )

    with tab_matrix:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Matriks Perbandingan Berpasangan**")
            st.dataframe(pd.DataFrame(matriks.round(4), index=FAKTOR_KODE, columns=FAKTOR_KODE),
                         use_container_width=True)
        with col_b:
            st.markdown("**Matriks Ternormalisasi & Bobot**")
            df_norm = pd.DataFrame(m_norm.round(4), index=FAKTOR_KODE, columns=FAKTOR_KODE)
            df_norm['Bobot'] = bobot.round(4)
            df_norm['Bobot (%)'] = (bobot * 100).round(2)
            st.dataframe(df_norm, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ⬇️ Download Hasil")
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        excel_bytes = export_excel(matriks, m_norm, bobot, lambda_max, ci, ri, cr)
        fname = f"ahp_{mode_label.lower().replace(' ', '_')}.xlsx" if mode_label else "hasil_ahp.xlsx"
        st.download_button(
            label="📥 Download Excel (Lengkap)",
            data=excel_bytes,
            file_name=fname,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col_dl2:
        if cr <= 0.1:
            st.markdown('<div class="success-box">✓ Matriks perbandingan <strong>konsisten</strong>. Data dapat digunakan untuk penelitian.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warning-box">⚠️ CR > 0.10 → Tidak konsisten. Tinjau kembali penilaian perbandingan Anda.</div>', unsafe_allow_html=True)


def widget_input_matriks(prefix: str, default_form: np.ndarray = None):
    """
    Widget input matriks 5×5 dengan skala kuesioner 1-5 bipolar.
    Otomatis konversi ke nilai AHP dan isi reciprocal.

    Skala:
      1 = Kiri jauh lebih penting  → AHP 5
      2 = Kiri lebih penting       → AHP 3
      3 = Sama penting             → AHP 1
      4 = Kanan lebih penting      → AHP 1/3
      5 = Kanan jauh lebih penting → AHP 1/5
    """
    if default_form is None:
        default_form = np.full((N, N), 3)  # default semua = 3 (sama penting)

    st.markdown("""
    <div class="info-box">
    💡 <strong>Petunjuk pengisian:</strong><br>
    Pilih nilai 1–5 untuk setiap pasang faktor sesuai tingkat kepentingan.<br>
    <b>1</b> = Faktor <em>kiri</em> jauh lebih penting &nbsp;|&nbsp;
    <b>3</b> = Sama penting &nbsp;|&nbsp;
    <b>5</b> = Faktor <em>kanan</em> jauh lebih penting
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    matriks_ahp = np.ones((N, N))   # akan diisi nilai AHP hasil konversi
    matriks_form = np.full((N, N), 3, dtype=int)  # simpan jawaban form 1-5

    for i in range(N):
        for j in range(i + 1, N):
            key = f"{prefix}_m_{i}_{j}"
            default_val = int(round(default_form[i][j]))
            default_val = max(1, min(5, default_val))  # clamp 1-5

            label = (
                f"**{FAKTOR_KODE[i]}** ({FAKTOR_SHORT[i]}) "
                f"↔ **{FAKTOR_KODE[j]}** ({FAKTOR_SHORT[j]})"
            )
            sel = st.select_slider(
                label,
                options=FORM_LABELS,
                value=FORM_LABELS[default_val - 1],
                key=key
            )
            form_val = FORM_LABELS.index(sel) + 1   # 1–5
            ahp_val  = konversi_skala_form(form_val)

            matriks_form[i][j] = form_val
            matriks_form[j][i] = 6 - form_val        # cermin: 1↔5, 2↔4, 3↔3
            matriks_ahp[i][j]  = ahp_val
            matriks_ahp[j][i]  = 1.0 / ahp_val

    np.fill_diagonal(matriks_ahp, 1.0)
    np.fill_diagonal(matriks_form, 3)

    # Preview: tampilkan jawaban form DAN nilai AHP
    with st.expander("👁️ Preview Matriks (Jawaban Form & Nilai AHP)", expanded=False):
        col_f, col_a = st.columns(2)
        with col_f:
            st.markdown("**Jawaban Form (Skala 1–5)**")
            st.dataframe(
                pd.DataFrame(matriks_form, index=FAKTOR_KODE, columns=FAKTOR_KODE),
                use_container_width=True
            )
        with col_a:
            st.markdown("**Nilai AHP (setelah konversi)**")
            st.dataframe(
                pd.DataFrame(matriks_ahp.round(4), index=FAKTOR_KODE, columns=FAKTOR_KODE),
                use_container_width=True
            )

    return matriks_ahp


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR NAVIGASI
# ──────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px 0">
        <div style="font-size:2.5rem">📊</div>
        <div style="color:#F8FAFC;font-size:1.1rem;font-weight:700;margin-top:6px">AHP Analyzer</div>
        <div style="color:#64748B;font-size:0.75rem">Matla Islamic Academy</div>
    </div>
    <hr style="border-color:#334155;margin:12px 0 20px 0">
    """, unsafe_allow_html=True)

    menu = st.radio(
        "Navigasi",
        options=["🏠 Beranda", "📋 Mode 1: Input Agregasi", "👥 Mode 2: Multi-Responden", "📖 Panduan AHP"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <hr style="border-color:#334155;margin:20px 0 12px 0">
    <div style="color:#64748B;font-size:0.75rem;text-align:center">
        Metode: Analytical Hierarchy Process<br>Saaty (1980)
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# HALAMAN: BERANDA
# ──────────────────────────────────────────────────────────────────────────────

if menu == "🏠 Beranda":
    st.markdown("""
    <div class="hero-header">
        <h1>📊 Analisis AHP Kepuasan Pengguna</h1>
        <p>Sistem Informasi Dokumentasi & Arsip Digital Kampus Berbasis Web<br>
        <strong style="color:#60A5FA">Matla Islamic Academy</strong></p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="ahp-card" style="text-align:center">
            <div style="font-size:2rem">🎯</div>
            <div style="color:#60A5FA;font-weight:700;margin:8px 0 4px">5 Kriteria</div>
            <div style="color:#94A3B8;font-size:0.85rem">Faktor kepuasan pengguna yang dianalisis</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="ahp-card" style="text-align:center">
            <div style="font-size:2rem">⚖️</div>
            <div style="color:#A78BFA;font-weight:700;margin:8px 0 4px">Metode AHP</div>
            <div style="color:#94A3B8;font-size:0.85rem">Analytical Hierarchy Process (Saaty, 1980)</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="ahp-card" style="text-align:center">
            <div style="font-size:2rem">✅</div>
            <div style="color:#34D399;font-weight:700;margin:8px 0 4px">Uji Konsistensi</div>
            <div style="color:#94A3B8;font-size:0.85rem">CR ≤ 0.10 → hasil valid & dapat digunakan</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="ahp-card">
        <h3 style="color:#F8FAFC;margin-top:0">📌 Faktor yang Dianalisis</h3>""", unsafe_allow_html=True)

    for i, (kode, nama) in enumerate(zip(FAKTOR_KODE, FAKTOR_SHORT)):
        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:10px 0;border-bottom:1px solid #334155">
            <span style="background:{WARNA[i]};color:white;padding:4px 10px;border-radius:6px;
                         font-weight:700;font-size:0.85rem;margin-right:14px">{kode}</span>
            <span style="color:#F8FAFC;font-weight:500">{nama}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="ahp-card">
        <h3 style="color:#F8FAFC;margin-top:0">🚀 Cara Penggunaan</h3>
        <ol style="color:#94A3B8;line-height:2">
            <li><strong style="color:#F8FAFC">Mode 1 – Input Agregasi</strong>: Langsung input matriks perbandingan yang sudah dirata-rata dari semua responden, atau upload Excel.</li>
            <li><strong style="color:#F8FAFC">Mode 2 – Multi-Responden</strong>: Input matriks per responden secara terpisah, lalu sistem menghitung rata-rata geometrik otomatis.</li>
        </ol>
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# HALAMAN: MODE 1 – INPUT AGREGASI
# ──────────────────────────────────────────────────────────────────────────────

elif menu == "📋 Mode 1: Input Agregasi":
    st.markdown('<div class="hero-header"><h1>📋 Mode 1: Matriks Agregasi</h1><p>Input satu matriks perbandingan (sudah dirata-rata dari semua responden)</p></div>', unsafe_allow_html=True)

    # Pilihan cara input
    cara_input = st.radio(
        "Pilih cara input data:",
        ["✏️ Input Manual (Slider)", "📤 Upload File Excel"],
        horizontal=True
    )

    matriks_input = None

    if cara_input == "✏️ Input Manual (Slider)":
        st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
        st.markdown("### 🔢 Input Matriks Perbandingan Berpasangan")

        # Preset demo: nilai form 1-5 (bukan Saaty langsung)
        if st.checkbox("Gunakan data contoh (untuk demo)"):
            # Matriks dalam skala form 1-5 (akan dikonversi)
            # 1=kiri jauh lebih penting, 3=sama, 5=kanan jauh lebih penting
            default_m = np.array([
                # K1  K2  K3  K4  K5
                [3,   2,  1,  2,  1],   # K1: Kemudahan Penggunaan
                [4,   3,  2,  4,  2],   # K2: Kelengkapan Fitur (cermin diisi otomatis)
                [5,   4,  3,  5,  4],   # K3: Kecepatan Akses
                [4,   2,  1,  3,  2],   # K4: Keamanan Data
                [5,   4,  2,  4,  3],   # K5: Kemudahan Pencarian Arsip
            ], dtype=float)
        else:
            default_m = np.full((N, N), 3, dtype=float)  # semua sama penting

        matriks_input = widget_input_matriks("mode1", default_m)
        st.markdown('</div>', unsafe_allow_html=True)

    else:  # Upload Excel
        st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload File Excel")
        st.markdown("""<div class="info-box">
            Format Excel: Sheet pertama berisi matriks 5×5 dengan nilai perbandingan.
            Baris dan kolom sesuai urutan: K1, K2, K3, K4, K5.<br>
            <strong>Contoh file</strong>: <code>template_kuesioner_ahp.xlsx</code> yang sudah ada di folder proyek.
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        uploaded = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx", "xls"])
        if uploaded:
            try:
                df_upload = pd.read_excel(uploaded, index_col=0, header=0)
                if df_upload.shape == (N, N):
                    raw = df_upload.values.astype(float)
                    # Deteksi apakah data dalam skala form 1-5 atau sudah AHP
                    is_form_scale = bool(np.all((raw >= 1) & (raw <= 5)) and np.any(raw > 1.5))
                    if is_form_scale:
                        matriks_input = konversi_matriks_form(raw)
                        st.success("✅ File berhasil dibaca dan dikonversi dari skala form 1–5 ke nilai AHP!")
                    else:
                        matriks_input = raw
                        st.success("✅ File berhasil dibaca (diasumsikan sudah dalam skala AHP Saaty).")
                    st.dataframe(df_upload.round(4), use_container_width=True)
                    with st.expander("📊 Matriks AHP (setelah konversi)"):
                        st.dataframe(
                            pd.DataFrame(matriks_input.round(4),
                                         index=FAKTOR_KODE, columns=FAKTOR_KODE),
                            use_container_width=True
                        )
                else:
                    st.error(f"❌ Ukuran matriks harus {N}×{N}. File yang diupload: {df_upload.shape[0]}×{df_upload.shape[1]}")
            except Exception as e:
                st.error(f"❌ Gagal membaca file: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Hitung
    if matriks_input is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Hitung AHP Sekarang", use_container_width=True):
            with st.spinner("Menghitung AHP..."):
                m, m_norm, bobot, lmax, ci, ri, cr = hitung_ahp(matriks_input)
            st.markdown("---")
            st.markdown("## 📊 Hasil Analisis AHP")
            tampil_hasil(m, m_norm, bobot, lmax, ci, ri, cr, "Agregasi")

# ──────────────────────────────────────────────────────────────────────────────
# HALAMAN: MODE 2 – MULTI-RESPONDEN
# ──────────────────────────────────────────────────────────────────────────────

elif menu == "👥 Mode 2: Multi-Responden":
    st.markdown('<div class="hero-header"><h1>👥 Mode 2: Multi-Responden</h1><p>Input matriks per responden → agregasi otomatis dengan rata-rata geometrik</p></div>', unsafe_allow_html=True)

    # Inisialisasi state
    if 'n_responden' not in st.session_state:
        st.session_state.n_responden = 3
    if 'nama_responden' not in st.session_state:
        st.session_state.nama_responden = [f"Responden {i+1}" for i in range(10)]

    # Kontrol jumlah responden
    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Pengaturan Responden")
    col_r1, col_r2 = st.columns([1, 2])
    with col_r1:
        n_resp = st.number_input("Jumlah Responden", min_value=1, max_value=10,
                                  value=st.session_state.n_responden, step=1)
        st.session_state.n_responden = int(n_resp)
    with col_r2:
        st.markdown('<div class="info-box">Minimal 1 responden. Semakin banyak responden, semakin representatif hasil analisis.</div>', unsafe_allow_html=True)

    # Input nama responden
    st.markdown("**Nama Responden:**")
    cols_nama = st.columns(min(n_resp, 5))
    for i in range(n_resp):
        with cols_nama[i % 5]:
            st.session_state.nama_responden[i] = st.text_input(
                f"Nama #{i+1}", value=st.session_state.nama_responden[i],
                key=f"nama_resp_{i}", label_visibility="collapsed",
                placeholder=f"Nama Responden {i+1}"
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # Pilihan cara input
    cara_input_multi = st.radio(
        "Pilih cara input data per responden:",
        ["✏️ Input Manual (Slider)", "📤 Upload File Excel per Responden"],
        horizontal=True
    )

    list_matriks = []
    list_nama = []
    semua_valid = True

    if cara_input_multi == "✏️ Input Manual (Slider)":
        # Tab per responden
        tab_labels = [st.session_state.nama_responden[i] or f"Resp {i+1}" for i in range(n_resp)]
        tabs = st.tabs(tab_labels)

        CONTOH_MATRIKS = [
            np.array([[1,3,5,2,4],[1/3,1,3,1/2,2],[1/5,1/3,1,1/4,1/2],[1/2,2,4,1,3],[1/4,1/2,2,1/3,1]]),
            np.array([[1,4,6,3,5],[1/4,1,3,1/2,2],[1/6,1/3,1,1/5,1/3],[1/3,2,5,1,3],[1/5,1/2,3,1/3,1]]),
            np.array([[1,3,4,2,4],[1/3,1,2,1/2,2],[1/4,1/2,1,1/3,1],[1/2,2,3,1,3],[1/4,1/2,1,1/3,1]]),
        ]

        for i, tab in enumerate(tabs):
            with tab:
                st.markdown(f'<div class="ahp-card">', unsafe_allow_html=True)
                nama = st.session_state.nama_responden[i] or f"Responden {i+1}"
                st.markdown(f"#### Input Matriks – {nama}")

                use_contoh = st.checkbox(f"Gunakan data contoh", key=f"contoh_resp_{i}")
                default_m = CONTOH_MATRIKS[i % len(CONTOH_MATRIKS)] if use_contoh else np.ones((N, N))

                m = widget_input_matriks(f"resp{i}", default_m)
                list_matriks.append(enforce_reciprocal(m))
                list_nama.append(nama)
                st.markdown('</div>', unsafe_allow_html=True)

    else:  # Upload Excel per responden
        st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
        st.markdown("### 📤 Upload File Excel per Responden")
        st.markdown("""<div class="info-box">Upload satu file Excel per responden. Setiap file berisi matriks 5×5 perbandingan berpasangan.</div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for i in range(n_resp):
            nama = st.session_state.nama_responden[i] or f"Responden {i+1}"
            up = st.file_uploader(f"Upload Excel – {nama}", type=["xlsx", "xls"], key=f"upload_resp_{i}")
            if up:
                try:
                    df_up = pd.read_excel(up, index_col=0, header=0)
                    if df_up.shape == (N, N):
                        m = enforce_reciprocal(df_up.values.astype(float))
                        list_matriks.append(m)
                        list_nama.append(nama)
                        st.success(f"✅ {nama}: File berhasil dibaca")
                    else:
                        st.error(f"❌ {nama}: Ukuran matriks harus {N}×{N}")
                        semua_valid = False
                except Exception as e:
                    st.error(f"❌ {nama}: Gagal baca file – {e}")
                    semua_valid = False
            else:
                if cara_input_multi == "📤 Upload File Excel per Responden":
                    semua_valid = False
        st.markdown('</div>', unsafe_allow_html=True)

    # Hitung
    st.markdown("<br>", unsafe_allow_html=True)
    hitung_btn = st.button("⚡ Agregasi & Hitung AHP", use_container_width=True,
                            disabled=(len(list_matriks) == 0))

    if hitung_btn and len(list_matriks) > 0:
        with st.spinner("Mengagregasi dan menghitung AHP..."):
            matriks_agg = agregasi_geometric_mean(list_matriks)
            m, m_norm, bobot, lmax, ci, ri, cr = hitung_ahp(matriks_agg)

        st.success(f"✅ Berhasil mengagregasi {len(list_matriks)} responden menggunakan rata-rata geometrik.")

        st.markdown("---")
        st.markdown("## 📊 Hasil Analisis AHP Multi-Responden")
        tampil_hasil(m, m_norm, bobot, lmax, ci, ri, cr, "Multi Responden")

        # Heatmap per responden
        if len(list_matriks) > 0:
            st.markdown("---")
            st.markdown("### 🔥 Heatmap Matriks Per Responden")
            with st.spinner("Membuat heatmap per responden..."):
                fig_resp = buat_chart_per_responden(list_matriks, list_nama)
                st.pyplot(fig_resp, use_container_width=True)
                chart_bytes = export_chart(fig_resp)
                plt.close(fig_resp)
            st.download_button(
                "⬇️ Download Heatmap Per Responden (PNG)",
                data=chart_bytes,
                file_name="ahp_per_responden.png",
                mime="image/png"
            )

# ──────────────────────────────────────────────────────────────────────────────
# HALAMAN: PANDUAN AHP
# ──────────────────────────────────────────────────────────────────────────────

elif menu == "📖 Panduan AHP":
    st.markdown('<div class="hero-header"><h1>📖 Panduan Metode AHP</h1><p>Analytical Hierarchy Process – Saaty (1980)</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### Apa itu AHP?")
    st.markdown("""
    **Analytical Hierarchy Process (AHP)** adalah metode pengambilan keputusan multi-kriteria yang dikembangkan oleh **Thomas L. Saaty (1980)**. 
    Metode ini membantu menentukan prioritas faktor berdasarkan perbandingan berpasangan (*pairwise comparison*).
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Skala Kuesioner yang Digunakan (Skala 1–5 Bipolar)")
    st.markdown("""
    Kuesioner menggunakan **skala 1–5 bipolar** yang disederhanakan dari skala Saaty 1–9,
    agar lebih mudah diisi oleh responden. Nilai **3** di tengah berarti sama penting;
    semakin ke **1** artinya faktor kiri lebih penting, semakin ke **5** artinya faktor kanan lebih penting.
    """)
    df_skala_form = pd.DataFrame({
        'Nilai Kuesioner': [1, 2, 3, 4, 5],
        'Arti': [
            'Faktor KIRI jauh lebih penting',
            'Faktor KIRI lebih penting',
            'Kedua faktor sama penting',
            'Faktor KANAN lebih penting',
            'Faktor KANAN jauh lebih penting',
        ],
        'Nilai AHP (a_ij)': ['5', '3', '1', '1/3 ≈ 0.333', '1/5 = 0.200'],
        'Nilai Reciprocal (a_ji)': ['1/5 = 0.200', '1/3 ≈ 0.333', '1', '3', '5'],
    })
    st.dataframe(df_skala_form, use_container_width=True, hide_index=True)
    st.markdown("""
    <div class="info-box">
    💡 <strong>Contoh pengisian kuesioner:</strong><br>
    <em>Kemudahan Penggunaan ↔ Keamanan Data</em> → jawab <strong>2</strong> artinya
    "Kemudahan Penggunaan lebih penting" → sistem otomatis menggunakan nilai AHP = <strong>3</strong>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### 🔄 Proses Konversi Otomatis")
    st.markdown("""
    Sistem secara otomatis mengkonversi jawaban kuesioner ke nilai AHP yang benar:

    | Langkah | Proses |
    |---------|--------|
    | 1️⃣ | Responden mengisi kuesioner skala **1–5** |
    | 2️⃣ | Sistem konversi ke nilai **AHP Saaty** sesuai tabel di atas |
    | 3️⃣ | Nilai reciprocal diisi otomatis: *a_ji = 1 / a_ij* |
    | 4️⃣ | Jika multi-responden: agregasi dengan **rata-rata geometrik** |
    | 5️⃣ | Hitung **bobot prioritas** dan **uji konsistensi (CR)** |
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### 📐 Tahapan Perhitungan AHP")
    st.markdown("""
    1. **Bangun Matriks Perbandingan Berpasangan** — hasil konversi dari jawaban kuesioner 1–5
    2. **Normalisasi Matriks** — setiap elemen dibagi jumlah kolomnya
    3. **Hitung Vektor Prioritas (Bobot)** — rata-rata setiap baris dari matriks ternormalisasi
    4. **Uji Konsistensi**:
       - λmax = rata-rata dari *(Aw)ᵢ / wᵢ*
       - CI = *(λmax – n) / (n – 1)*
       - CR = *CI / RI*
       - ✅ **CR ≤ 0.10 → Konsisten** (data valid untuk penelitian)
       - ❌ **CR > 0.10 → Tidak Konsisten** (perlu ditinjau ulang oleh responden)
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Random Index (RI) – Saaty (1980)")
    df_ri = pd.DataFrame({
        'n (Jumlah Kriteria)': list(RI_TABLE.keys()),
        'Random Index (RI)': list(RI_TABLE.values())
    })
    st.dataframe(df_ri, use_container_width=True, hide_index=True)
    st.markdown("""
    <div class="info-box">
    Penelitian ini menggunakan <strong>n = 5 kriteria</strong>, sehingga RI = <strong>1.12</strong>.
    Batas konsistensi yang diterima adalah CR ≤ 0.10.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### 📌 Faktor yang Dianalisis")
    for i, (kode, nama) in enumerate(zip(FAKTOR_KODE, FAKTOR_SHORT)):
        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:10px 0;border-bottom:1px solid #334155">
            <span style="background:{WARNA[i]};color:white;padding:4px 12px;border-radius:6px;
                         font-weight:700;font-size:0.85rem;margin-right:14px;min-width:36px;text-align:center">{kode}</span>
            <span style="color:#F8FAFC;font-weight:500">{nama}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ahp-card">', unsafe_allow_html=True)
    st.markdown("### ℹ️ Referensi")
    st.markdown("""
    - Saaty, T. L. (1980). *The Analytic Hierarchy Process*. McGraw-Hill.
    - Saaty, T. L. (1990). *How to make a decision: The Analytic Hierarchy Process*. European Journal of Operational Research, 48(1), 9–26.
    - Forman, E. H., & Gass, S. I. (2001). The Analytic Hierarchy Process — An Exposition. *Operations Research*, 49(4), 469–486.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
