import streamlit as st
import segno
import io

@st.dialog("Course Enrollment QR & Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "presentcall.streamlit.app"
    join_url = f"https://{app_domain}/?join-code={subject_code}"

    st.markdown(f"""
    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:12px 14px; margin-bottom:14px;">
        <div style="font-weight:700; color:#0F172A; font-size:1.05rem;">{subject_name}</div>
        <div style="font-size:0.8rem; color:#64748B;">Share this instant join link or QR code with your enrolled class.</div>
    </div>
    """, unsafe_allow_html=True)

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns([1, 1], gap="medium")

    with col1:
        st.markdown("<p style='font-weight:600; font-size:0.88rem; color:#0F172A; margin-bottom:4px;'>Course Code</p>", unsafe_allow_html=True)
        st.code(subject_code, language="text")

        st.markdown("<p style='font-weight:600; font-size:0.88rem; color:#0F172A; margin-bottom:4px;'>Direct Join Link</p>", unsafe_allow_html=True)
        st.code(join_url, language="text")
        st.caption('Distribute this link via WhatsApp, Email, or LMS.')

    with col2:
        st.markdown("<p style='font-weight:600; font-size:0.88rem; color:#0F172A; margin-bottom:4px;'>Scan QR to Self-Enroll</p>", unsafe_allow_html=True)
        st.image(out.getvalue(), use_container_width=True)
