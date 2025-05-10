from scapy.all import ARP, Ether, srp
import socket
import requests

def get_mac_vendor(mac):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}")
        return response.text
    except:
        return "Unknown"

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

def scan_network(target_ip="192.168.1.1/24"):
    """
    Scans the local network and returns a list of connected devices.
    """
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []
    for sent, received in result:
        ip = received.psrc
        mac = received.hwsrc
        vendor = get_mac_vendor(mac)
        hostname = get_hostname(ip)

        devices.append({
            "ip": ip,
            "mac": mac,
            "vendor": vendor,
            "hostname": hostname
        })

    return devices

if __name__ == "__main__":
    devices = scan_network()
    for d in devices:
        print(f"{d['ip']:15} {d['mac']:17} {d['vendor']:30} {d['hostname']}")