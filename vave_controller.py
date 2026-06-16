import requests
import json
import os

# Global state for offline mock mode
IS_OFFLINE = False
MOCK_DEVICES = None

def _get_base_url():
    """Get VAVE server base URL dynamically from database config."""
    try:
        import template_manager
        ip = template_manager.get_config("vave_server_ip", "192.168.2.10")
    except Exception:
        ip = "192.168.2.10"
    return f"http://{ip}/cgi-bin", ip

def load_mock_devices():
    global MOCK_DEVICES
    mock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mxsta_response.json')
    if not os.path.exists(mock_file):
        print(f"[!] Mock response file not found at {mock_file}")
        return []
        
    try:
        with open(mock_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            devices = []
            
            # Parse Encoders (Inputs)
            for enc in data.get('in', []):
                devices.append({
                    "id": str(enc.get('id')),
                    "name": enc.get('name', f"Input {enc.get('id')}"),
                    "ip": enc.get('ip', 'Unknown IP'),
                    "role": "encoder"
                })
                
            # Parse Decoders (Outputs)
            for dec in data.get('out', []):
                devices.append({
                    "id": str(dec.get('id')),
                    "name": dec.get('name', f"Output {dec.get('id')}"),
                    "ip": dec.get('ip', 'Unknown IP'),
                    "role": "decoder",
                    "source_id": str(dec.get('txout', ''))
                })
            
            MOCK_DEVICES = devices
            print("[Mock Server] Successfully loaded mock devices from mxsta_response.json")
            return MOCK_DEVICES
    except Exception as e:
        print(f"[!] Error loading mock devices: {e}")
        return []

def get_server_status():
    """Check if VAVE Control Server is reachable. Returns status dict."""
    global IS_OFFLINE
    base_url, server_ip = _get_base_url()
    url = f"{base_url}/getjson.cgi?json=mxsta"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            IS_OFFLINE = False
            return {"online": True, "ip": server_ip, "mode": "live"}
    except Exception:
        pass
    IS_OFFLINE = True
    return {"online": False, "ip": server_ip, "mode": "offline_simulator"}

def fetch_devices_from_server():
    global IS_OFFLINE, MOCK_DEVICES
    
    base_url, server_ip = _get_base_url()
    url = f"{base_url}/getjson.cgi?json=mxsta"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            devices = []
            
            for enc in data.get('in', []):
                devices.append({
                    "id": str(enc.get('id')),
                    "name": enc.get('name', f"Input {enc.get('id')}"),
                    "ip": enc.get('ip', 'Unknown IP'),
                    "role": "encoder"
                })
                
            for dec in data.get('out', []):
                devices.append({
                    "id": str(dec.get('id')),
                    "name": dec.get('name', f"Output {dec.get('id')}"),
                    "ip": dec.get('ip', 'Unknown IP'),
                    "role": "decoder",
                    "source_id": str(dec.get('txout', ''))
                })
                
            IS_OFFLINE = False
            return devices
    except Exception as e:
        if not IS_OFFLINE:
            print(f"[!] VAVE Server offline ({e}). Falling back to Offline Simulator mode.")
            IS_OFFLINE = True
            
    # Fallback to Offline Simulator Mode
    if MOCK_DEVICES is None:
        return load_mock_devices()
    return MOCK_DEVICES

def send_switch_command(encoder_id, decoder_ids):
    global IS_OFFLINE, MOCK_DEVICES
    
    if IS_OFFLINE:
        if MOCK_DEVICES is None:
            load_mock_devices()
            
        print(f"[Mock Server] Routing Encoder {encoder_id} to Decoders {decoder_ids}")
        for dev in MOCK_DEVICES:
            if dev['role'] == 'decoder' and dev['id'] in [str(d) for d in decoder_ids]:
                dev['source_id'] = str(encoder_id)
        return True
        
    base_url, _ = _get_base_url()
    success_count = 0
    for dec_id in decoder_ids:
        cmd_url = f"{base_url}/submit?cmd=SET DEC {dec_id} SWITCH {encoder_id} ALL USER admin"
        try:
            print(f"[*] Sending Command: SET DEC {dec_id} SWITCH {encoder_id}")
            response = requests.get(cmd_url, timeout=3)
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"[!] Command failed for Decoder ID {dec_id} with status {response.status_code}")
        except Exception as e:
            print(f"[!] Network error sending command to Decoder ID {dec_id}: {e}")
            
    return success_count > 0

def send_blackout_command(decoder_ids):
    """Send blackout (disconnect) command to one or more decoders.
    Uses encoder ID '0' which signals no source / blank output."""
    global IS_OFFLINE, MOCK_DEVICES
    
    if IS_OFFLINE:
        if MOCK_DEVICES is None:
            load_mock_devices()
        print(f"[Mock Server] Blackout Decoders {decoder_ids}")
        for dev in MOCK_DEVICES:
            if dev['role'] == 'decoder' and dev['id'] in [str(d) for d in decoder_ids]:
                dev['source_id'] = '0'
        return True

    base_url, _ = _get_base_url()
    success_count = 0
    for dec_id in decoder_ids:
        # VAVE command: switch to encoder 0 = no signal / blackout
        cmd_url = f"{base_url}/submit?cmd=SET DEC {dec_id} SWITCH 0 ALL USER admin"
        try:
            print(f"[*] Sending Blackout Command: SET DEC {dec_id} SWITCH 0")
            response = requests.get(cmd_url, timeout=3)
            if response.status_code == 200:
                success_count += 1
        except Exception as e:
            print(f"[!] Network error sending blackout to Decoder ID {dec_id}: {e}")
            
    return success_count > 0
