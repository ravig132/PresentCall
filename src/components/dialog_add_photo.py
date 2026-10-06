import streamlit as st
from PIL import Image

@st.dialog("Capture or Upload Classroom Photos")
def add_photos_dialog():
    st.markdown("""
    <p style="color:#64748B; font-size:0.85rem; margin:0 0 14px 0;">
        Take optical snapshots via webcam or upload high-resolution classroom images to scan.
    </p>
    """, unsafe_allow_html=True)

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Optical Camera', type=type_camera, width='stretch', icon=':material/photo_camera:'):
            st.session_state.photo_tab = 'camera'
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload Images', type=type_upload, width='stretch', icon=':material/upload_file:'):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast('Photo Captured Successfully!', icon="📸")
            st.rerun()

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader('Choose classroom image files', type=['jpg', 'png', 'jpeg'], accept_multiple_files=True, key='dialog_upload')

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            st.toast(f'{len(uploaded_files)} Photo(s) Added!', icon="🖼️")
            st.rerun()

    st.divider()
    if st.button('Done & Return to Session', type='primary', width='stretch', icon=':material/check:'):
        st.rerun()
