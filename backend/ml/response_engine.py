from datetime import datetime

# In-memory blocklist (can later move to DB / Redis)
BLOCKED_SOURCES = {}

THREAT_THRESHOLD = 2  # number of detections before block

def evaluate_and_respond(packets, predictions):
    responses = []

    for i in range(len(predictions)):
        src_port = packets[i][2]

        if predictions[i] == -1:
            BLOCKED_SOURCES[src_port] = BLOCKED_SOURCES.get(src_port, 0) + 1

        action = "ALLOW"
        if BLOCKED_SOURCES.get(src_port, 0) >= THREAT_THRESHOLD:
            action = "BLOCK"

        responses.append({
            "packet": packets[i].tolist(),
            "prediction": "THREAT" if predictions[i] == -1 else "SAFE",
            "action": action,
            "timestamp": datetime.utcnow()
        })

    return responses
