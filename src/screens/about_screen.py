import streamlit as st
from src.components.navbar import top_navbar
from src.components.footer import footer_home
from src.components.stat_card import stat_row
from src.components.system_bar import render_page_header
from src.ui.base_layout import style_base_layout, style_background_dashboard


def _step_row(steps):
    inner = ""
    for i, (icon, title, desc) in enumerate(steps):
        inner += f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; min-width:140px; flex:1; text-align:center; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
            <div style="font-size:1.8rem; margin-bottom:6px;">{icon}</div>
            <div style="font-weight:700; color:#0F172A; font-size:0.92rem; font-family:'Plus Jakarta Sans', sans-serif;">{title}</div>
            <div style="color:#64748B; font-size:0.78rem; margin-top:4px; line-height:1.35;">{desc}</div>
        </div>
        """
        if i < len(steps) - 1:
            inner += f'<div style="display:flex; align-items:center; justify-content:center; color:#94A3B8; font-size:1.2rem; padding:0 4px;">&rarr;</div>'
    return f'<div style="display:flex; flex-wrap:wrap; gap:8px; align-items:stretch; margin:14px 0 26px 0;">{inner}</div>'


def about_screen():
    style_background_dashboard()
    style_base_layout()
    top_navbar()

    render_page_header(
        title="About Present Call",
        subtitle="Architecture, deep learning biometric pipelines, and institutional workflows.",
        breadcrumb="System Architecture",
        badge="Technical Specs"
    )

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-left:4px solid #2563EB; border-radius:14px; padding:20px 24px; box-shadow:0 1px 3px rgba(15,23,42,0.04); margin-bottom:24px;">
        <h3 style="margin:0 0 6px 0; color:#0F172A; font-size:1.2rem; font-weight:700;">AI Intelligent Attendance Platform</h3>
        <p style="color:#475569; font-size:0.92rem; line-height:1.55; margin:0;">
            Present Call is an enterprise AI-powered attendance platform built for academic universities, schools, and corporate institutions.
            It eliminates manual roll calls and proxy attendance with automated face and acoustic voice recognition — a single classroom group photo or short audio clip is enough to audit and mark an entire enrolled class present in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:20px 22px; box-shadow:0 1px 3px rgba(15,23,42,0.04); height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                <span style="font-size:1.3rem;">👥</span>
                <h3 style="margin:0; font-size:1.1rem; color:#0F172A; font-weight:700;">Who can use it?</h3>
            </div>
            <ul style="color:#475569; font-size:0.88rem; line-height:1.6; padding-left:18px; margin:0;">
                <li><b>Students</b> — Enroll once with a selfie snapshot (and optional voice sample), then track real-time attendance ratios and class presence.</li>
                <li><b>Faculty & Teachers</b> — Create courses, generate QR/join codes, and audit attendance via instant group photo recognition or voice roll-call.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:20px 22px; box-shadow:0 1px 3px rgba(15,23,42,0.04); height:100%;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:10px;">
                <span style="font-size:1.3rem;">⚙️</span>
                <h3 style="margin:0; font-size:1.1rem; color:#0F172A; font-weight:700;">How does it work?</h3>
            </div>
            <p style="color:#475569; font-size:0.88rem; line-height:1.6; margin:0;">
                A teacher captures a classroom group photo or audio clip. The neural vision pipeline detects every face in the scene, extracts 128-d biometric feature descriptors, performs high-dimensional nearest-neighbor matching against enrolled student vectors, resolves duplicate matches, and logs attendance into Supabase PostgreSQL.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
    st.subheader('Engine Specifications')
    st.markdown("<p style='color:#64748B; font-size:0.85rem; margin-top:-6px; margin-bottom:14px;'>Underlying production neural architecture and database infrastructure.</p>", unsafe_allow_html=True)

    stat_row([
        ('👁️', 'Face Embedding', '128-d', 'dlib ResNet descriptor'),
        ('🎙️', 'Voice Embedding', '256-d', 'Resemblyzer d-vector'),
        ('🔐', 'Auth Security', 'bcrypt', 'Salted password hashing'),
        ('☁️', 'Database Engine', 'Supabase', 'PostgreSQL + Row Level Security'),
    ])

    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    st.subheader('Student Workflow Journey')
    st.markdown(_step_row([
        ('📝', 'Scan & Enroll', 'Scan class QR code and enroll with a selfie'),
        ('👤', 'Biometric ID', 'Face (and voice) become your verified login'),
        ('📚', 'Course Roster', 'View every class you are enrolled in'),
        ('📊', 'Live Logs', 'Live attendance logs and audit timestamps'),
        ('📈', 'Analytics', 'Track attendance trajectory over time'),
    ]), unsafe_allow_html=True)

    st.subheader('Faculty Workflow Journey')
    st.markdown(_step_row([
        ('🔐', 'Teacher Sign In', 'Secure encrypted faculty login'),
        ('🏫', 'Course Admin', 'Create subjects and distribute join codes'),
        ('📸', 'Group Capture', 'One classroom photo or audio clip'),
        ('💾', 'Audit Detections', 'Review detections with match confidence'),
        ('📑', 'Export Reports', 'Comprehensive CSV reports and records'),
    ]), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
    st.subheader('Getting Started Guides')
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:20px 22px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
            <h4 style="margin:0 0 10px 0; color:#0F172A; font-size:1.02rem;">For Enrolled Students</h4>
            <ol style="color:#475569; font-size:0.86rem; line-height:1.65; margin:0; padding-left:18px;">
                <li>Scan your teacher's subject QR code or enter code</li>
                <li>Enter your full name and capture initial selfie</li>
                <li>Access your personal student dashboard</li>
                <li>Monitor your course attendance percentages</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:20px 22px; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
            <h4 style="margin:0 0 10px 0; color:#0F172A; font-size:1.02rem;">For Instructors & Faculty</h4>
            <ol style="color:#475569; font-size:0.86rem; line-height:1.65; margin:0; padding-left:18px;">
                <li>Register a faculty account in the Teacher Portal</li>
                <li>Create a subject and share the generated join code</li>
                <li>Capture or upload classroom photos during lectures</li>
                <li>Review AI detection confidence and save records</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    footer_home()
