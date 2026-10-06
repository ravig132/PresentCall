import streamlit as st
from datetime import datetime

LANDING_PAGE_URL = "https://present-call.vercel.app/"

LOGO_SVG_SIDEBAR = """
<svg width="28" height="28" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="4" y="4" width="92" height="92" rx="26" fill="#1E293B" stroke="#38BDF8" stroke-width="5"/>
  <path d="M27 51 L43 67 L74 33" stroke="#38BDF8" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

def render_sidebar():
    """
    Renders the professional Present Call deep navy sidebar (#0B132B).
    Follows exact enterprise dashboard specifications:
    - Full height, deep navy background
    - Present Call logo & branding at top
    - Uppercase letter-spaced section labels
    - Active vs inactive state styling
    - Strictly preserves existing application navigation and state.
    """
    with st.sidebar:
        # Brand Header
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:11px; padding:6px 0 16px 0; border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:14px;">
            <div>{LOGO_SVG_SIDEBAR}</div>
            <div style="line-height:1.15;">
                <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.05rem; color:#FFFFFF; letter-spacing:0.02em;">PRESENT CALL</div>
                <div style="font-size:0.68rem; color:#94A3B8; letter-spacing:0.08em; text-transform:uppercase; font-weight:600;">Attendance Hub</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        login_type = st.session_state.get('login_type')

        # -------------------------------------------------------------
        # 1. TEACHER LOGGED IN
        # -------------------------------------------------------------
        if login_type == 'teacher' and 'teacher_data' in st.session_state:
            active_tab = st.session_state.get('current_teacher_tab', 'dashboard')

            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:10px 0 6px 4px;">OPERATIONS</p>', unsafe_allow_html=True)

            is_dash = (active_tab == 'dashboard')
            if st.button("Executive Overview", key="sb_t_dash", icon=":material/dashboard:", type="primary" if is_dash else "tertiary", width="stretch"):
                st.session_state.current_teacher_tab = 'dashboard'
                st.rerun()

            is_rec = (active_tab == 'attendance_records')
            if st.button("Attendance Records", key="sb_t_records", icon=":material/table_chart:", type="primary" if is_rec else "tertiary", width="stretch"):
                st.session_state.current_teacher_tab = 'attendance_records'
                st.rerun()

            is_ai = (active_tab == 'take_attendance')
            if st.button("AI Face Attendance", key="sb_t_ai", icon=":material/photo_camera:", type="primary" if is_ai else "tertiary", width="stretch"):
                st.session_state.current_teacher_tab = 'take_attendance'
                st.rerun()

            is_voice = (active_tab == 'voice_attendance')
            if st.button("Voice ID Roll-Call", key="sb_t_voice", icon=":material/mic:", type="primary" if is_voice else "tertiary", width="stretch"):
                st.session_state.current_teacher_tab = 'voice_attendance'
                st.rerun()

            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:16px 0 6px 4px;">MANAGEMENT</p>', unsafe_allow_html=True)

            is_sub = (active_tab == 'manage_subjects')
            if st.button("Manage Subjects", key="sb_t_subjects", icon=":material/menu_book:", type="primary" if is_sub else "tertiary", width="stretch"):
                st.session_state.current_teacher_tab = 'manage_subjects'
                st.rerun()

            is_dir = (active_tab == 'students_directory')
            if st.button("Students Directory", key="sb_t_dir", icon=":material/group:", type="primary" if is_dir else "tertiary", width="stretch"):
                st.session_state.current_teacher_tab = 'students_directory'
                st.rerun()

            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:16px 0 6px 4px;">FACULTY ACCOUNT</p>', unsafe_allow_html=True)
            teacher_name = st.session_state.teacher_data.get('name', 'Instructor')
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:8px 12px; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
                <div style="width:26px; height:26px; border-radius:50%; background:#2563EB; color:#FFF; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:700;">
                    {teacher_name[0].upper()}
                </div>
                <div style="font-size:0.83rem; color:#F8FAFC; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    {teacher_name}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Logout", key="sb_t_logout", icon=":material/logout:", type="secondary", width="stretch"):
                st.session_state['is_logged_in'] = False
                del st.session_state.teacher_data
                st.rerun()

        # -------------------------------------------------------------
        # 2. STUDENT LOGGED IN
        # -------------------------------------------------------------
        elif login_type == 'student' and 'student_data' in st.session_state:
            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:10px 0 6px 4px;">STUDENT PORTAL</p>', unsafe_allow_html=True)

            if st.button("My Attendance", key="sb_s_dash", icon=":material/dashboard:", type="primary", width="stretch"):
                st.rerun()

            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:16px 0 6px 4px;">ACCOUNT</p>', unsafe_allow_html=True)
            student_name = st.session_state.student_data.get('name', 'Student')
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:8px 12px; margin-bottom:8px; display:flex; align-items:center; gap:8px;">
                <div style="width:26px; height:26px; border-radius:50%; background:#10B981; color:#FFF; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:700;">
                    {student_name[0].upper()}
                </div>
                <div style="font-size:0.83rem; color:#F8FAFC; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    {student_name}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Logout", key="sb_s_logout", icon=":material/logout:", type="secondary", width="stretch"):
                st.session_state['is_logged_in'] = False
                del st.session_state.student_data
                st.rerun()

        # -------------------------------------------------------------
        # 3. NOT LOGGED IN / PORTAL CHOOSER / ABOUT
        # -------------------------------------------------------------
        else:
            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:10px 0 6px 4px;">PORTALS</p>', unsafe_allow_html=True)

            is_home = (login_type is None and st.session_state.get('page') != 'about')
            if st.button("Gateway Chooser", key="sb_nav_home", icon=":material/home:", type="primary" if is_home else "tertiary", width="stretch"):
                st.session_state.login_type = None
                st.session_state.page = 'home'
                st.rerun()

            is_std = (login_type == 'student')
            if st.button("Student Portal", key="sb_nav_std", icon=":material/school:", type="primary" if is_std else "tertiary", width="stretch"):
                st.session_state.login_type = 'student'
                st.rerun()

            is_tch = (login_type == 'teacher')
            if st.button("Teacher Portal", key="sb_nav_tch", icon=":material/person_apron:", type="primary" if is_tch else "tertiary", width="stretch"):
                st.session_state.login_type = 'teacher'
                st.rerun()

            st.markdown('<p style="font-size:0.72rem; letter-spacing:0.08em; color:#64748B; font-weight:700; margin:16px 0 6px 4px;">PLATFORM</p>', unsafe_allow_html=True)

            is_about = (st.session_state.get('page') == 'about' and login_type is None)
            if st.button("About Architecture", key="sb_nav_about", icon=":material/info:", type="primary" if is_about else "tertiary", width="stretch"):
                st.session_state.login_type = None
                st.session_state.page = 'about'
                st.rerun()

            st.link_button("Marketing Website", LANDING_PAGE_URL, icon=":material/arrow_outward:", type="tertiary", width="stretch")

        # Sidebar Footer: System Status
        st.markdown("""
        <div style="margin-top:28px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.08);">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10B981; box-shadow:0 0 8px rgba(16,185,129,0.8);"></span>
                <span style="font-size:0.75rem; color:#CBD5E1; font-weight:600;">Engine Online</span>
            </div>
            <div style="font-size:0.7rem; color:#64748B;">app.presentcall.ai · Enterprise Hub</div>
        </div>
        """, unsafe_allow_html=True)
