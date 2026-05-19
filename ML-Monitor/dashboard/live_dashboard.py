import streamlit as st
import pandas as pd
import psutil
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from pathlib import Path

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="ML Monitor Dashboard",
    layout="wide"
)

st.title("🔍 ML Monitor - Live Dashboard")

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:

    st.header("⚙ Configuration")

    refresh_rate = st.slider(
        "Refresh Rate (seconds)",
        1,
        30,
        5
    )

    selected_metric = st.selectbox(
        "Metric",
        [
            "CPU",
            "Memory",
            "Processes"
        ]
    )

# ==========================================
# LIVE SYSTEM METRICS
# ==========================================
cpu_usage = psutil.cpu_percent(interval=1)

memory = psutil.virtual_memory()
memory_usage = memory.percent

process_count = len(psutil.pids())

# ==========================================
# ALERT COUNT
# ==========================================
alert_file = Path("../data/alerts/alerts.log")

alert_count = 0

if alert_file.exists():

    with open(alert_file, "r", encoding="utf-8") as f:
        alerts = f.readlines()

    alert_count = len(alerts)

# ==========================================
# TOP METRIC CARDS
# ==========================================
col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "CPU Usage",
        f"{cpu_usage:.1f}%"
    )

with col2:

    st.metric(
        "Memory Usage",
        f"{memory_usage:.1f}%"
    )

with col3:

    st.metric(
        "Alerts",
        str(alert_count)
    )

# ==========================================
# CHART DATA
# ==========================================
st.subheader("📈 Live Performance")

times = pd.date_range(
    end=datetime.now(),
    periods=30,
    freq="1min"
)

cpu_history = [
    psutil.cpu_percent(interval=0.05)
    for _ in range(30)
]

memory_history = [
    psutil.virtual_memory().percent
    for _ in range(30)
]

chart_data = pd.DataFrame({
    "Time": times,
    "CPU": cpu_history,
    "Memory": memory_history
})

# ==========================================
# PLOTLY GRAPH
# ==========================================
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=chart_data["Time"],
    y=chart_data["CPU"],
    mode='lines',
    name='CPU Usage'
))

fig.add_trace(go.Scatter(
    x=chart_data["Time"],
    y=chart_data["Memory"],
    mode='lines',
    name='Memory Usage'
))

fig.update_layout(
    height=400,
    xaxis_title="Time",
    yaxis_title="Usage %",
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# PROCESS TABLE
# ==========================================
st.subheader("🧠 Top Processes")

process_data = []

for proc in psutil.process_iter([
    'pid',
    'name',
    'cpu_percent',
    'memory_percent'
]):

    try:

        process_data.append({
            "PID": proc.info['pid'],
            "Name": proc.info['name'],
            "CPU %": proc.info['cpu_percent'],
            "Memory %": round(
                proc.info['memory_percent'],
                2
            )
        })

    except:
        continue

df = pd.DataFrame(process_data)

df = df.sort_values(
    by="CPU %",
    ascending=False
).head(10)

st.dataframe(
    df,
    use_container_width=True
)

# ==========================================
# ALERT LOGS
# ==========================================
st.subheader("🚨 Recent Alerts")

if alert_file.exists():

    with open(alert_file, "r", encoding="utf-8") as f:

        log_lines = f.readlines()

    latest_logs = log_lines[-10:]

    for line in reversed(latest_logs):

        st.error(line.strip())

else:

    st.success("No alerts detected")

# ==========================================
# REFRESH BUTTON
# ==========================================
if st.button("🔄 Refresh Dashboard"):

    st.rerun()

# ==========================================
# AUTO REFRESH
# ==========================================
time.sleep(refresh_rate)

st.rerun()