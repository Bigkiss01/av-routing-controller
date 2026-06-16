import socket
import concurrent.futures
import ipaddress

def check_device(ip, timeout=1.0):
    """
    Check if common AV over IP control ports are open on a given IP.
    """
    ports_to_check = [80, 23, 5000, 8000, 8080]
    open_ports = []
    
    for port in ports_to_check:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((str(ip), port))
                if result == 0:
                    open_ports.append(port)
        except Exception:
            pass
            
    if open_ports:
        return {"ip": str(ip), "ports": open_ports}
    return None

def scan_network(subnet):
    """
    Scan a given subnet for active devices with open AV ports.
    """
    try:
        network = ipaddress.IPv4Network(subnet, strict=False)
    except ValueError:
        return []

    found_devices = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_device, network.hosts())
        
        for result in results:
            if result:
                found_devices.append(result)
                
    return found_devices

if __name__ == "__main__":
    # Test execution
    print(scan_network("192.168.1.0/24"))
