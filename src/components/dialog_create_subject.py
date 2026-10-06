import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Academic Subject")
def create_subject_dialog(teacher_id):
    st.markdown("""
    <p style="color:#64748B; font-size:0.85rem; margin:0 0 14px 0;">
        Enter course parameters to generate a unique enrollment code and roster.
    </p>
    """, unsafe_allow_html=True)

    sub_id = st.text_input("Course Code", placeholder="e.g. CS101")
    sub_name = st.text_input("Course Name", placeholder="e.g. Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="e.g. Section A")

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    if st.button("Create Course", type='primary', width='stretch', icon=':material/add_circle:'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject Created Successfully!", icon="🎉")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all required course fields.")
