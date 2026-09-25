import streamlit as st
from src.components.navbar import top_navbar
from src.components.header import hero_header
from src.components.footer import footer_home
from src.ui.base_layout import style_base_layout, style_background_home, theme_colors

# NOTE: This screen is intentionally minimal. Full marketing copy (what the
# product is, why it matters, feature highlights) now lives on the Vercel
# landing page (present-call.vercel.app), which is the actual front door
# most people arrive through. Duplicating that pitch here would mean
# maintaining the same content in two places. This screen's only job is:
# let someone already inside the app pick a portal.

STUDENT_ICON = """
<svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 3L1 8.5 12 14l9-4.5V15h2V8.5L12 3z" fill="{accent}"/>
<path d="M5 12.6v3.9c0 .5.3 1 .8 1.3L12 21l6.2-3.2c.5-.3.8-.8.8-1.3v-3.9l-7 3.5-7-3.5z" fill="{text}"/>
</svg>
"""

TEACHER_ICON = """
<svg width="100" height="100" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="2" y="4" width="20" height="13" rx="2.2" stroke="{text}" stroke-width="1.6"/>
<path d="M8 20.5h8M12 17v3.5" stroke="{text}" stroke-width="1.6" stroke-linecap="round"/>
<path d="M6.5 13l3-3.2 2.2 2 4.3-4.3" stroke="{accent}" stroke-width="2.1" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


def home_screen():
    style_background_home()
    style_base_layout()
    top_navbar()
    hero_header()

    t = theme_colors()

    st.markdown(
        f'<p style="text-align:center; color:{t["text_secondary"]}; margin:0 0 24px 0; font-size:0.95rem;">Choose your portal to continue</p>',
        unsafe_allow_html=True
    )

    with st.container(key="hero_cards"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.header("I'm Student")
            icon_html = f'<div style="text-align:center; margin:6px 0 16px 0;">{STUDENT_ICON.format(accent=t["accent"], text=t["text"])}</div>'
            st.markdown(icon_html, unsafe_allow_html=True)
            if st.button('Student Portal', type='primary', width='stretch',
                          icon=':material/arrow_outward:', icon_position='right'):
                st.session_state['login_type'] = 'student'
                st.rerun()

        with col2:
            st.header("I'm Teacher")
            icon_html = f'<div style="text-align:center; margin:6px 0 16px 0;">{TEACHER_ICON.format(accent=t["accent"], text=t["text"])}</div>'
            st.markdown(icon_html, unsafe_allow_html=True)
            if st.button('Teacher Portal', type='primary', width='stretch',
                          icon=':material/arrow_outward:', icon_position='right'):
                st.session_state['login_type'] = 'teacher'
                st.rerun()

    footer_home()
