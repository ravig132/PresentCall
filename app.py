
import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen
from src.screens.about_screen import about_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='Present Call — AI Intelligent Attendance System',
        page_icon="assets/favicon.png",
        layout='wide'
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = 'home'

    # Deep-link support: the external landing page (present-call.vercel.app)
    # can link directly to https://presentcall.streamlit.app/?portal=student
    # or ?portal=teacher to skip the chooser entirely. Only applied once,
    # on first load, so it doesn't fight with in-app navigation afterwards.
    if not st.session_state.get('_portal_param_checked'):
        st.session_state['_portal_param_checked'] = True
        portal_param = st.query_params.get('portal')
        if portal_param in ('student', 'teacher'):
            st.session_state['login_type'] = portal_param

    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()

        case 'student':
            student_screen()

        case None:
            if st.session_state['page'] == 'about':
                about_screen()
            else:
                home_screen()


    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)
main()
