import streamlit as st
import cv2
import numpy as np
import urllib.request
import time

# Refresh param untuk memicu rerun tanpa while loop
st.query_params["t"] = str(time.time())

st.title("Camera Snapshot Viewer")

ip_snapshot_url = st.text_input("IP Camera Snapshot URL", "http://192.168.89.120/cam-hi.jpg")

if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

# Tombol custom style
st.markdown("""
    <style>
    div.stButton > button:first-child {
        color: white !important;
        background-color: #2E86C1;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if not st.session_state.camera_active:
        if st.button("Start Snapshot Stream"):
            st.session_state.camera_active = True
            st.rerun()
    else:
        if st.button("Stop Snapshot Stream"):
            st.session_state.camera_active = False
            st.rerun()

if st.session_state.camera_active:
    outer_col1, outer_col2, outer_col3 = st.columns([1, 2, 1])
    with outer_col2:
        img_placeholder = st.empty()
        try:
            resp = urllib.request.urlopen(ip_snapshot_url)
            img_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_placeholder.image(frame, channels="RGB", width=750)
        except Exception as e:
            st.error(f"Gagal mengambil gambar: {e}")

    # Rerun otomatis tiap 0.2 detik
    time.sleep(0.2)
    st.rerun()
