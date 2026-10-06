import streamlit as st
from src.components.navbar import top_navbar
from src.components.footer import footer_home
from src.components.system_bar import render_page_header
from src.ui.base_layout import style_base_layout, style_background_home

STUDENT_ICON_SVG = """
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 3L1 8.5 12 14l9-4.5V15h2V8.5L12 3z" fill="#2563EB"/>
  <path d="M5 12.6v3.9c0 .5.3 1 .8 1.3L12 21l6.2-3.2c.5-.3.8-.8.8-1.3v-3.9l-7 3.5-7-3.5z" fill="#0F172A"/>
</svg>
"""

TEACHER_ICON_SVG = """
<svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="2" y="4" width="20" height="13" rx="2.2" stroke="#0F172A" stroke-width="1.8"/>
  <path d="M8 20.5h8M12 17v3.5" stroke="#0F172A" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M6.5 13l3-3.2 2.2 2 4.3-4.3" stroke="#2563EB" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

def home_screen():
    style_background_home()
    style_base_layout()
    top_navbar()

    render_page_header(
        title="Institutional Attendance Gateway",
        subtitle="Select your access portal to enter the Present Call attendance management hub.",
        breadcrumb="Portal Gateway",
        badge="Engine Online"
    )

    with st.container(key="hero_cards"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(f"""
            <div style="text-align:center; margin-bottom:12px;">
                <div style="width:68px; height:68px; border-radius:18px; background:#EFF6FF; border:1px solid #DBEAFE; display:inline-flex; align-items:center; justify-content:center; margin-bottom:12px;">
                    {STUDENT_ICON_SVG}
                </div>
                <h2 style="font-size:1.55rem !important; color:#0F172A !important; margin:0 0 6px 0 !important; font-weight:700;">Student Portal</h2>
                <p style="color:#64748B; font-size:0.88rem; margin:0 0 16px 0;">
                    Biometric access for enrolled learners to track personal course attendance.
                </p>
                <div style="text-align:left; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:12px 14px; margin-bottom:18px;">
                    <div style="font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        <span style="color:#10B981; font-weight:700;">✓</span> FaceID single-glance biometric login
                    </div>
                    <div style="font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        <span style="color:#10B981; font-weight:700;">✓</span> Real-time attendance ratios & activity logs
                    </div>
                    <div style="font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:8px;">
                        <span style="color:#10B981; font-weight:700;">✓</span> Fast course self-enrollment via join codes
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button('Launch Student Portal', key='home_btn_student', type='primary', width='stretch',
                          icon=':material/arrow_forward:', icon_position='right'):
                st.session_state['login_type'] = 'student'
                st.rerun()

        with col2:
            st.markdown(f"""
            <div style="text-align:center; margin-bottom:12px;">
                <div style="width:68px; height:68px; border-radius:18px; background:#F0FDF4; border:1px solid #DCFCE7; display:inline-flex; align-items:center; justify-content:center; margin-bottom:12px;">
                    {TEACHER_ICON_SVG}
                </div>
                <h2 style="font-size:1.55rem !important; color:#0F172A !important; margin:0 0 6px 0 !important; font-weight:700;">Teacher Portal</h2>
                <p style="color:#64748B; font-size:0.88rem; margin:0 0 16px 0;">
                    Faculty console for AI optical attendance, voice roll-call, and course audit logs.
                </p>
                <div style="text-align:left; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:12px 14px; margin-bottom:18px;">
                    <div style="font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        <span style="color:#2563EB; font-weight:700;">✓</span> Instant classroom group photo face recognition
                    </div>
                    <div style="font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                        <span style="color:#2563EB; font-weight:700;">✓</span> Voice ID acoustic roll-call verification
                    </div>
                    <div style="font-size:0.8rem; color:#475569; display:flex; align-items:center; gap:8px;">
                        <span style="color:#2563EB; font-weight:700;">✓</span> Course management, join codes & CSV export
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button('Launch Teacher Portal', key='home_btn_teacher', type='primary', width='stretch',
                          icon=':material/arrow_forward:', icon_position='right'):
                st.session_state['login_type'] = 'teacher'
                st.rerun()

    # System Architecture Highlights Row
    st.markdown("""
    <div style="
        margin-top: 26px;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 20px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 1px 2px rgba(15,23,42,0.03);
    ">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.1rem;">👁️</span>
            <div>
                <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase;">Vision Model</div>
                <div style="font-size:0.85rem; font-weight:700; color:#0F172A;">128-d ResNet Embeddings</div>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.1rem;">🎙️</span>
            <div>
                <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase;">Acoustic Model</div>
                <div style="font-size:0.85rem; font-weight:700; color:#0F172A;">256-d Resemblyzer d-vector</div>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.1rem;">🔐</span>
            <div>
                <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase;">Security & DB</div>
                <div style="font-size:0.85rem; font-weight:700; color:#0F172A;">PostgreSQL RLS + bcrypt</div>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.1rem;">⚡</span>
            <div>
                <div style="font-size:0.75rem; color:#64748B; font-weight:600; text-transform:uppercase;">Latency</div>
                <div style="font-size:0.85rem; font-weight:700; color:#0F172A;">Under 800ms Roll-Call</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    footer_home()
