import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
THREAT_LOG_FILE = "threat_logs.csv"
@st.cache_data
def load_threat_data():
    try:
        df = pd.read_csv(THREAT_LOG_FILE)
        if df.empty:
            return None 
        return df
    except FileNotFoundError:
        return None 
def main():
    st.title("📊 Cybersecurity Threat Analytics Dashboard")
    threats = load_threat_data()

    if threats.empty:
        st.warning("No threats detected yet.")
        return

    st.subheader("🛑 Threat Severity Breakdown")
    severity_counts = threats["severity"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(severity_counts, labels=severity_counts.index, autopct='%1.1f%%', colors=['green', 'orange', 'red'], startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    st.subheader("⏳ Threats Detected Over Time")
    threats["timestamp"] = pd.to_datetime(threats["timestamp"])
    time_chart = px.line(threats, x="timestamp", y=threats.index, title="Threat Detection Timeline")
    st.plotly_chart(time_chart)
if __name__ == "__main__":
    main()
