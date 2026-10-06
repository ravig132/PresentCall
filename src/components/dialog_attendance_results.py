import streamlit as st
from src.database.db import create_attendance

def show_attendance_result(df, logs):
    total = len(df)
    present_cnt = sum(1 for l in logs if l.get('is_present')) if logs else 0
    absent_cnt = total - present_cnt

    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:12px 16px; margin-bottom:14px; display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div style="font-weight:700; color:#0F172A; font-size:0.95rem;">Attendance Detection Audit</div>
            <div style="font-size:0.78rem; color:#64748B;">Please review matched identities before committing to database.</div>
        </div>
        <div style="display:flex; gap:8px;">
            <span style="background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:6px;">
                ✅ {present_cnt} Present
            </span>
            <span style="background:#FEF2F2; color:#DC2626; border:1px solid #FECACA; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:6px;">
                ❌ {absent_cnt} Absent
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, hide_index=True, width='stretch')

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Discard Session', type='tertiary', width='stretch', icon=':material/close:'):
            st.session_state.voice_attendance_results = None
            st.session_state.attendance_images = []
            st.rerun()

    with col2:
        if st.button('Confirm & Save Records', width='stretch', type='primary', icon=':material/check_circle:'):
            try:
                create_attendance(logs)
                st.toast("Attendance successfully recorded into database!", icon="✅")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error(f'Sync failed: {str(e)}')


@st.dialog("Attendance Verification Results")
def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
