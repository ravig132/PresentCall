import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.navbar import top_navbar
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import (
    get_all_students,
    create_student,
    get_student_subjects,
    get_student_attendance,
    unenroll_student_to_subject,
    get_teacher_names,
)
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.stat_card import stat_row
import pandas as pd
from src.components.attendance_export import (
    build_attendance_csv,
    format_timestamp,
)


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

    if 'current_student_tab' not in st.session_state:
        st.session_state.current_student_tab = 'dashboard'

    _student_navigation_group('Operations', [
        ('Dashboard', 'dashboard', ':material/dashboard:'),
        ('Attendance Records', 'attendance_records', ':material/assignment:'),
    ])
    _student_navigation_group('Management', [
        ('My Subjects', 'subjects', ':material/book_ribbon:'),
        ('Settings', 'settings', ':material/settings:'),
    ])
    st.divider()

    if st.session_state.current_student_tab == 'dashboard':
        st.header('Dashboard')
        stat_row([
            ('📊', 'Overall Attendance', f'{overall_pct}%',
             f'{total_attended} / {total_classes} classes'),
            ('📚', 'Enrolled Subjects', len(subjects)),
            ('✅', 'Classes Attended', total_attended),
        ])

        log_rows = [
            {
                'date': str(log['timestamp'])[:10],
                'is_present': bool(log.get('is_present')),
            }
            for log in logs if log.get('timestamp')
        ]
        if log_rows:
            trend_df = pd.DataFrame(log_rows)
            trend_df['date'] = pd.to_datetime(trend_df['date']).dt.date
            daily = trend_df.groupby('date')['is_present'].mean().mul(100).round(1)
            st.space()
            st.subheader('Your Attendance Trend')
            st.line_chart(daily.tail(7))
        else:
            st.info('Your attendance trend will appear after your first class record.')

        recent_logs = sorted(
            [log for log in logs if log.get('timestamp')],
            key=lambda log: log['timestamp'],
            reverse=True,
        )[:5]
        if recent_logs:
            st.space()
            st.subheader('Recent Activity')
            recent_df = pd.DataFrame([{
                'Subject': (log.get('subjects') or {}).get('name', '-'),
                'Date': format_timestamp(log['timestamp']),
                'Method': {'face': 'FaceID', 'voice': 'VoiceID'}.get(
                    log.get('method'), '-'
                ),
                'Confidence': (
                    f"{log['confidence']:.1f}%"
                    if log.get('confidence') is not None else '-'
                ),
                'Status': 'Present' if log.get('is_present') else 'Absent',
            } for log in recent_logs])
            st.dataframe(recent_df, width='stretch', hide_index=True)
    elif st.session_state.current_student_tab == 'attendance_records':
        student_tab_attendance_records(student_data, logs)
    elif st.session_state.current_student_tab == 'subjects':
        student_tab_subjects(student_id, subjects, stats_map)
    else:
        student_tab_settings(student_data)

    footer_dashboard()


def _student_navigation_group(label, items):
    st.caption(label)
    columns = st.columns(len(items))
    for column, (title, tab_id, icon) in zip(columns, items):
        with column:
            if st.button(
                title,
                key=f'student_nav_{tab_id}',
                type=(
                    'primary'
                    if st.session_state.current_student_tab == tab_id
                    else 'tertiary'
                ),
                icon=icon,
                width='stretch',
            ):
                st.session_state.current_student_tab = tab_id
                st.rerun()


def student_tab_attendance_records(student_data, logs):
    st.header('Attendance Records')
    if not logs:
        st.info('No attendance has been recorded for your account yet.')
        return

    teacher_ids = [
        (log.get('subjects') or {}).get('teacher_id')
        for log in logs
        if (log.get('subjects') or {}).get('teacher_id') is not None
    ]
    teacher_names = get_teacher_names(teacher_ids)
    rows = []
    for log in logs:
        subject = log.get('subjects') or {}
        timestamp = log.get('timestamp')
        confidence = log.get('confidence')
        rows.append({
            'Student Name': student_data.get('name', '-'),
            'Student ID': student_data.get('student_id', '-'),
            'Subject ID': log.get('subject_id') or subject.get('subject_id', '-'),
            'Subject Name': subject.get('name', '-'),
            'Subject Code': subject.get('subject_code', '-'),
            'Teacher Name': teacher_names.get(subject.get('teacher_id'), '-'),
            'Timestamp': format_timestamp(timestamp),
            'Date': str(timestamp)[:10] if timestamp else '-',
            'Method': {'face': 'FaceID', 'voice': 'VoiceID'}.get(
                log.get('method'), '-'
            ),
            'AI Confidence Score': (
                f'{confidence:.1f}%' if confidence is not None else '-'
            ),
            'Status': 'Present' if log.get('is_present') else 'Absent',
        })

    df = pd.DataFrame(rows)
    subject_names = sorted(df['Subject Name'].dropna().unique().tolist())
    filter_col, search_col, status_col = st.columns([2, 2, 1])
    with filter_col:
        subject_filter = st.selectbox(
            'Filter by subject',
            ['All Subjects'] + subject_names,
            key='student_records_subject',
        )
    with search_col:
        search = st.text_input(
            'Search records',
            placeholder='Subject, code, or ID',
            key='student_records_search',
        )
    with status_col:
        status_filter = st.selectbox(
            'Status',
            ['All', 'Present', 'Absent'],
            key='student_records_status',
        )
    filtered = df.copy()
    if subject_filter != 'All Subjects':
        filtered = filtered[filtered['Subject Name'] == subject_filter]
    if search:
        search_columns = [
            'Subject ID', 'Subject Name', 'Subject Code', 'Teacher Name',
        ]
        mask = pd.Series(False, index=filtered.index)
        for column in search_columns:
            mask |= filtered[column].astype(str).str.contains(
                search, case=False, na=False
            )
        filtered = filtered[mask]
    if status_filter != 'All':
        filtered = filtered[filtered['Status'] == status_filter]

    if filtered.empty:
        st.info('No records match your search or filters.')
    else:
        st.dataframe(filtered, width='stretch', hide_index=True)

    st.download_button(
        'Download complete attendance CSV',
        data=build_attendance_csv(filtered.to_dict('records')),
        file_name='attendance_records.csv',
        mime='text/csv',
        icon=':material/download:',
    )


def student_tab_subjects(student_id, subjects, stats_map):
    st.header('Your Enrolled Subjects')
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption('View your subject-wise attendance or unenroll from a course.')
    with col2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()

    if not subjects:
        st.info('You are not enrolled in any subjects yet.')
        return

    cols = st.columns(2)
    for index, sub_node in enumerate(subjects):
        sub = sub_node.get('subjects')
        if not sub:
            continue
        subject_id = sub['subject_id']
        stats = stats_map.get(subject_id, {'total': 0, 'attended': 0})

        def unenroll_button(student_id=student_id, sid=subject_id, sub=sub):
            if st.button(
                'Unenroll from this course',
                type='tertiary',
                width='stretch',
                icon=':material/delete_forever:',
                key=f'unenroll_{sid}',
            ):
                unenroll_student_to_subject(student_id, sid)
                st.toast(f'Unenrolled from {sub["name"]} successfully!')
                st.rerun()

        subject_pct = (
            round(stats['attended'] / stats['total'] * 100)
            if stats['total'] else 0
        )
        with cols[index % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub.get('section', '-'),
                stats=[
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button,
            )
            st.progress(subject_pct / 100, text=f'{subject_pct}% attendance')


def student_tab_settings(student_data):
    st.header('Settings')
    st.subheader('Profile and biometric enrollment')
    stat_row([
        ('🪪', 'Student ID', student_data.get('student_id', '-')),
        (
            '📷',
            'FaceID',
            'Registered' if student_data.get('face_embedding') else 'Not registered',
        ),
        (
            '🎙️',
            'VoiceID',
            'Registered' if student_data.get('voice_embedding') else 'Not registered',
        ),
    ])
    st.info(
        'Face and voice profiles are used only by the existing attendance '
        'recognition flows. Contact your teacher if a biometric profile needs updating.'
    )


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
            detected, _, num_faces = predict_attendance(img)

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
