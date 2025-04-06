import pandas as pd
import random
import time
LOG_FILE = "threat_logs.csv"
threat_types = [
    ("Phishing Attempt", "low"),
    ("Malware Infection", "medium"),
    ("DDoS Attack", "high"),
    ("Unauthorized Login", "medium"),
    ("Privilege Escalation", "critical"),
    ("Ransomware Attack", "critical"),
    ("SQL Injection", "high"),
    ("Zero-Day Exploit", "critical"),
]
def generate_fake_threat():
    timestamp = pd.Timestamp.now()
    threat, severity = random.choice(threat_types)
    source_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
    return [timestamp, source_ip, threat, severity]
def simulate_threat_activity():
    while True:
        df = pd.DataFrame(columns=["timestamp", "source_ip", "threat_type", "severity"])
        for _ in range(random.randint(1, 5)):
            df.loc[len(df)] = generate_fake_threat()
        df.to_csv(LOG_FILE, index=False)
        print(f"Generated {len(df)} threats.")
        time.sleep(random.randint(5, 15))

if __name__ == "__main__":
    simulate_threat_activity()
