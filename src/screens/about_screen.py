import streamlit as st
from src.components.navbar import top_navbar
from src.components.footer import footer_home
from src.components.stat_card import stat_row
from src.ui.base_layout import style_base_layout, style_background_dashboard, theme_colors


def _step_row(steps):
    t = theme_colors()
    inner = ""
    for i, (icon, title, desc) in enumerate(steps):
        inner += f"""
<div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:16px; padding:16px; min-width:140px; flex:1; text-align:center;">
<div style="font-size:1.6rem;">{icon}</div>
<div style="font-weight:700; color:{t['text']}; margin-top:6px; font-size:0.9rem;">{title}</div>
<div style="color:{t['text_secondary']}; font-size:0.76rem; margin-top:4px;">{desc}</div>
</div>
"""
        if i < len(steps) - 1:
            inner += f'<div style="display:flex; align-items:center; color:{t["text_secondary"]}; font-size:1.3rem; padding:0 4px;">&rarr;</div>'
    return f'<div style="display:flex; flex-wrap:wrap; gap:6px; align-items:stretch; margin:14px 0 26px 0;">{inner}</div>'


def about_screen():
    style_background_dashboard()
    style_base_layout()
    top_navbar()

    t = theme_colors()

    st.header('About Present Call')
    st.markdown(
        f'<p style="color:{t["text_secondary"]}; max-width:820px; font-size:1rem;">'
        'Present Call is an AI-powered attendance platform built for schools and colleges. '
        'It replaces manual roll calls and proxy attendance with automated face and voice '
        'recognition — one group photo or one audio clip is enough to mark an entire class present.'
        '</p>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader('Who can use it?')
        st.markdown(
            "- **Students** — enroll once with a selfie (and optionally a voice sample), "
            "then check attendance anytime.\n"
            "- **Teachers** — create subjects, share a join code, and take attendance "
            "with one photo or one audio clip."
        )
    with c2:
        st.subheader('How does it work?')
        st.markdown(
            "A teacher captures a single group photo or a short classroom recording. "
            "The system detects every face or voice in it, matches each one against "
            "the enrolled class roster using deep learning embeddings, removes duplicate "
            "detections, and logs attendance automatically."
        )

    st.divider()

    st.header('Engine Specs')
    st.markdown(
        f'<p style="color:{t["text_secondary"]}; font-size:0.9rem; margin-bottom:14px;">'
        'The real architecture behind Present Call — no inflated numbers, just what the models actually output.'
        '</p>',
        unsafe_allow_html=True
    )
    stat_row([
        ('👁️', 'Face Embedding', '128-d', 'dlib ResNet descriptor'),
        ('🎙️', 'Voice Embedding', '256-d', 'Resemblyzer d-vector'),
        ('🔐', 'Auth', 'bcrypt', 'Salted password hashing'),
        ('☁️', 'Database', 'Supabase', 'PostgreSQL + Row Level Security'),
    ])

    st.divider()

    st.header('Student Journey')
    st.markdown(_step_row([
        ('📝', 'Register / Login', 'Scan a class QR code and enroll with a selfie'),
        ('👤', 'Student Profile', 'Your face (and voice) become your login'),
        ('📚', 'View Subjects', 'See every class you are enrolled in'),
        ('📊', 'View Attendance', 'Live attendance logs, subject by subject'),
        ('📈', 'Analyze', 'Track your attendance percentage over time'),
    ]), unsafe_allow_html=True)

    st.header('Teacher Journey')
    st.markdown(_step_row([
        ('🔐', 'Register / Login', 'Create a secure teacher account'),
        ('🏫', 'Manage Subjects', 'Create classes and share join codes'),
        ('📸', 'Take Attendance', 'One group photo or one audio clip'),
        ('💾', 'Save Records', 'Review detections before confirming'),
        ('📑', 'View Reports', 'Attendance analytics per subject'),
    ]), unsafe_allow_html=True)

    st.divider()

    st.header('Getting Started')
    c1, c2 = st.columns(2)
    with c1:
        st.subheader('For Students')
        st.markdown(
            "1. Scan your teacher's subject QR code\n"
            "2. Enter your details and take a selfie\n"
            "3. Access your student dashboard\n"
            "4. View subject-wise attendance\n"
            "5. Monitor your attendance percentage"
        )
    with c2:
        st.subheader('For Teachers')
        st.markdown(
            "1. Register a teacher account\n"
            "2. Create a subject and share the join code\n"
            "3. Add students, or let them self-enroll\n"
            "4. Take attendance each class\n"
            "5. Review and save attendance\n"
            "6. Check attendance analytics anytime"
        )

    footer_home()
