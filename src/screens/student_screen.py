import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.navbar import top_navbar
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.stat_card import stat_row
import pandas as pd
from datetime import datetime


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        st.subheader(f"""Welcome, {student_data['name']} """)
        has_face = bool(student_data.get('face_embedding'))
        has_voice = bool(student_data.get('voice_embedding'))
        badge_html = (
            f'<span style="font-size:0.8rem; margin-right:10px;">'
            f'{"✅" if has_face else "⚠️"} FaceID {"Registered" if has_face else "Not Registered"}</span>'
            f'<span style="font-size:0.8rem;">'
            f'{"✅" if has_voice else "⚠️"} VoiceID {"Registered" if has_voice else "Not Registered"}</span>'
        )
        st.markdown(badge_html, unsafe_allow_html=True)
    with c2:
        if st.button("Logout", type='secondary', key='loginbackbtn', width='stretch', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    with st.spinner('Loading your attendance..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}

        stats_map[sid]['total'] += 1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    total_classes = sum(s['total'] for s in stats_map.values())
    total_attended = sum(s['attended'] for s in stats_map.values())
    overall_pct = round((total_attended / total_classes) * 100, 1) if total_classes else 0.0

    stat_row([
        ('📊', 'Overall Attendance', f'{overall_pct}%',
         f'{total_attended} / {total_classes} classes'),
        ('📚', 'Enrolled Subjects', len(subjects)),
        ('✅', 'Classes Attended', total_attended),
    ])

    # ---------- Attendance trend ----------
    log_rows = []
    for log in logs:
        ts = log.get('timestamp')
        if ts:
            log_rows.append({'date': pd.to_datetime(ts.split('.')[0]).date(), 'is_present': bool(log.get('is_present'))})

    if log_rows:
        trend_df = pd.DataFrame(log_rows)
        daily = trend_df.groupby('date')['is_present'].mean().reset_index()
        daily['Attendance %'] = (daily['is_present'] * 100).round(1)
        daily = daily.sort_values('date').tail(7)

        if len(daily) >= 2:
            st.space()
            st.subheader('Your Attendance Trend')
            st.line_chart(daily.set_index('date')['Attendance %'])

    # ---------- Recent activity ----------
    recent_logs = sorted(
        [l for l in logs if l.get('timestamp')],
        key=lambda l: l['timestamp'], reverse=True
    )[:5]

    if recent_logs:
        st.space()
        st.subheader('Recent Activity')
        recent_df = pd.DataFrame([{
            'Subject': l.get('subjects', {}).get('name', '-'),
            'Date': datetime.fromisoformat(l['timestamp'].split('.')[0]).strftime('%b %d, %I:%M %p'),
            'Status': '✅ Present' if l.get('is_present') else '❌ Absent',
        } for l in recent_logs])
        st.dataframe(recent_df, width='stretch', hide_index=True)

    st.space()

    c1, c2 = st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()

    st.divider()

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button(student_id=student_id, sid=sid, sub=sub):
            if st.button("Unenroll from this course", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f'Unenrolled from {sub["name"]} successfully!')
                st.rerun()

        subject_pct = round((stats['attended'] / stats['total']) * 100) if stats['total'] else 0

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
            st.progress(subject_pct / 100, text=f'{subject_pct}% attendance')
    footer_dashboard()


def student_screen():

    style_background_dashboard()
    style_base_layout()
    top_navbar()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    st.header('Login using FaceID', text_alignment='center')
    st.space()

    show_registration = False
    photo_source = st.camera_input("Position your face in the center")

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('AI is scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('Face not found!')
            elif num_faces > 1:
                st.warning('Multiple faces found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'Welcome Back {student["name"]}')
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Vijay Sharma')

            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")

            audio_data = None

            try:
                audio_data = st.audio_input('Record a short phrase like I am present, My name is Vijay.')
            except Exception:
                st.error('Audio Data failed!')

            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner('Creating profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration')

                else:
                    st.warning('Please enter your name!')

    footer_dashboard()
