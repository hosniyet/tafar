import time
import threading
from scapy.all import ARP, sniff
import arpspoof
import scanner

# Whitelist of trusted MAC addresses (manually or dynamically added)
WHITELIST_MACS = ["00:11:22:33:44:55", "66:77:88:99:AA:BB"]

def monitor_network():
    """
    Continuously monitors the network for new devices
    and performs ARP spoofing on untrusted devices.
    """
    print("[NetLock] Monitoring network for new devices...")
    while True:
        devices = scanner.scan_network()
        for dev in devices:
            mac = dev['mac']
            if mac not in WHITELIST_MACS:
                print(f"[NetLock] Unknown MAC detected: {mac}. Spoofing...")
                # Assuming the gateway is always 192.168.1.1 for spoofing
                arpspoof.spoof(target_ip=dev['ip'], spoof_ip="192.168.1.1")
        time.sleep(10)  # Sleep for 10 seconds before checking again

def start_netlock():
    """
    Starts a background thread to monitor the network and apply NetLock.
    """
    netlock_thread = threading.Thread(target=monitor_network, daemon=True)
    netlock_thread.start()
    print("[NetLock] NetLock feature started in the background.")

