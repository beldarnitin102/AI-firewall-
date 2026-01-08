import random
import numpy as np

def generate_packets(count=5):
    packets = []
    for _ in range(count):
        packets.append([
            random.randint(100, 2000),          # packet size
            round(random.uniform(0.05, 5.0), 2),# duration
            random.choice([80, 443, 22, 21]),   # src port
            random.randint(40000, 60000)        # dst port
        ])
    return np.array(packets)
