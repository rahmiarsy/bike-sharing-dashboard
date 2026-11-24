from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")
sns.set_style("whitegrid")

# Load dataset relatif terhadap lokasi file dashboard.py
DATA_PATH = Path(__file__).parent / "main_data.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

df = load_data(DATA_PATH)

# --- SIDEBAR FILTER ---
st.sidebar.header("Filter Data")
min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Tanggal",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date],
)

selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim",
    options=["Spring", "Summer", "Fall", "Winter"],
    default=["Spring", "Summer", "Fall", "Winter"],
)

filtered_df = df[
    (df["dteday"].dt.date >= start_date)
    & (df["dteday"].dt.date <= end_date)
    & (df["season_label"].isin(selected_seasons))
]

# --- HEADER & KPI METRICS ---
st.title("🚲 Bike Sharing Analytics Dashboard (2011–2012)")
st.markdown("Dashboard interaktif hasil analisis penyewaan sepeda Capital Bikeshare.")

if filtered_df.empty:
    st.warning("Data kosong untuk kombinasi filter yang dipilih. Silakan ubah filter di sidebar.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
col2.metric("Pengguna Registered", f"{filtered_df['registered'].sum():,}")
col3.metric("Pengguna Casual", f"{filtered_df['casual'].sum():,}")

st.divider()

# --- VISUALISASI 1: TREN BULANAN & MUSIM ---
st.subheader("1. Tren Penyewaan Bulanan & Perbandingan Musim")
fig1, ax1 = plt.subplots(1, 2, figsize=(15, 5))

monthly_trend = (
    filtered_df.groupby(["year", "mnth"], observed=False)["cnt"].sum().reset_index()
)
sns.lineplot(
    data=monthly_trend,
    x="mnth",
    y="cnt",
    hue="year",
    marker="o",
    palette=["#95a5a6", "#1f77b4"],
    linewidth=2.5,
    ax=ax1[0],
)
ax1[0].set_title("Total Penyewaan Sepeda Bulanan", fontweight="bold")
ax1[0].set_xlabel("Bulan")
ax1[0].set_ylabel("Total Penyewaan")
ax1[0].set_xticks(range(1, 13))

season_order = ["Spring", "Summer", "Fall", "Winter"]
daily_season = (
    filtered_df.groupby(["dteday", "season_label"], observed=False)["cnt"]
    .sum()
    .reset_index()
)
season_avg = (
    daily_season.groupby("season_label", observed=False)["cnt"]
    .mean()
    .reindex(season_order)
    .fillna(0)
    .reset_index()
)
max_season = season_avg.loc[season_avg["cnt"].idxmax(), "season_label"]
bar_colors = ["#1f77b4" if s == max_season else "#d3d3d3" for s in season_avg["season_label"]]

sns.barplot(
    data=season_avg,
    x="season_label",
    y="cnt",
    hue="season_label",
    palette=bar_colors,
    legend=False,
    ax=ax1[1],
)
ax1[1].set_title("Rata-rata Penyewaan Harian per Musim", fontweight="bold")
ax1[1].set_xlabel("Musim")
ax1[1].set_ylabel("Rata-rata Penyewaan / Hari")

plt.tight_layout()
st.pyplot(fig1)

# --- VISUALISASI 2: POLA JAM SIBUK ---
st.subheader("2. Pola Jam Sibuk: Pengguna Registered vs Casual")
hourly_eda = (
    filtered_df.groupby(["day_type", "hr"], observed=False)[["casual", "registered"]]
    .mean()
    .reset_index()
)

fig2, ax2 = plt.subplots(1, 2, figsize=(15, 5), sharey=True)
for idx, dtype in enumerate(["Hari Kerja", "Akhir Pekan/Libur"]):
    subset = hourly_eda[hourly_eda["day_type"] == dtype]
    ax2[idx].plot(subset["hr"], subset["registered"], label="Registered", color="#1f77b4", linewidth=2.5)
    ax2[idx].plot(subset["hr"], subset["casual"], label="Casual", color="#ff7f0e", linewidth=2.5)
    ax2[idx].set_title(f"Pola Penyewaan per Jam ({dtype})", fontweight="bold")
    ax2[idx].set_xlabel("Jam (0 - 23)")
    ax2[idx].set_xticks(range(0, 24, 2))
    ax2[idx].legend()

ax2[0].set_ylabel("Rata-rata Penyewaan / Jam")
plt.tight_layout()
st.pyplot(fig2)

# --- VISUALISASI 3: ANALISIS LANJUTAN (BINNING / CLUSTERING) ---
st.subheader("3. Analisis Lanjutan: Distribusi Tingkat Permintaan per Kategori Waktu")
time_order = ["Dini Hari (00-05)", "Pagi (06-11)", "Siang-Sore (12-17)", "Malam (18-23)"]
demand_order = ["Low Demand", "Medium Demand", "High Demand"]

cluster_summary = (
    pd.crosstab(filtered_df["time_category"], filtered_df["demand_level"])
    .reindex(index=time_order, columns=demand_order, fill_value=0)
)

fig3, ax3 = plt.subplots(figsize=(10, 4))
cluster_summary.plot(
    kind="bar",
    stacked=True,
    color=["#d3d3d3", "#6baed6", "#08519c"],
    ax=ax3,
)
ax3.set_title("Proporsi Tingkat Permintaan Berdasarkan Kategori Waktu", fontweight="bold")
ax3.set_xlabel("Kategori Waktu")
ax3.set_ylabel("Jumlah Catatan Jam")
ax3.tick_params(axis="x", rotation=0)
plt.tight_layout()
st.pyplot(fig3)