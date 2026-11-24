# Bike Sharing Analytics Dashboard 🚲

Proyek analisis data dan dashboard interaktif menggunakan dataset **Capital Bikeshare (2011–2012)** untuk mengeksplorasi tren penyewaan berdasarkan musim, perbandingan pola jam sibuk antara pengguna *casual* dan *registered*, serta pengelompokan tingkat permintaan (*binning*).

## Struktur Direktori
- `dashboard/`: Berisi aplikasi Streamlit (`dashboard.py`) dan data bersih (`main_data.csv`).
- `data/`: Berisi dataset mentah (`day.csv` dan `hour.csv`).
- `notebook.ipynb`: Jupyter/Colab Notebook yang memuat seluruh proses analisis data.
- `requirements.txt`: Daftar *library* Python yang dibutuhkan.
- `url.txt`: Tautan menuju aplikasi Streamlit Cloud yang telah di-*deploy*.

## Cara Menjalankan Dashboard di Local

1. Pastikan Python sudah terinstal, lalu instal seluruh dependensi:
   ```bash
   pip install -r requirements.txt