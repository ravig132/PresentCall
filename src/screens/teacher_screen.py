import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.navbar import top_navbar
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.stat_card import stat_row
from src.components.system_bar import render_page_header
from src.components.real_time_feed import render_real_time_feed

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects,
    get_attendance_for_teacher,
    get_all_students,
    create_attendance
)
from src.database.config import supabase

from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_results import attendance_result_dialog, show_attendance_result
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.pipelines.voice_pipeline import process_bulk_audio


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
    teacher_id = teacher_data['teacher_id']

    # Default tab
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'dashboard'

    tab = st.session_state.current_teacher_tab

    # Fetch data
    with st.spinner('Loading institutional telemetry...'):
        overview_subjects = get_teacher_subjects(teacher_id)
        overview_records = get_attendance_for_teacher(teacher_id)

    total_subjects = len(overview_subjects)
    total_students = sum(s.get('total_students', 0) for s in overview_subjects)
    total_classes = sum(s.get('total_classes', 0) for s in overview_subjects)

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_records = [r for r in (overview_records or []) if r.get('timestamp', '').startswith(today_str)]
    present_today = sum(1 for r in today_records if r.get('is_present'))
    absent_today = sum(1 for r in today_records if not r.get('is_present'))

    # Top Workspace Tab Navigation Pills
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    with t1:
        if st.button("Overview", key="pill_dash", type="primary" if tab == "dashboard" else "tertiary", width="stretch", icon=":material/dashboard:"):
            st.session_state.current_teacher_tab = 'dashboard'
            st.rerun()
    with t2:
        if st.button("AI Face Attendance", key="pill_ai", type="primary" if tab == "take_attendance" else "tertiary", width="stretch", icon=":material/photo_camera:"):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()
    with t3:
        if st.button("Voice ID Roll-Call", key="pill_voice", type="primary" if tab == "voice_attendance" else "tertiary", width="stretch", icon=":material/mic:"):
            st.session_state.current_teacher_tab = 'voice_attendance'
            st.rerun()
    with t4:
        if st.button("Records & Reports", key="pill_rec", type="primary" if tab == "attendance_records" else "tertiary", width="stretch", icon=":material/table_chart:"):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()
    with t5:
        if st.button("Manage Subjects", key="pill_sub", type="primary" if tab == "manage_subjects" else "tertiary", width="stretch", icon=":material/menu_book:"):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()
    with t6:
        if st.button("Students Roster", key="pill_dir", type="primary" if tab == "students_directory" else "tertiary", width="stretch", icon=":material/group:"):
            st.session_state.current_teacher_tab = 'students_directory'
            st.rerun()

    st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)

    # Route content according to active tab
    if tab == 'dashboard':
        teacher_tab_dashboard(teacher_data, overview_subjects, overview_records, total_subjects, total_students, present_today, absent_today, today_records)
    elif tab == 'take_attendance':
        teacher_tab_take_attendance()
    elif tab == 'voice_attendance':
        teacher_tab_voice_attendance()
    elif tab == 'attendance_records':
        teacher_tab_attendance_records()
    elif tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    elif tab == 'students_directory':
        teacher_tab_students_directory()

    footer_dashboard()


# -------------------------------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW (DASHBOARD)
# -------------------------------------------------------------------
def teacher_tab_dashboard(teacher_data, overview_subjects, overview_records, total_subjects, total_students, present_today, absent_today, today_records):
    render_page_header(
        title="Executive Overview",
        subtitle="Monitor live attendance, verification telemetry, and classroom performance.",
        breadcrumb="Executive Overview",
        badge=f"Faculty: {teacher_data.get('name', 'Instructor')}"
    )

    # 4 Enterprise Metric Cards
    stat_row([
        ('🏫', 'Active Subjects', total_subjects),
        ('👥', 'Total Students', total_students),
        ('✅', 'Present Today', present_today),
        ('❌', 'Absent Today', absent_today),
    ])

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # 2-Column Layout: Analytics Chart (Left) + Real-Time Verification Feed (Right)
    col_chart, col_feed = st.columns([7, 5], gap="large")

    with col_chart:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04); margin-bottom:16px;">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
                <div>
                    <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.05rem; color:#0F172A;">Weekly Attendance Rate</div>
                    <div style="font-size:0.75rem; color:#64748B;">Institutional daily presence ratio across registered sessions</div>
                </div>
                <div style="background:#EFF6FF; color:#2563EB; font-size:0.72rem; font-weight:700; padding:3px 8px; border-radius:6px; border:1px solid #DBEAFE;">
                    7-DAY TREND
                </div>
            </div>
        """, unsafe_allow_html=True)

        if overview_records:
            data = []
            for r in overview_records:
                ts = r.get('timestamp')
                if ts:
                    data.append({
                        'date': pd.to_datetime(ts.split(".")[0]).date(),
                        'is_present': bool(r.get('is_present', False))
                    })
            if data:
                df = pd.DataFrame(data)
                daily = df.groupby('date')['is_present'].mean().reset_index()
                daily['Attendance %'] = (daily['is_present'] * 100).round(1)
                daily = daily.sort_values('date').tail(7)
                if len(daily) >= 2:
                    st.line_chart(daily.set_index('date')['Attendance %'], height=220)
                else:
                    st.info("Additional session logs needed to construct 7-day trend curve.")
            else:
                st.info("No recorded sessions yet this week.")
        else:
            st.info("No attendance records logged yet. Run face analysis to populate.")

        st.markdown("</div>", unsafe_allow_html=True)

        # Quick Actions Card
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px 20px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:0.98rem; color:#0F172A; margin-bottom:4px;">
                Quick Attendance Actions
            </div>
            <div style="font-size:0.78rem; color:#64748B; margin-bottom:14px;">
                Launch real-time biometric roll-calls or manage course rosters.
            </div>
        """, unsafe_allow_html=True)

        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            if st.button("Take AI Attendance", key="dash_btn_ai", type="primary", width="stretch", icon=":material/ar_on_you:"):
                st.session_state.current_teacher_tab = 'take_attendance'
                st.rerun()
        with qa2:
            if st.button("Voice Roll-Call", key="dash_btn_voice", type="secondary", width="stretch", icon=":material/mic:"):
                st.session_state.current_teacher_tab = 'voice_attendance'
                st.rerun()
        with qa3:
            if st.button("Course Roster", key="dash_btn_sub", type="secondary", width="stretch", icon=":material/menu_book:"):
                st.session_state.current_teacher_tab = 'manage_subjects'
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_feed:
        # Real-Time Verification Feed (Sections 16 & 17)
        render_real_time_feed(today_records)


# -------------------------------------------------------------------
# TAB 2: TAKE AI ATTENDANCE
# -------------------------------------------------------------------
def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    render_page_header(
        title="AI Attendance — Group Face Recognition",
        subtitle="Capture or upload classroom photos to automatically detect and mark enrolled students present.",
        breadcrumb="AI Attendance",
        badge="Engine Ready"
    )

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning('You have not created any subjects yet! Please create one in Manage Subjects to begin.')
        return

    subject_options = {f"{s['name']} ({s['subject_code']}) — Section {s['section']}": s['subject_id'] for s in subjects}

    # Professional Camera / Photo Control Container
    st.markdown("""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        margin-bottom: 20px;
    ">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
            <div>
                <h3 style="margin:0 0 4px 0; color:#0F172A; font-size:1.15rem; font-weight:700;">Session Parameters & Media</h3>
                <p style="margin:0; font-size:0.8rem; color:#64748B;">Select target academic course and provide classroom group snapshots.</p>
            </div>
            <div style="display:flex; align-items:center; gap:6px; background:#ECFDF5; border:1px solid #A7F3D0; padding:4px 10px; border-radius:8px;">
                <span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#10B981; box-shadow:0 0 6px #10B981;"></span>
                <span style="font-size:0.75rem; font-weight:700; color:#059669;">● AI Verification Ready</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1], vertical_alignment='bottom')
    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))
    with col2:
        if st.button('Add Photos', type='primary', icon=':material/add_a_photo:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]
    st.markdown("</div>", unsafe_allow_html=True)

    # Added Photos Gallery
    if st.session_state.attendance_images:
        st.subheader(f"Added Classroom Photos ({len(st.session_state.attendance_images)})")
        gallery_cols = st.columns(min(4, len(st.session_state.attendance_images)))
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')

    has_photos = bool(st.session_state.attendance_images)

    # Action Toolbar
    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='primary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos with 128-d ResNet embeddings...'):
                all_detected_ids = {}
                all_detected_scores = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)

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
                    st.warning('No students currently enrolled in this course.')
                else:
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
                            "Match Confidence": f"{confidence}%" if confidence is not None else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='secondary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)


# -------------------------------------------------------------------
# TAB 3: VOICE ID ROLL-CALL
# -------------------------------------------------------------------
def teacher_tab_voice_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']

    render_page_header(
        title="Voice ID Roll-Call",
        subtitle="Sequential & bulk voice acoustic verification for classroom attendance.",
        breadcrumb="Voice ID",
        badge="Acoustic Engine"
    )

    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning('Please create a subject first.')
        return

    subject_options = {f"{s['name']} ({s['subject_code']})": s['subject_id'] for s in subjects}
    selected_label = st.selectbox('Target Subject', options=list(subject_options.keys()))
    selected_subject_id = subject_options[selected_label]

    st.markdown("""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(15,23,42,0.04);
        margin: 16px 0;
        text-align: center;
    ">
        <div style="width:48px; height:48px; border-radius:50%; background:#EFF6FF; color:#2563EB; display:inline-flex; align-items:center; justify-content:center; font-size:1.6rem; margin-bottom:12px;">
            🎙️
        </div>
        <h3 style="margin:0 0 6px 0; font-size:1.2rem; color:#0F172A; font-weight:700;">Classroom Audio Stream Capture</h3>
        <p style="color:#64748B; font-size:0.85rem; max-width:540px; margin:0 auto 16px auto;">
            Record audio of students calling out roll or stating "I am present". The neural acoustic model will extract 256-d voice d-vectors and match them to enrolled profiles.
        </p>
    """, unsafe_allow_html=True)

    audio_data = st.audio_input("Record classroom audio")

    if st.button('Analyze Audio & Log Attendance', width='stretch', type='primary', icon=':material/graphic_eq:'):
        if not audio_data:
            st.warning('Please finish recording (tap stop) before analyzing.')
        else:
            with st.spinner('Matching voice embeddings across enrolled roster...'):
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
                    st.error('No enrolled students have voice profiles registered yet.')
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

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df_results, logs = st.session_state.voice_attendance_results
        show_attendance_result(df_results, logs)


# -------------------------------------------------------------------
# TAB 4: ATTENDANCE RECORDS & REPORTS
# -------------------------------------------------------------------
def teacher_tab_attendance_records():
    teacher_id = st.session_state.teacher_data['teacher_id']

    render_page_header(
        title="Attendance Records & Reports",
        subtitle="Search, audit, and export historical classroom attendance sessions.",
        breadcrumb="Records",
        badge="Audit Log"
    )

    records = get_attendance_for_teacher(teacher_id)
    if not records:
        st.info("No attendance has been recorded yet. Take an AI attendance session to generate logs.")
        return

    data = []
    for r in records:
        ts = r.get('timestamp')
        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    # Session summary table
    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + ' Students'
    )

    full_df = (summary.sort_values(by='ts_group', ascending=False)
               [['Time', 'Subject', 'Subject Code', 'Attendance Stats']])

    # Filter Toolbar
    c1, c2 = st.columns([2, 1])
    with c1:
        search = st.text_input('Search records', placeholder='e.g. CS101 or Computer Science')
    with c2:
        subject_options = ['All Subjects'] + sorted(full_df['Subject'].unique().tolist())
        subject_filter = st.selectbox('Filter by subject', options=subject_options)

    display_df = full_df.copy()
    if subject_filter != 'All Subjects':
        display_df = display_df[display_df['Subject'] == subject_filter]
    if search:
        mask = (
            display_df['Subject'].str.contains(search, case=False, na=False)
            | display_df['Subject Code'].str.contains(search, case=False, na=False)
        )
        display_df = display_df[mask]

    if display_df.empty:
        st.info('No records match your search/filter parameters.')
    else:
        st.dataframe(display_df, width='stretch', hide_index=True)

    st.download_button(
        'Export CSV Report',
        data=full_df.to_csv(index=False).encode('utf-8'),
        file_name='present_call_attendance_records.csv',
        mime='text/csv',
        icon=':material/download:'
    )


# -------------------------------------------------------------------
# TAB 5: MANAGE SUBJECTS
# -------------------------------------------------------------------
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    render_page_header(
        title="Manage Subjects",
        subtitle="Manage academic courses, student join codes, and enrollment links.",
        breadcrumb="Subjects",
        badge="Course Directory"
    )

    col1, col2 = st.columns([3, 1], vertical_alignment='center')
    with col1:
        st.markdown("<p style='color:#64748B; margin:0;'>Active subjects under your faculty administration.</p>", unsafe_allow_html=True)
    with col2:
        if st.button('Create New Subject', type='primary', width='stretch', icon=':material/add:'):
            create_subject_dialog(teacher_id)

    st.markdown("<div style='margin-bottom:16px;'></div>", unsafe_allow_html=True)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(sub=sub):
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(sub['name'], sub['subject_code'])
                st.markdown("<div style='margin-bottom:8px;'></div>", unsafe_allow_html=True)

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("No active courses found. Tap 'Create New Subject' above to set up your first class.")


# -------------------------------------------------------------------
# TAB 6: STUDENTS DIRECTORY
# -------------------------------------------------------------------
def teacher_tab_students_directory():
    render_page_header(
        title="Students Directory",
        subtitle="Roster of enrolled students and their biometric verification credentials.",
        breadcrumb="Students Directory",
        badge="Student Registry"
    )

    students = get_all_students()
    if not students:
        st.info("No students registered yet in the institutional database.")
        return

    search_query = st.text_input("Search students by name or ID", placeholder="e.g. Priyanshu, PC001")

    rows = []
    for s in students:
        has_face = bool(s.get('face_embedding'))
        has_voice = bool(s.get('voice_embedding'))
        rows.append({
            "Student ID": f"PC{int(s['student_id']):03d}",
            "Full Name": s.get('name', 'N/A'),
            "FaceID Status": "✅ Enrolled" if has_face else "⚠️ Missing",
            "VoiceID Status": "✅ Enrolled" if has_voice else "⚠️ Missing",
            "Account Status": "Active"
        })

    df = pd.DataFrame(rows)
    if search_query:
        mask = (
            df['Full Name'].str.contains(search_query, case=False, na=False)
            | df['Student ID'].str.contains(search_query, case=False, na=False)
        )
        df = df[mask]

    st.dataframe(df, width='stretch', hide_index=True)


# -------------------------------------------------------------------
# AUTH: LOGIN & REGISTRATION
# -------------------------------------------------------------------
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
    render_page_header(
        title="Faculty Authentication",
        subtitle="Sign in to your Present Call instructor console.",
        breadcrumb="Faculty Login",
        badge="Secure Auth"
    )

    # Centered enterprise login container
    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);
            margin-bottom: 24px;
        ">
            <h3 style="margin:0 0 4px 0; color:#0F172A; font-weight:700; font-size:1.25rem;">Teacher Login</h3>
            <p style="color:#64748B; font-size:0.85rem; margin:0 0 20px 0;">Enter your institutional credentials to proceed.</p>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='kiran')
        teacher_pass = st.text_input("Password", type='password', placeholder="••••••••")

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Sign In', type="primary", icon=':material/login:', shortcut='control+enter', width='stretch'):
                if login_teacher(teacher_username, teacher_pass):
                    st.toast("Welcome back!", icon="👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with btnc2:
            if st.button('Register Profile', type="secondary", icon=':material/person_add:', width='stretch'):
                st.session_state.teacher_login_type = 'register'
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required."
    if check_teacher_exists(teacher_username):
        return False, "Username is already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Profile successfully created! Please sign in."
    except Exception:
        return False, "Unexpected error occurred during registration."


def teacher_screen_register():
    render_page_header(
        title="Faculty Registration",
        subtitle="Register your instructor profile for course attendance management.",
        breadcrumb="Faculty Register",
        badge="New Account"
    )

    col_l, col_center, col_r = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.06);
            margin-bottom: 24px;
        ">
            <h3 style="margin:0 0 4px 0; color:#0F172A; font-weight:700; font-size:1.25rem;">Create Faculty Account</h3>
            <p style="color:#64748B; font-size:0.85rem; margin:0 0 20px 0;">Set up your credentials for classroom access.</p>
        """, unsafe_allow_html=True)

        teacher_username = st.text_input("Username", placeholder='e.g. kiran')
        teacher_name = st.text_input("Full Name", placeholder='e.g. Prof. Kiran Sharma')
        teacher_pass = st.text_input("Password", type='password', placeholder="••••••••")
        teacher_pass_confirm = st.text_input("Confirm Password", type='password', placeholder="••••••••")

        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
        btnc1, btnc2 = st.columns(2)

        with btnc1:
            if st.button('Register Now', type="primary", icon=':material/check_circle:', shortcut='control+enter', width='stretch'):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    import time
                    time.sleep(1.5)
                    st.session_state.teacher_login_type = "login"
                    st.rerun()
                else:
                    st.error(message)

        with btnc2:
            if st.button('Back to Login', type="secondary", icon=':material/arrow_back:', width='stretch'):
                st.session_state.teacher_login_type = 'login'
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    footer_dashboard()
