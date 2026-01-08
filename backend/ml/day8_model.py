import pandas as pd
from sklearn.ensemble import IsolationForest

data = pd.read_csv("../data/processed_logs.csv")

model = IsolationForest(contamination=0.3, random_state=42)
model.fit(data)

data["anomaly"] = model.predict(data)

print(data)
