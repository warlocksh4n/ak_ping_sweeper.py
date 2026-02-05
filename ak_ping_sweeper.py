import ipaddress
import subprocess
import platform

def ping_ip(ip):
    """
    Returns True if host responds to ping, False otherwise
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", str(ip)]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False


def get_working_ips(cidr):
    network = ipaddress.ip_network(cidr, strict=False)

    print(f"[+] Network      : {network}")
    print(f"[+] Total usable : {network.num_addresses - 2}")
    print("[+] Scanning...\n")

    working_ips = []

    for ip in network.hosts():  # hosts() gives usable IPs only
        if ping_ip(ip):
            print(f"[✔] {ip} is alive")
            working_ips.append(str(ip))

    return working_ips


if __name__ == "__main__":
    cidr_range = input("Enter CIDR (e.g. 192.168.1.0/26): ").strip()
    alive_ips = get_working_ips(cidr_range)

    print("\n==== WORKING IPs ====")
    for ip in alive_ips:
        print(ip)

    print(f"\nTotal alive hosts: {len(alive_ips)}")
