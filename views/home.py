import streamlit as st
from data import get_units, reset_demo_data
from ui import render_topbar, render_hero, render_sidebar_profile


def render_role_picker():
    render_hero(
        badge_text="SIMONA",
        title_html='Kelola Maturity Level Gudang Distribusi <span class="accent">Secara Presisi</span>',
        subtitle=(
            "Self-assessment digital untuk seluruh unit gudang distribusi PLN UID Banten — "
            "menggantikan penilaian manual berbasis Excel dengan sistem yang terukur, "
            "terpusat, dan dapat dipantau secara real-time."
        ),
    )

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("#### Masuk ke SIMONA")
            st.caption("Prototipe — pilih role & unit untuk mencoba aplikasinya. Data Juni 2026 sudah terisi data real.")

            role = st.selectbox("Role", ["UID", "UP3", "ULP"])

            units_df = get_units(unit_type=role)
            if role == "UID":
                unit_row = units_df.iloc[0]
                st.caption(f"Login sebagai UID: **{unit_row['name']}**")
            else:
                label = "Unit (Gudang UP3)" if role == "UP3" else "Unit (ULP)"
                unit_name = st.selectbox(label, sorted(units_df["name"].tolist()))
                unit_row = units_df[units_df["name"] == unit_name].iloc[0]

            fullname = st.text_input("Nama (bebas, untuk ditampilkan saja)", value=f"Admin {role}")

            if st.button("Masuk", type="primary", use_container_width=True):
                st.session_state["role"] = role
                st.session_state["unit_id"] = unit_row["id"]
                st.session_state["unit_name"] = unit_row["name"]
                st.session_state["fullname"] = fullname
                st.session_state["is_authenticated"] = True
                st.rerun()

            st.divider()
            if st.button("Reset semua data demo ke kondisi awal", use_container_width=True):
                reset_demo_data()
                st.success("Data demo direset ke data Juni 2026 real + Juli 2026 kosong.")
                st.rerun()

    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("**6 Aspek Penilaian**")
            st.caption("SDM, Anggaran, Tata Kelola, Infrastruktur, Peralatan Operasional, dan Kinerja — sesuai standar resmi.")
    with c2:
        with st.container(border=True):
            st.markdown("**29 Indikator Terukur**")
            st.caption("Tiap indikator punya rubrik kriteria Level 1-5 yang jelas, bukan penilaian subjektif.")
    with c3:
        with st.container(border=True):
            st.markdown("**Data Juni 2026 Real**")
            st.caption("7 unit UP3 sudah terisi hasil penilaian aktual untuk langsung dicoba di Dashboard.")


def render_home():
    render_topbar()
    render_sidebar_profile()

    role = st.session_state.get("role")
    fullname = st.session_state.get("fullname")
    unit_name = st.session_state.get("unit_name")

    st.success(f"Selamat datang, **{fullname}** ({role} - {unit_name}).")
    st.info(
        "Gunakan menu di sidebar kiri: **Dashboard**, **Assessment**, "
        "**Review** (khusus UID), **Master Data** (khusus UID), dan **Notifikasi**."
    )

    st.markdown("#### Ringkasan Peran Kamu")
    if role == "UID":
        st.write("Kelola periode, aspek, indikator & bobot aspek. Review dan approve assessment dari seluruh unit gudang UP3.")
    else:
        st.write("Isi self-assessment maturity level gudang bulanan, upload evidence, simpan draft, submit, dan pantau catatan revisi dari UID.")

    st.markdown("---")
    st.markdown("#### Formula Penilaian")
    st.latex(r"Nilai = \sum \frac{Level}{5} \times \frac{Bobot\ Aspek}{Jumlah\ Indikator\ dalam\ Aspek}")
    st.caption("Maturity Level (Matlev) = Nilai Total ÷ 20 (skala 1-5). Data Juni 2026 sudah terisi dari hasil penilaian real.")


if not st.session_state.get("is_authenticated"):
    render_role_picker()
else:
    render_home()
