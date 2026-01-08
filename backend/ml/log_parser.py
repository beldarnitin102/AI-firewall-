import pandas as pd

# Load raw logs
df = pd.read_csv("../data/real_network_logs.csv")

# Feature selection
features = df[["duration", "src_bytes", "dst_bytes"]]

# Save processed data
features.to_csv("../data/processed_logs.csv", index=False)

print("✅ Logs processed successfully")
