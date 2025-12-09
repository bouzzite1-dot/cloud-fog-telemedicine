import numpy as np
import requests
import time
import zlib
from scipy.signal import butter, filtfilt
import json

# ===========================
# 1. Filtre passe-bas Butterworth
# ===========================
def lowpass_filter(data, cutoff=40, fs=250, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return filtfilt(b, a, data)

# ===========================
# 2. Compression des données
# ===========================
def compress_data(data):
    data_bytes = json.dumps(data.tolist()).encode("utf-8")
    compressed = zlib.compress(data_bytes)
    return compressed

# ===========================
# 3. Envoi vers le Cloud
# ===========================
def send_to_cloud(compressed_data, cloud_url):
    headers = {"Content-Type": "application/octet-stream"}
    start = time.time()
    response = requests.post(cloud_url, data=compressed_data, headers=headers)
    end = time.time()

    return response.status_code, (end - start)

# ===========================
# 4. Pipeline Fog Node
# ===========================
def fog_pipeline(data, cloud_url):
    times = {}

    # Filtrage
    t0 = time.time()
    filtered = lowpass_filter(data)
    times["filtering_time"] = time.time() - t0

    # Compression
    t1 = time.time()
    compressed = compress_data(filtered)
    times["compression_time"] = time.time() - t1

    # Envoi Cloud
    status, upload_time = send_to_cloud(compressed, cloud_url)
    times["upload_time"] = upload_time
    times["status"] = status

    return times

# ===========================
# 5. Exécution principale
# ===========================
if __name__ == "__main__":
    print("==== Fog Node Started ====")

    # Simulation des données ECG (1000 points)
    sample_data = np.sin(np.linspace(0, 10, 1000))

    cloud_endpoint = "https://cloud-server-medical.com/upload"

    results = fog_pipeline(sample_data, cloud_endpoint)

    print("Fog Node Performance:")
    for key, value in results.items():
        print(f"{key}: {value}")
