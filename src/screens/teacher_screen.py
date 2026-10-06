import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout

from src.components.navbar import top_navbar
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
    get_subject_students,
)
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.components.stat_card import stat_row
from src.components.attendance_export import (
    ATTENDANCE_EXPORT_COLUMNS,
    build_attendance_csv,
    format_timestamp,
)


def teacher_screen():

    style_background_dashboard()
    style_base_layout()
    top_navbar()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
    with c2:
        if st.button("Logout", type='secondary', key='loginbackbtn', width='stretch', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()

    if 'face_match_threshold' not in st.session_state:
        st.session_state.face_match_threshold = 0.6
    with st.spinner('Loading dashboard data...'):
        subjects = get_teacher_subjects(teacher_data['teacher_id'])
        records = get_attendance_for_teacher(teacher_data['teacher_id'])

    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab = 'dashboard'
    st.session_state.current_teacher_tab = {
        'take_attendance': 'ai_attendance',
        'manage_subjects': 'subject_management',
    }.get(
        st.session_state.current_teacher_tab,
        st.session_state.current_teacher_tab,
    )
    valid_tabs = {
        'dashboard',
        'attendance_records',
        'ai_attendance',
        'voice_roll_call',
        'students_directory',
        'subject_management',
        'settings',
    }
    if st.session_state.current_teacher_tab not in valid_tabs:
        st.session_state.current_teacher_tab = 'dashboard'

    _teacher_navigation_group('Operations', [
        ('Dashboard', 'dashboard', ':material/dashboard:'),
        ('Attendance Records', 'attendance_records', ':material/assignment:'),
        ('AI Attendance', 'ai_attendance', ':material/face:'),
        ('Voice ID Roll-Call', 'voice_roll_call', ':material/mic:'),
    ])
    _teacher_navigation_group('Management', [
        ('Students Directory', 'students_directory', ':material/groups:'),
        ('Subject Management', 'subject_management', ':material/book_ribbon:'),
        ('Settings', 'settings', ':material/settings:'),
    ])
    st.divider()

    current_tab = st.session_state.current_teacher_tab
    if current_tab == 'dashboard':
        teacher_tab_dashboard(subjects, records)
    elif current_tab == 'attendance_records':
        teacher_tab_attendance_records(records)
    elif current_tab == 'ai_attendance':
        teacher_tab_take_attendance()
    elif current_tab == 'voice_roll_call':
        teacher_tab_voice_roll_call(subjects)
    elif current_tab == 'students_directory':
        teacher_tab_students_directory(subjects, records)
    elif current_tab == 'subject_management':
        teacher_tab_manage_subjects(subjects)
    elif current_tab == 'settings':
        teacher_tab_settings()

    footer_dashboard()


def _teacher_navigation_group(label, items):
    st.caption(label)
    columns = st.columns(len(items))
    for column, (title, tab_id, icon) in zip(columns, items):
        with column:
            selected = st.session_state.current_teacher_tab == tab_id
            if st.button(
                title,
                key=f'teacher_nav_{tab_id}',
                type='primary' if selected else 'tertiary',
                icon=icon,
                width='stretch',
            ):
                st.session_state.current_teacher_tab = tab_id
                st.rerun()


def teacher_tab_dashboard(subjects, records):
    st.header('Dashboard')
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_records = [
        row for row in records
        if str(row.get('timestamp', '')).startswith(today_str)
    ]
    present_today = sum(bool(row.get('is_present')) for row in today_records)
    absent_today = sum(not bool(row.get('is_present')) for row in today_records)
    stat_row([
        ('🏫', 'Active Subjects', len(subjects)),
        ('🫂', 'Student Enrollments', sum(s.get('total_students', 0) for s in subjects)),
        ('✅', 'Present Today', present_today),
        ('❌', 'Absent Today', absent_today),
    ])

    st.space()
    chart_col, feed_col = st.columns([3, 2])
    with chart_col:
        st.subheader('Weekly Attendance Trend')
        trend_rows = [
            {
                'date': str(row['timestamp'])[:10],
                'present': bool(row.get('is_present')),
            }
            for row in records if row.get('timestamp')
        ]
        if trend_rows:
            trend = pd.DataFrame(trend_rows)
            trend['date'] = pd.to_datetime(trend['date']).dt.date
            daily = trend.groupby('date')['present'].mean().mul(100).round(1)
            st.line_chart(daily.tail(7))
        else:
            st.info('Attendance trends will appear after attendance is recorded.')

    with feed_col:
        st.subheader('Recent Verifications')
        recent = sorted(
            [row for row in records if row.get('timestamp')],
            key=lambda row: row['timestamp'],
            reverse=True,
        )[:10]
        if recent:
            feed = []
            for row in recent:
                student = row.get('students') or {}
                subject = row.get('subjects') or {}
                confidence = row.get('confidence')
                feed.append({
                    'Student': student.get('name', f"ID {row.get('student_id', '-')}"),
                    'Subject': subject.get('name', '-'),
                    'Method': {'face': 'FaceID', 'voice': 'VoiceID'}.get(
                        row.get('method'), '-'
                    ),
                    'Confidence': f'{confidence:.1f}%' if confidence is not None else '-',
                    'Time': format_timestamp(row.get('timestamp')),
                })
            st.dataframe(pd.DataFrame(feed), width='stretch', hide_index=True)
        else:
            st.info('No attendance verifications have been recorded yet.')

    if records:
        present_count = sum(bool(row.get('is_present')) for row in records)
        st.caption(
            f"Recorded attendance: {present_count} present of {len(records)} "
            f"student-session records."
        )


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    with st.expander('Biometric Parameters'):
        st.write('Face embedding: dlib ResNet, 128 dimensions')
        st.write('Face classifier: linear SVM')
        st.write('Voice embedding: Resemblyzer, 256 dimensions')
        st.caption(
            'Face match threshold is an L2 embedding-distance limit. '
            'The displayed confidence is derived from distance and is not calibrated.'
        )
        threshold = st.slider(
            'Face match threshold',
            min_value=0.3,
            max_value=1.0,
            step=0.01,
            key='face_match_threshold',
            help='Lower values require a closer face-embedding match.',
        )
        st.caption(f'Current face match threshold: {threshold:.2f}')

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2 = st.columns(2)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:

        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}
                all_detected_scores = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(
                        img_np,
                        resemblance_threshold=st.session_state.face_match_threshold,
                    )

                    if detected:
                        for sid, confidence in detected.items():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")
                            all_detected_scores[student_id] = max(
                                all_detected_scores.get(student_id, 0), confidence
                            )

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', selected_subject_id).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                    return

                results, attendance_to_log = [], []
                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                for node in enrolled_students:
                    student = node['students']
                    sid_int = int(student['student_id'])
                    sources = all_detected_ids.get(sid_int, [])
                    is_present = len(sources) > 0
                    confidence = all_detected_scores.get(sid_int)

                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Source": ", ".join(sources) if is_present else "-",
                        "Match Confidence": (
                            f"{confidence}%" if confidence is not None else "-"
                        ),
                        "Status": "✅ Present" if is_present else "❌ Absent",
                    })

                    attendance_to_log.append({
                        'student_id': student['student_id'],
                        'subject_id': selected_subject_id,
                        'timestamp': current_timestamp,
                        'is_present': bool(is_present),
                        'method': 'face',
                        'confidence': confidence,
                    })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

def teacher_tab_voice_roll_call(subjects):
    st.header('Voice ID Roll-Call')
    if not subjects:
        st.info('Create a subject before starting a voice roll-call.')
        return
    subject_options = {
        f"{subject['name']} - {subject['subject_code']}": subject['subject_id']
        for subject in subjects
    }
    selected_label = st.selectbox(
        'Select Subject',
        options=list(subject_options),
        key='voice_roll_call_subject',
    )
    st.info(
        'Record a classroom audio clip. Students need a registered VoiceID '
        'profile to be matched.'
    )
    if st.button(
        'Start Voice ID Roll-Call',
        type='primary',
        icon=':material/mic:',
        key='start_voice_roll_call',
    ):
        voice_attendance_dialog(subject_options[selected_label])


def teacher_tab_students_directory(subjects, records):
    st.header('Students Directory')
    if not subjects:
        st.info('Create a subject before managing its student directory.')
        return

    subject_options = {
        f"{subject['name']} - {subject['subject_code']}": subject['subject_id']
        for subject in subjects
    }
    selected_label = st.selectbox(
        'Subject roster',
        options=list(subject_options),
        key='directory_subject',
    )
    subject_id = subject_options[selected_label]
    enrolled = get_subject_students(subject_id)
    subject_records = [
        row for row in records if row.get('subject_id') == subject_id
    ]
    if not enrolled:
        st.info('No students are enrolled in this subject yet.')
        return

    student_rows = []
    for item in enrolled:
        student = item.get('students') or {}
        student_id = student.get('student_id', item.get('student_id'))
        attendance = [
            row for row in subject_records
            if row.get('student_id') == student_id
        ]
        attended = sum(bool(row.get('is_present')) for row in attendance)
        pct = round(attended / len(attendance) * 100, 1) if attendance else 0.0
        student_rows.append({
            'Student Name': student.get('name', '-'),
            'Student ID': student_id,
            'FaceID': 'Registered' if student.get('face_embedding') else 'Not registered',
            'VoiceID': 'Registered' if student.get('voice_embedding') else 'Not registered',
            'Attendance %': pct if attendance else 'No records',
            'Sessions Attended': f'{attended} / {len(attendance)}',
        })

    stat_row([
        ('🫂', 'Enrolled Students', len(student_rows)),
        ('📷', 'FaceID Profiles', sum(row['FaceID'] == 'Registered' for row in student_rows)),
        ('🎙️', 'VoiceID Profiles', sum(row['VoiceID'] == 'Registered' for row in student_rows)),
    ])
    st.dataframe(pd.DataFrame(student_rows), width='stretch', hide_index=True)
    chart_rows = [
        {'Student': row['Student Name'], 'Attendance %': row['Attendance %']}
        for row in student_rows if isinstance(row['Attendance %'], (int, float))
    ]
    if chart_rows:
        st.subheader('Subject Attendance by Student')
        st.bar_chart(pd.DataFrame(chart_rows).set_index('Student'))


def teacher_tab_manage_subjects(subjects=None):
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    if subjects is None:
        subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.space()

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("No subjects found. Create one above to get started.")


def teacher_tab_settings():
    st.header('Settings')
    st.subheader('Face matching')
    st.caption(
        'This setting is active for face-based AI attendance for this session. '
        'The underlying distance-derived confidence is approximate, not calibrated.'
    )
    st.slider(
        'Face match threshold',
        min_value=0.3,
        max_value=1.0,
        step=0.01,
        key='face_match_threshold',
        help='Lower values require a closer face-embedding match.',
    )
    with st.expander('Biometric model details'):
        st.write('Face embedding: dlib ResNet, 128 dimensions')
        st.write('Face classifier: linear SVM')
        st.write('Voice embedding: Resemblyzer, 256 dimensions')
        st.info('Liveness / anti-spoofing is not implemented.')


def _teacher_attendance_rows(records):
    teacher_name = st.session_state.teacher_data.get('name', '-')
    rows = []
    for record in records:
        subject = record.get('subjects') or {}
        student = record.get('students') or {}
        timestamp = record.get('timestamp')
        confidence = record.get('confidence')
        rows.append({
            'Student Name': student.get(
                'name', f"ID {record.get('student_id', '-')}"
            ),
            'Student ID': record.get('student_id', '-'),
            'Subject ID': record.get('subject_id') or subject.get('subject_id', '-'),
            'Subject Name': subject.get('name', '-'),
            'Subject Code': subject.get('subject_code', '-'),
            'Teacher Name': teacher_name,
            'Timestamp': format_timestamp(timestamp),
            'Date': str(timestamp)[:10] if timestamp else '-',
            'Method': {'face': 'FaceID', 'voice': 'VoiceID'}.get(
                record.get('method'), '-'
            ),
            'AI Confidence Score': (
                f'{confidence:.1f}%' if confidence is not None else '-'
            ),
            'Status': 'Present' if record.get('is_present') else 'Absent',
            '_timestamp': timestamp or '',
        })
    return rows


def teacher_tab_attendance_records(records=None):
    st.header('Attendance Records')

    if records is None:
        teacher_id = st.session_state.teacher_data['teacher_id']
        records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance has been recorded yet.")
        return

    detailed_rows = _teacher_attendance_rows(records)
    df = pd.DataFrame(detailed_rows)

    # ---------- Weekly attendance trend ----------
    chart_rows = [
        {'Date': row['Date'], 'Present': row['Status'] == 'Present'}
        for row in detailed_rows if row['Date'] != '-'
    ]
    if chart_rows:
        trend = pd.DataFrame(chart_rows)
        trend['Date'] = pd.to_datetime(trend['Date']).dt.date
        daily = trend.groupby('Date')['Present'].mean().mul(100).round(1)
        st.subheader('Weekly Attendance Trend')
        st.line_chart(daily.tail(7))

    st.radio(
        'Record view',
        ['Session summaries', 'Student-level records'],
        horizontal=True,
        key='teacher_record_view',
    )
    subject_names = sorted(df['Subject Name'].dropna().unique().tolist())
    c1, c2 = st.columns([2, 1])
    with c1:
        search = st.text_input(
            'Search records',
            placeholder='Student, subject name, code, or ID',
            key='teacher_records_search',
        )
    with c2:
        subject_filter = st.selectbox(
            'Filter by subject',
            options=['All Subjects'] + subject_names,
            key='teacher_records_subject',
        )

    filtered = df.copy()
    if subject_filter != 'All Subjects':
        filtered = filtered[filtered['Subject Name'] == subject_filter]
    if search:
        searchable = [
            'Student Name', 'Student ID', 'Subject Name', 'Subject Code',
            'Subject ID',
        ]
        mask = pd.Series(False, index=filtered.index)
        for column in searchable:
            mask |= filtered[column].astype(str).str.contains(
                search, case=False, na=False
            )
        filtered = filtered[mask]

    if st.session_state.teacher_record_view == 'Session summaries':
        summary_source = filtered
        summary = summary_source.groupby(
            ['Timestamp', 'Date', 'Subject Name', 'Subject Code', 'Subject ID'],
            dropna=False,
        ).agg(
            Present=('Status', lambda values: (values == 'Present').sum()),
            Total=('Status', 'count'),
        ).reset_index()
        summary['Attendance Stats'] = (
            summary['Present'].astype(str) + ' / '
            + summary['Total'].astype(str) + ' Students'
        )
        display_df = summary.sort_values(
            'Timestamp', ascending=False
        )[['Timestamp', 'Date', 'Subject Name', 'Subject Code', 'Attendance Stats']]
        export_rows = filtered.drop(columns=['_timestamp'])
    else:
        status_filter = st.selectbox(
            'Filter by status',
            ['All', 'Present', 'Absent'],
            key='teacher_records_status',
        )
        display_df = filtered.copy()
        if status_filter != 'All':
            display_df = display_df[display_df['Status'] == status_filter]
        display_df = display_df.drop(columns=['_timestamp'])
        export_rows = display_df

    if display_df.empty:
        st.info('No records match your search/filter.')
    else:
        st.dataframe(display_df, width='stretch', hide_index=True)

    detailed_export = export_rows[ATTENDANCE_EXPORT_COLUMNS]
    st.download_button(
        'Download complete attendance CSV',
        data=build_attendance_csv(detailed_export.to_dict('records')),
        file_name='attendance_records.csv',
        mime='text/csv',
        icon=':material/download:',
    )


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


def teacher_screen_login():
    st.header('Teacher Login', text_alignment='center')
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='kiran')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")

    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'register'

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"


def teacher_screen_register():
    st.header('Register your teacher profile')
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='kiran')
    teacher_name = st.text_input("Enter name", placeholder='Kiran')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")
    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'

    footer_dashboard()
