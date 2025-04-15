import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from pymongo import MongoClient
import time

# Koneksi MongoDB
MONGO_URI = "mongodb+srv://symbiot:horehore@sensor.hh6drjg.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["sensor"]
collection = db["data_sensor"]

def get_latest_data(limit=10):
    cursor = collection.find().sort("timestamp", -1).limit(limit)
    df = pd.DataFrame(cursor)
    if not df.empty and "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])  # Pastikan tipe datetime
        df = df.sort_values("timestamp")
    return df

def plot_graph(title, x, y, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', line=dict(color=color)))
    fig.update_layout(title=title, xaxis_title="Time", yaxis_title=title)
    return fig

def run():
    st.markdown("<h1 style='text-align: center;'>DASHBOARD BOMBATRONIC</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3><b>System Status:</b> <span style='color: green;'>On</span></h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("<h3><b>Threat Level:</b> <span style='color: green;'>Safe</span></h3>", unsafe_allow_html=True)

    placeholder = st.empty()  # Placeholder to update content

    while True:
        df = get_latest_data()

        if df.empty:
            st.warning("Belum ada data tersedia.")
            break

        # Mengambil 10 titik terakhir pada grafik
        x = df['timestamp'].dt.strftime("%H:%M:%S") if 'timestamp' in df.columns else list(range(len(df)))
        y1 = df["CO"] if "CO" in df else [0]*len(x)
        y2 = df["CO2"] if "CO2" in df else [0]*len(x)
        y3 = df["temperature"] if "temperature" in df else [0]*len(x)
        y4 = df["humidity"] if "humidity" in df else [0]*len(x)

        # Gunakan placeholder untuk mengganti konten setelah 10 detik
        with placeholder.container():
            col1, col2 = st.columns(2)
            col1.plotly_chart(plot_graph("CO", x, y1, "blue"), use_container_width=True)
            col2.plotly_chart(plot_graph("CO2", x, y2, "orange"), use_container_width=True)

            col1, col2 = st.columns(2)
            col1.plotly_chart(plot_graph("Temperature", x, y3, "green"), use_container_width=True)
            col2.plotly_chart(plot_graph("Humidity", x, y4, "black"), use_container_width=True)

            st.markdown("<h3>Recent Readings</h3>", unsafe_allow_html=True)
            # Menampilkan seluruh data dalam tabel
            st.dataframe(df[["CO", "CO2", "temperature", "humidity", "timestamp"]])

        time.sleep(10)  # Delay before next update
        placeholder.empty()  # Clear the placeholder for next update

if __name__ == "__main__":
    run()
