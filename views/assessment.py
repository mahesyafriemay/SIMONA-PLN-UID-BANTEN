import streamlit as st
from data import (
    init_demo_data, get_periods, get_aspects, get_indicators, get_assessment,
    save_draft, submit_unit_assessments, add_evidence, get_aspect_weight,
)
from ui import inject_global_style, render_topbar, render_sidebar_profile

init_demo_data()
inject_global_style()
render_topbar()
render_sidebar_profile()

if not st.session_state.get("is_authenticated"):
    st.warning("Silakan masuk terlebih dahulu di halaman utama.")
    st.stop()

role = st.session_state["role"]
if role not in ("UP3", "ULP"):
    st.error("Halaman ini khusus untuk role UP3/ULP (unit gudang). UID tidak input nilai, hanya me-review.")
    st.stop()

unit_id = st.session_state["unit_id"]
fullname = st.session_state["fullname"]

st.title("Self Assessment Maturity Level Gudang")

periods_df = get_periods().copy()
periods_df["label"] = periods_df.apply(lambda r: f"{r['month']:02d}/{r['year']} ({r['status']})", axis=1)
selected_label = st.selectbox("Pilih Periode", periods_df["label"].tolist())
period_row = periods_df[periods_df["label"] == selected_label].iloc[0]
period_id = period_row["id"]

if period_row["status"] == "LOCKED":
    st.warning(
        "Periode ini sudah **LOCKED** — data di bawah bersifat read-only "
        "(tidak bisa diedit lagi, sudah final)."
    )

st.caption(
    "Geser slider untuk pilih **Level 1-5** tiap indikator sesuai kondisi gudang saat ini, baca kriterianya di bawah slider. "
    "Simpan Draft untuk menyimpan tanpa mengirim, atau Submit ketika seluruh indikator sudah lengkap."
)

aspects_df = get_aspects()
any_locked_for_edit = False
is_period_locked = period_row["status"] == "LOCKED"

for _, aspect in aspects_df.iterrows():
    indicators = get_indicators(aspect["id"])
    if not indicators:
        continue
    bobot_aspek = get_aspect_weight(period_id, aspect["id"])
    with st.expander(f"{aspect['name']} · bobot {bobot_aspek}", expanded=not is_period_locked):
        for ind in indicators:
            existing = get_assessment(unit_id, period_id, ind["id"]) or {}
            current_level = existing.get("level") or 1
            current_notes = existing.get("notes", "")
            current_status = existing.get("status", "DRAFT")
            is_locked = is_period_locked or current_status in ("SUBMITTED", "IN_REVIEW", "APPROVED")
            if is_locked:
                any_locked_for_edit = True

            st.markdown(f"**{ind['name']}** &nbsp; status: `{current_status}`")

            col1, col2 = st.columns([2, 3])
            with col1:
                selected_level = st.select_slider(
                    "Level", options=[1, 2, 3, 4, 5], value=current_level,
                    key=f"level_{ind['id']}_{period_id}", disabled=is_locked,
                )
                level_map = {lv["level"]: lv["level_label"] for lv in ind["levels"]}
                st.info(f"**Level {selected_level}:** {level_map.get(selected_level, '-')}")
            with col2:
                notes = st.text_area("Catatan", value=current_notes, key=f"notes_{ind['id']}_{period_id}",
                                      disabled=is_locked, height=100)

            if not is_locked:
                if st.button("Simpan Draft", key=f"save_{ind['id']}_{period_id}"):
                    save_draft(unit_id, period_id, ind["id"], selected_level, notes, fullname)
                    st.success("Tersimpan.")
                    st.rerun()

            st.markdown("_Evidence:_")
            evidences = existing.get("evidences", [])
            if evidences:
                for idx, ev in enumerate(evidences):
                    c1, c2 = st.columns([4, 1])
                    c1.write(f"{ev['filename']} — diupload {ev['uploaded_at'].strftime('%d/%m/%Y %H:%M')}")
                    if ev.get("file_bytes"):
                        c2.download_button(
                            "Download", data=ev["file_bytes"], file_name=ev["filename"],
                            mime=ev.get("mime_type") or "application/octet-stream",
                            key=f"dl_{ind['id']}_{period_id}_{idx}",
                        )
            else:
                st.caption("Belum ada evidence.")

            if not is_locked:
                uploaded_file = st.file_uploader(
                    "Upload evidence baru",
                    type=["pdf", "png", "jpg", "jpeg", "xlsx", "xls", "docx", "doc"],
                    key=f"upload_{ind['id']}_{period_id}",
                )
                if uploaded_file is not None:
                    if st.button("Upload", key=f"upload_btn_{ind['id']}_{period_id}"):
                        add_evidence(
                            unit_id, period_id, ind["id"], uploaded_file.name, fullname,
                            file_bytes=uploaded_file.getvalue(), mime_type=uploaded_file.type,
                        )
                        st.success("Evidence terupload.")
                        st.rerun()

            st.divider()

if not is_period_locked:
    st.markdown("### Kirim Assessment")
    if any_locked_for_edit:
        st.info("Beberapa indikator sudah SUBMITTED/APPROVED sehingga tidak bisa diedit lagi.")

    if st.button("Submit Semua Draft ke UID", type="primary"):
        count = submit_unit_assessments(unit_id, period_id, fullname)
        if count:
            st.success(f"{count} indikator berhasil di-submit dan menunggu review UID.")
        else:
            st.warning("Tidak ada draft yang bisa di-submit (isi minimal satu indikator dulu).")
        st.rerun()
