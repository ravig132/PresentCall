import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
import time

@st.dialog("Quick Course Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']

    res = supabase.table('subjects').select('subject_id, name').eq('subject_code', subject_code).execute()
    if not res.data:
        st.error('Course Code not found in database.')
        if st.button('Close', type='secondary'):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data[0]

    check = supabase.table('subject_students').select('*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
    if check.data:
        st.info(f"You are already enrolled in **{subject['name']}**.")
        if st.button('Continue to Dashboard', type='primary'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:14px; margin-bottom:16px;">
        <div style="font-size:0.85rem; color:#64748B;">Target Course</div>
        <div style="font-size:1.15rem; font-weight:700; color:#0F172A;">{subject['name']}</div>
        <div style="font-size:0.8rem; color:#2563EB; font-weight:600; font-family:monospace; margin-top:2px;">Code: {subject_code}</div>
    </div>
    <p style="color:#475569; font-size:0.88rem;">Would you like to enroll and add this course to your roster?</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Decline', type='secondary', width='stretch'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Confirm & Join', type='primary', width='stretch', icon=':material/check_circle:'):
            enroll_student_to_subject(student_id, subject['subject_id'])
            st.success(f"Joined {subject['name']} successfully!")
            st.query_params.clear()
            time.sleep(1.5)
            st.rerun()
