import json
import os

CONFIG_FILE = 'devices.json'

def load_devices():
    """Load devices from JSON configuration."""
    if not os.path.exists(CONFIG_FILE):
        return []
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_devices(devices):
    """Save devices to JSON configuration."""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(devices, f, indent=4, ensure_ascii=False)

def add_or_update_device(ip, name, role):
    """Add a new device or update an existing one by IP."""
    devices = load_devices()
    updated = False
    for device in devices:
        if device['ip'] == ip:
            device['name'] = name
            device['role'] = role
            updated = True
            break
            
    if not updated:
        devices.append({
            "id": ip.replace('.', '_'),
            "ip": ip,
            "name": name,
            "role": role # 'encoder' or 'decoder'
        })
        
    save_devices(devices)
    return devices

def remove_device(ip):
    """Remove a device by IP."""
    devices = load_devices()
    devices = [d for d in devices if d['ip'] != ip]
    save_devices(devices)
    return devices
