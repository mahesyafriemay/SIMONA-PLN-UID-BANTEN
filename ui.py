"""
Komponen UI bersama untuk semua halaman SIMONA — logo, font kustom, topbar,
dan hero section bergaya website resmi PLN/Danantara.
"""

import streamlit as st
import base64
from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets"


@st.cache_data(show_spinner=False)
def _load_logo_b64(filename: str) -> str:
    path = ASSETS_DIR / filename
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


def get_favicon():
    """Path ke logo PLN untuk dipakai sebagai favicon tab browser."""
    path = ASSETS_DIR / "logo_pln.png"
    return str(path) if path.exists() else None


def inject_global_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        h1, h2, h3, h4, .simona-brand-name, .simona-hero-title {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* hilangkan padding atas bawaan streamlit supaya topbar full-bleed */
        .block-container { padding-top: 0 !important; }

        /* ---- topbar nav ala website resmi ---- */
        .simona-topbar {
            display: flex; align-items: center; justify-content: space-between;
            padding: 14px 28px; margin: -1rem -1rem 1.75rem -1rem;
            background: #FFFFFF;
            border-bottom: 1px solid #E7ECF5;
            box-shadow: 0 1px 4px rgba(16,24,40,0.04);
        }
        .simona-topbar-brand { display: flex; align-items: center; gap: 12px; }
        .simona-topbar-brand img { height: 30px; object-fit: contain; }
        .simona-topbar-divider { width: 1px; height: 24px; background: #DCE2EE; }
        .simona-brand-name { color: #0B3D91; font-size: 1.05rem; font-weight: 700; margin: 0; letter-spacing: 0.2px; }
        .simona-brand-sub { color: #8891A3; font-size: 0.72rem; font-weight: 500; margin: 0; }
        .simona-topbar-right img { height: 30px; object-fit: contain; }

        /* ---- hero section (halaman login) ---- */
        .simona-hero {
            position: relative; overflow: hidden;
            margin: 0 -1rem 1.75rem -1rem; padding: 44px 48px 52px 48px;
            background: radial-gradient(circle at 15% 20%, #144EA8 0%, #0B3D91 45%, #072659 100%);
            border-radius: 0 0 28px 28px;
        }
        .simona-hero::before {
            content: ""; position: absolute; inset: 0;
            background-image:
                radial-gradient(circle at 85% 15%, rgba(41,182,246,0.22) 0%, transparent 45%),
                radial-gradient(circle at 30% 95%, rgba(255,196,0,0.10) 0%, transparent 40%),
                repeating-linear-gradient(115deg, rgba(255,255,255,0.025) 0px, rgba(255,255,255,0.025) 1px, transparent 1px, transparent 64px);
            pointer-events: none;
        }
        .simona-hero-grid {
            position: relative; display: flex; align-items: center; justify-content: space-between;
            gap: 32px; margin-top: 36px; flex-wrap: wrap;
        }
        .simona-hero-left { flex: 1 1 480px; min-width: 320px; }
        .simona-hero-right { flex: 0 1 360px; min-width: 300px; display: flex; justify-content: center; }
        .simona-hero-card-wrap {
            transform: rotate(-2deg); filter: drop-shadow(0 18px 34px rgba(3,20,55,0.45));
            transition: transform 0.25s ease;
        }
        .simona-hero-badge {
            position: relative; display: inline-block; background: rgba(255,255,255,0.12);
            color: #E8F0FF; padding: 6px 14px; border-radius: 999px; font-size: 0.78rem;
            font-weight: 600; margin-bottom: 18px; border: 1px solid rgba(255,255,255,0.25);
            backdrop-filter: blur(4px);
        }
        .simona-hero-title {
            position: relative; color: #FFFFFF; font-size: 2.5rem; font-weight: 800;
            line-height: 1.15; margin: 0 0 14px 0;
        }
        .simona-hero-title .accent { color: #6FD3FF; }
        .simona-hero-subtitle {
            position: relative; color: rgba(255,255,255,0.82); font-size: 1.0rem;
            font-weight: 400; max-width: 560px; line-height: 1.55; margin-bottom: 20px;
        }
        .simona-hero-chips { display: flex; gap: 10px; flex-wrap: wrap; }
        .simona-hero-chip {
            background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18);
            color: #E8F0FF; font-size: 0.78rem; font-weight: 600;
            padding: 6px 13px; border-radius: 999px; backdrop-filter: blur(4px);
        }

        /* ---- generic ---- */
        .simona-subtitle { color: #5B6478; font-size: 0.97rem; margin-bottom: 1.1rem; font-weight: 400; }
        div[data-testid="stMetric"] {
            background: #FFFFFF;
            border-radius: 14px; padding: 16px 18px; border: 1px solid #E7ECF5;
            box-shadow: 0 1px 3px rgba(16,24,40,0.04);
        }
        div[data-testid="stMetricLabel"] { font-weight: 600; color: #475066; }
        div[data-testid="stMetricValue"] { font-family: 'Plus Jakarta Sans', sans-serif; color: #0B3D91; }

        .status-badge {
            display: inline-block; background: #EEF4FF; color: #0F62D6;
            padding: 4px 12px; border-radius: 999px; font-size: 0.76rem; font-weight: 600;
            margin-bottom: 1rem; border: 1px solid #D6E4FA;
        }

        .stTabs [data-baseweb="tab-list"] { gap: 4px; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0; font-weight: 600; color: #5B6478;
        }
        .stTabs [aria-selected="true"] { color: #0F62D6 !important; }
        [data-baseweb="tab-highlight"] { background-color: #0F62D6 !important; }
        [data-baseweb="tab-border"] { background-color: #E7ECF5 !important; }

        div[data-testid="stExpander"] {
            border: 1px solid #E7ECF5; border-radius: 12px;
        }

        section[data-testid="stSidebar"] { background: #F7F9FC; }

        /* ---- nav sidebar (st.navigation) ala Material Design ---- */
        [data-testid="stSidebarNav"] { padding-top: 8px; }
        [data-testid="stSidebarNav"] ul { padding: 0 10px; }
        [data-testid="stSidebarNav"] a {
            border-radius: 10px; padding: 9px 14px; margin: 2px 0;
            font-weight: 500; color: #37415A; transition: background 0.15s ease;
        }
        [data-testid="stSidebarNav"] a:hover { background: #E9EFFC; }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: #0F62D6; color: #FFFFFF !important; font-weight: 600;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] span { color: #FFFFFF !important; }

        .sidebar-profile {
            background: #FFFFFF; border: 1px solid #E7ECF5; border-radius: 12px;
            padding: 12px 14px; margin: 10px 0 8px 0;
        }
        .sidebar-profile-name { margin: 0; font-weight: 700; color: #1A1F36; font-size: 0.92rem; }
        .sidebar-profile-meta { margin: 2px 0 0 0; color: #7A8399; font-size: 0.78rem; }

        button[kind="primary"] {
            background: #0F62D6 !important; border-radius: 8px !important;
            font-weight: 600 !important;
        }
        div.stButton > button {
            border-radius: 8px !important; font-weight: 500 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_profile():
    """Kartu profil user + tombol logout, ditampilkan di bawah menu navigasi sidebar."""
    role = st.session_state.get("role")
    fullname = st.session_state.get("fullname")
    unit_name = st.session_state.get("unit_name")

    with st.sidebar:
        st.markdown('<div class="sidebar-profile">'
                    f'<p class="sidebar-profile-name">{fullname}</p>'
                    f'<p class="sidebar-profile-meta">{role} &middot; {unit_name}</p>'
                    '</div>', unsafe_allow_html=True)
        if st.button("Ganti Role / Logout", use_container_width=True, key="logout_btn"):
            for k in ["role", "unit_id", "unit_name", "fullname", "is_authenticated"]:
                st.session_state.pop(k, None)
            st.rerun()


def render_topbar():
    """Topbar tipis untuk semua halaman internal (bukan halaman hero)."""
    pln_b64 = _load_logo_b64("logo_pln.png")
    dan_b64 = _load_logo_b64("logo_danantara.png")

    left_logo = f'<img src="data:image/png;base64,{dan_b64}" alt="Danantara Indonesia">' if dan_b64 else ""
    right_logo = f'<img src="data:image/png;base64,{pln_b64}" alt="PLN">' if pln_b64 else ""

    st.markdown(f"""
    <div class="simona-topbar">
        <div class="simona-topbar-brand">
            {left_logo}
            <div class="simona-topbar-divider"></div>
            <div>
                <p class="simona-brand-name">SIMONA</p>
                <p class="simona-brand-sub">Maturity Level Gudang Distribusi — UID Banten</p>
            </div>
        </div>
        <div class="simona-topbar-right">{right_logo}</div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(badge_text: str, title_html: str, subtitle: str):
    """Hero section besar untuk halaman login, bergaya website resmi PLN."""
    pln_b64 = _load_logo_b64("logo_pln.png")
    dan_b64 = _load_logo_b64("logo_danantara.png")

    left_logo = (
        f'<img src="data:image/png;base64,{dan_b64}" alt="Danantara Indonesia" '
        f'style="filter:invert(1) brightness(1.6);">'
    ) if dan_b64 else ""
    right_logo = f'<img src="data:image/png;base64,{pln_b64}" alt="PLN">' if pln_b64 else ""

    preview_card = """
    <div class="simona-hero-card-wrap">
      <svg width="340" height="270" viewBox="0 0 340 270" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="340" height="270" rx="20" fill="#FFFFFF"/>
        <text x="24" y="34" font-family="Plus Jakarta Sans, Inter, sans-serif" font-size="13" font-weight="700" fill="#0B3D91">Ringkasan Maturity Level</text>
        <text x="24" y="52" font-family="Inter, sans-serif" font-size="10" fill="#8891A3">UID Banten · Juni 2026</text>
        <line x1="24" y1="64" x2="316" y2="64" stroke="#EEF1F7" stroke-width="1"/>

        <g transform="translate(92,168)">
          <circle r="54" fill="none" stroke="#EEF1F7" stroke-width="14"/>
          <circle r="54" fill="none" stroke="#0F62D6" stroke-width="14"
            stroke-dasharray="305 339" stroke-linecap="round" transform="rotate(-90)"/>
          <text text-anchor="middle" y="4" font-family="Plus Jakarta Sans, sans-serif" font-size="28" font-weight="800" fill="#0B3D91">4.5</text>
          <text text-anchor="middle" y="24" font-family="Inter, sans-serif" font-size="10" fill="#8891A3">Matlev / 5</text>
        </g>

        <g font-family="Inter, sans-serif" font-size="10" fill="#37415A">
          <text x="182" y="100">Tata Kelola</text>
          <rect x="182" y="106" width="132" height="7" rx="3.5" fill="#EEF1F7"/>
          <rect x="182" y="106" width="124" height="7" rx="3.5" fill="#0F62D6"/>

          <text x="182" y="132">Kinerja</text>
          <rect x="182" y="138" width="132" height="7" rx="3.5" fill="#EEF1F7"/>
          <rect x="182" y="138" width="99" height="7" rx="3.5" fill="#29B6F6"/>

          <text x="182" y="164">Infrastruktur</text>
          <rect x="182" y="170" width="132" height="7" rx="3.5" fill="#EEF1F7"/>
          <rect x="182" y="170" width="128" height="7" rx="3.5" fill="#0F62D6"/>

          <text x="182" y="196">SDM</text>
          <rect x="182" y="202" width="132" height="7" rx="3.5" fill="#EEF1F7"/>
          <rect x="182" y="202" width="119" height="7" rx="3.5" fill="#29B6F6"/>
        </g>

        <rect x="16" y="232" width="308" height="1" fill="#EEF1F7"/>
        <circle cx="30" cy="250" r="4" fill="#22C55E"/>
        <text x="42" y="254" font-family="Inter, sans-serif" font-size="10" fill="#37415A">7 unit sudah dinilai · data real</text>
      </svg>
    </div>
    """

    st.html(f"""
    <div class="simona-hero">
        <div class="simona-topbar-brand">
            {left_logo}
            <div class="simona-topbar-divider" style="background: rgba(255,255,255,0.3);"></div>
            {right_logo}
        </div>
        <div class="simona-hero-grid">
            <div class="simona-hero-left">
                <div class="simona-hero-badge">SIMONA — Sistem Monitoring &amp; Self Assessment Unit PLN</div>
                <p class="simona-hero-title">{title_html}</p>
                <p class="simona-hero-subtitle">{subtitle}</p>
                <div class="simona-hero-chips">
                    <span class="simona-hero-chip">7 Unit Gudang</span>
                    <span class="simona-hero-chip">29 Indikator</span>
                    <span class="simona-hero-chip">6 Aspek Penilaian</span>
                    <span class="simona-hero-chip">Real-time Monitoring</span>
                </div>
            </div>
            <div class="simona-hero-right">
                {preview_card}
            </div>
        </div>
    </div>
    """)
