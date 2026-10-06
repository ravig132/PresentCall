import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
import pandas as pd
from src.components.dialog_attendance_results import show_attendance_result
from datetime import datetime

@st.dialog('Voice ID Roll-Call')
def voice_attendance_dialog(selected_subject_id):
    st.markdown("""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:12px 14px; margin-bottom:14px;">
        <div style="font-weight:700; color:#0F172A; font-size:0.95rem;">Acoustic Biometric Verification</div>
        <div style="font-size:0.8rem; color:#64748B;">Record students calling out roll or saying "I am present". The neural model will match 256-d voice vectors.</div>
    </div>
    """, unsafe_allow_html=True)

    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio Stream', width='stretch', type='primary', icon=':material/graphic_eq:'):
        if not audio_data:
            st.warning('Please finish recording (tap stop) before analyzing.')
            return

        with st.spinner('Matching acoustic signatures across enrolled student profiles...'):
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning('No students enrolled in this course.')
                return

            candidates_dict = {
                s['students']['student_id']: s['students']['voice_embedding'] 
                for s in enrolled_students if s['students'].get('voice_embedding')
            }

            if not candidates_dict:
                st.error('No enrolled students have voice profiles registered.')
                return

            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes, candidates_dict)

            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            for node in enrolled_students:
                student = node['students']
                score = detected_scores.get(student['student_id'], 0.0)
                is_present = bool(score > 0)

                results.append({
                    "Name": student['name'],
                    "ID": student['student_id'],
                    "Acoustic Score": f"{score:.2f}" if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })

                attendance_to_log.append({
                    'student_id': student['student_id'],
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })

            st.session_state.voice_attendance_results = (pd.DataFrame(results), attendance_to_log)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)