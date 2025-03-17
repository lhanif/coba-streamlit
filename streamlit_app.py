import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi layout
st.set_page_config(page_title="Aplikasi Streamlit Sederhana", layout="wide")

# Judul aplikasi
st.title("Aplikasi Streamlit Sederhana")

# Sidebar untuk navigasi
st.sidebar.header("Navigasi")
page = st.sidebar.selectbox("Pilih Halaman", ["Beranda", "Visualisasi", "Tentang"])

if page == "Beranda":
    st.header("Selamat Datang!")
    user_input = st.text_input("Masukkan nama Anda:")
    if st.button("Submit"):
        st.success(f"Halo, {user_input}!")

    number = st.slider("Pilih angka:", 1, 100, 50)
    st.write(f"Angka yang dipilih: {number}")

    if st.checkbox("Tampilkan gambar"):
        st.image("https://via.placeholder.com/150", caption="Contoh Gambar")

elif page == "Visualisasi":
    st.header("Visualisasi Data")
    data = pd.DataFrame({
        "Kategori": ["A", "B", "C", "D"],
        "Nilai": [10, 20, 30, 40]
    })

    fig, ax = plt.subplots()
    ax.bar(data["Kategori"], data["Nilai"], color='skyblue')
    st.pyplot(fig)

elif page == "Tentang":
    st.header("Tentang Aplikasi")
    st.write("Aplikasi ini dibuat dengan Streamlit untuk demonstrasi UI yang sederhana dan interaktif.")
