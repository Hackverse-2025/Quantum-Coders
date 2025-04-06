import streamlit as st
import pandas as pd
import os
import hashlib
import logging
from datetime import datetime
from plyer import notification
LOG_FILE = "threat_activity.log"
THREAT_LOG_FILE = "threat_logs.csv"
ALLOWED_USERS = ["admin", "cybersec", "prabh"]
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
def log_event(level, message):
    logging.log(level, message)
    print(message)
def get_file_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        log_event(logging.ERROR, f"File not found: {file_path}")
        return None
SCRIPT_PATH = os.path.abspath(__file__)
SCRIPT_HASH = get_file_hash(SCRIPT_PATH)
ORIGINAL_LOG_HASH = get_file_hash(THREAT_LOG_FILE)
def verify_script_integrity():
    if get_file_hash(SCRIPT_PATH) != SCRIPT_HASH:
        log_event(logging.ERROR, "⚠️ Script Integrity Compromised!")
        st.error("⚠️ Script Integrity Compromised!")
        st.stop()
def verify_threat_log_integrity():
    if get_file_hash(THREAT_LOG_FILE) != ORIGINAL_LOG_HASH:
        log_event(logging.CRITICAL, "⚠️ Threat Logs Modified!")
        st.error("⚠️ Threat Logs Modified!")
        st.stop()
@st.cache_data(show_spinner=False)
def load_threat_data(clear_cache=False):
    if clear_cache:
        st.cache_data.clear()
    if not os.path.exists(THREAT_LOG_FILE):
        log_event(logging.ERROR, "⚠️ Threat logs file is missing!")
        return pd.DataFrame(columns=["threat_id", "severity", "status"])
    verify_threat_log_integrity()
    return pd.read_csv(THREAT_LOG_FILE)
def authenticate_user():
    current_user = os.getenv("USER") or os.getenv("USERNAME") or "unknown"
    if current_user not in ALLOWED_USERS:
        log_event(logging.WARNING, f"Unauthorized access attempt by {current_user}")
        st.error("🚫 Access Denied! Unauthorized user.")
        st.stop()
def kill_threat(threat_id):
    log_event(logging.WARNING, f"Neutralized Critical Threat: {threat_id}")
    st.success(f"✅ Threat {threat_id} neutralized!")
    notification.notify(
        title="Threat Neutralized",
        message=f"Critical Threat {threat_id} has been neutralized!",
        timeout=5
    )
def main():
    authenticate_user()
    verify_script_integrity()
    st.title("🔒 AI-Driven Cybersecurity Threat Detection Bot")
    st.sidebar.header("Settings")
    if "refresh_trigger" not in st.session_state:
        st.session_state.refresh_trigger = 0

    if st.sidebar.button("🔄 Refresh Data"):
        st.session_state.refresh_trigger += 1
        st.rerun()
    threats = load_threat_data(clear_cache=st.session_state.refresh_trigger > 0)
    st.write("### Real-Time Threat Detection Dashboard")
    st.table(threats)
    st.write(f"**Total Threats Detected:** {len(threats)}")
    if "severity" in threats.columns and "threat_id" in threats.columns:
        critical_threats = threats[threats['severity'].str.lower() == 'critical']
        if not critical_threats.empty:
            log_event(logging.CRITICAL, "🚨 Critical Threats Detected!")
            st.error("🚨 **Critical Threats Detected!**")
            st.table(critical_threats)
            for _, threat in critical_threats.iterrows():
                threat_id = threat['threat_id']
                log_event(logging.CRITICAL, f"⚠️ Detected Critical Threat: {threat_id}")
                notification.notify(
                    title="🚨 Critical Threat Detected!",
                    message=f"Threat {threat_id} requires immediate action!",
                    timeout=5
                )
                if st.button(f"🛑 Neutralize Threat {threat_id}"):
                    kill_threat(threat_id)

if __name__ == "__main__":
    main()
