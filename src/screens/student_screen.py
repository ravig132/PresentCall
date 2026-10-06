import streamlit as st
import time
import numpy as np
import pandas as pd
from datetime import datetime
from PIL import Image

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.navbar import top_navbar
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.stat_card import stat_row
from src.components.system_bar import render_page_header
from src.components.dialog_enroll import enroll_dialog

from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject
)


def student_screen():
    style_background_dashboard()
    style_base_layout()
    top_navbar()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Student Login / FaceID Biometric Scan
    render_page_header(
        title="Student Biometric Authentication",
        subtitle="Authenticate via optical FaceID sensor or register your new student profile.",
        breadcrumb="Biometric Login",
        badge="AI Vision 2.0"
    )

    # Professional Camera Container (Sections 18, 19, 20)
    col_l, col_cam, col_r = st.columns([1, 2, 1])
    with col_cam:
        st.markdown("""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);
            margin-bottom: 24px;
            text-align: center;
        ">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:14px;">
                <div style="text-align:left;">
                    <h3 style="margin:0 0 2px 0; color:#0F172A; font-weight:700; font-size:1.15rem;">Optical FaceID Scanner</h3>
                    <p style="margin:0; font-size:0.8rem; color:#64748B;">Center your face within frame for neural match</p>
                </div>
                <div style="display:flex; align-items:center; gap:6px; background:#ECFDF5; border:1px solid #A7F3D0; padding:3px 8px; border-radius:8px;">
                    <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10B981; box-shadow:0 0 6px #10B981;"></span>
                    <span style="font-size:0.72rem; font-weight:700; color:#059669;">SENSOR ACTIVE</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        photo_source = st.camera_input("Position face in camera viewport", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

    show_registration = False

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner('Neural scanner matching 128-d face descriptor...'):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('No face detected in camera viewport. Please center your face.')
            elif num_faces > 1:
                st.warning('Multiple faces detected. Please ensure only one student is in frame.')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'Authenticated! Welcome back {student["name"]}', icon="👋")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized in institutional database. You may register your new profile below.')
                    show_registration = True

    if show_registration:
        col_l, col_reg, col_r = st.columns([1, 2, 1])
        with col_reg:
            st.markdown("""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 16px;
                padding: 26px;
                box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);
                margin-bottom: 24px;
            ">
                <h3 style="margin:0 0 4px 0; color:#0F172A; font-weight:700; font-size:1.2rem;">Register New Student Profile</h3>
                <p style="color:#64748B; font-size:0.82rem; margin:0 0 16px 0;">Enroll your facial embedding with your institutional identity.</p>
            """, unsafe_allow_html=True)

            new_name = st.text_input("Full Name", placeholder='e.g. Priyanshu Vijay')

            st.markdown("""
            <div style="margin:14px 0 6px 0;">
                <span style="font-size:0.85rem; font-weight:600; color:#0F172A;">Voice ID Enrollment (Optional)</span>
                <p style="color:#64748B; font-size:0.78rem; margin:2px 0 8px 0;">Record phrase: "I am present, my name is ..."</p>
            </div>
            """, unsafe_allow_html=True)

            audio_data = None
            try:
                audio_data = st.audio_input("Record voice sample")
            except Exception:
                st.error('Microphone access unavailable.')

            st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
            if st.button('Complete Profile Enrollment', type='primary', width='stretch', icon=':material/check_circle:'):
                if new_name:
                    with st.spinner('Extracting embeddings and training classifier...'):
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
                                st.toast(f'Profile Created! Welcome {new_name}!')
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Could not extract facial landmarks. Please ensure good lighting.')
                else:
                    st.warning('Please enter your full name.')

            st.markdown("</div>", unsafe_allow_html=True)

    footer_dashboard()


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    has_face = bool(student_data.get('face_embedding'))
    has_voice = bool(student_data.get('voice_embedding'))

    status_badge = "FaceID & VoiceID Active" if (has_face and has_voice) else ("FaceID Active" if has_face else "Pending Credentials")

    render_page_header(
        title=f"Welcome, {student_data['name']}",
        subtitle="Track personal course attendance, attendance ratios, and enrollment status.",
        breadcrumb="Student Dashboard",
        badge=status_badge
    )

    with st.spinner('Loading attendance telemetry...'):
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

    # KPI Metric Cards
    stat_row([
        ('📊', 'Overall Attendance', f'{overall_pct}%', f'{total_attended} / {total_classes} total classes attended'),
        ('📚', 'Enrolled Subjects', len(subjects)),
        ('✅', 'Classes Attended', total_attended),
    ])

    st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)

    # 2-Column: Trend Chart (Left) + Recent Activity (Right)
    col_chart, col_rec = st.columns([7, 5], gap="large")

    with col_chart:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04); margin-bottom:16px;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
                <div>
                    <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.05rem; color:#0F172A;">Your Attendance Trajectory</div>
                    <div style="font-size:0.75rem; color:#64748B;">Daily personal presence ratio across enrolled sessions</div>
                </div>
                <div style="background:#EFF6FF; color:#2563EB; font-size:0.72rem; font-weight:700; padding:3px 8px; border-radius:6px; border:1px solid #DBEAFE;">
                    TRAJECTORY
                </div>
            </div>
        """, unsafe_allow_html=True)

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
                st.line_chart(daily.set_index('date')['Attendance %'], height=220)
            else:
                st.info("Additional session logs required to display attendance curve.")
        else:
            st.info("No recorded attendance logs yet.")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_rec:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04); margin-bottom:16px;">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.02rem; color:#0F172A; margin-bottom:4px;">
                Recent Verification Activity
            </div>
            <div style="font-size:0.76rem; color:#64748B; margin-bottom:12px;">
                Latest presence confirmations from class sessions.
            </div>
        """, unsafe_allow_html=True)

        recent_logs = sorted(
            [l for l in logs if l.get('timestamp')],
            key=lambda l: l['timestamp'], reverse=True
        )[:5]

        if recent_logs:
            recent_df = pd.DataFrame([{
                'Subject': l.get('subjects', {}).get('name', '-'),
                'Date': datetime.fromisoformat(l['timestamp'].split('.')[0]).strftime('%b %d, %I:%M %p'),
                'Status': '✅ Present' if l.get('is_present') else '❌ Absent',
            } for l in recent_logs])
            st.dataframe(recent_df, width='stretch', hide_index=True)
        else:
            st.info("No recent activity logs.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Enrolled Subjects Section
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        st.subheader('Enrolled Academic Courses')
        st.markdown("<p style='color:#64748B; font-size:0.85rem; margin:0;'>Your currently registered courses and attendance ratios.</p>", unsafe_allow_html=True)
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch', icon=':material/add:'):
            enroll_dialog()

    st.markdown("<div style='margin-bottom:16px;'></div>", unsafe_allow_html=True)

    if subjects:
        cols = st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']
            stats = stats_map.get(sid, {"total": 0, "attended": 0})

            def unenroll_button(student_id=student_id, sid=sid, sub=sub):
                if st.button(f"Unenroll from {sub['subject_code']}", key=f"unenroll_{sid}", type='tertiary', width='stretch', icon=':material/delete:'):
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
                st.progress(subject_pct / 100, text=f'{subject_pct}% Attendance Rate')
                st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)
    else:
        st.info("You are not currently enrolled in any courses. Tap 'Enroll in Subject' above to join with a course join code.")

    footer_dashboard()
