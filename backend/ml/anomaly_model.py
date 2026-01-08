import numpy as np
from sklearn.ensemble import IsolationForest

# Sample training data (packet behavior)
# [packet_size, duration, src_port, dst_port]
TRAIN_DATA = np.array([
    [500, 0.1, 443, 52344],
    [520, 0.2, 80, 51234],
    [480, 0.15, 443, 53421],
    [1500, 3.5, 22, 44444],
    [1600, 4.0, 22, 55555],
])

model = IsolationForest(
    contamination=0.3,
    random_state=42
)

model.fit(TRAIN_DATA)
