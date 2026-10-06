import streamlit as st
from src.ui.base_layout import theme_colors, theme_toggle_button
from src.components.header import _logo

LANDING_PAGE_URL = "https://present-call.vercel.app/"


def top_navbar():
    """Persistent top navigation bar — rendered first on every screen
    (Home, About, Student, Teacher). Theme toggle always sits far right."""
    t = theme_colors()

    logo_col, back_col, home_col, about_col, student_col, teacher_col, spacer, toggle_col = st.columns(
        [2.0, 1.3, 0.8, 0.8, 1.3, 1.3, 1.0, 0.6]
    )

    with logo_col:
        html = f"""
<div style="display:flex; align-items:center; gap:10px; height:38px;">
{_logo(34)}
<span style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.05rem; color:{t['text']};">PRESENT CALL</span>
</div>
"""
        st.markdown(html, unsafe_allow_html=True)

    with back_col:
        st.link_button('Website', LANDING_PAGE_URL, type='tertiary', width='stretch',
                        icon=':material/arrow_back:')

    with home_col:
        if st.button('Home', key='nav_home', type='tertiary', width='stretch'):
            st.session_state.login_type = None
            st.session_state.page = 'home'
            st.rerun()

    with about_col:
        if st.button('About', key='nav_about', type='tertiary', width='stretch'):
            st.session_state.login_type = None
            st.session_state.page = 'about'
            st.rerun()

    with student_col:
        if st.button("I'm a Student", key='nav_student', type='tertiary', width='stretch'):
            st.session_state.login_type = 'student'
            st.rerun()

    with teacher_col:
        if st.button("I'm a Teacher", key='nav_teacher', type='tertiary', width='stretch'):
            st.session_state.login_type = 'teacher'
            st.rerun()

    with toggle_col:
        theme_toggle_button(key='theme_nav')

    st.markdown(
        f"<hr style='margin-top:-4px; margin-bottom:20px; border-color:{t['border']};'>",
        unsafe_allow_html=True
    )
