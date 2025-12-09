import speedtest
import csv
import time
from datetime import datetime

output_file = "bandwidth_results.csv"

def test_bandwidth():
    st = speedtest.Speedtest()
    download = st.download() / 1_000_000  # Mbps
    upload = st.upload() / 1_000_000      # Mbps
    ping = st.results.ping                # ms
    
    return download, upload, ping

def save_results(download, upload, ping):
    header = ["timestamp", "download_mbps", "upload_mbps", "latency_ms"]
    exists = False
    
    try:
        with open(output_file, "r"):
            exists = True
    except FileNotFoundError:
        pass
    
    with open(output_file, "a", newline="") as file:
        writer = csv.writer(file)
        if not exists:
            writer.writerow(header)

        writer.writerow([datetime.now(), download, upload, ping])

if __name__ == "__main__":
    print("=== Mesure de la bande passante ===")

    for i in range(5):
        download, upload, ping = test_bandwidth()
        print(f"Test {i+1} -> ↓ {download:.2f} Mbps | ↑ {upload:.2f} Mbps | Ping: {ping:.2f} ms")
        save_results(download, upload, ping)
        time.sleep(5)
