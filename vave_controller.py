import time
import requests
import json
import os

CONTROL_SERVER_IP = "192.168.2.10"
BASE_URL = f"http://{CONTROL_SERVER_IP}/cgi-bin"

# Global state for offline mock mode
IS_OFFLINE = False
MOCK_DEVICES = None

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

def fetch_devices_from_server():
    global IS_OFFLINE, MOCK_DEVICES
    
    # Try fetching from live VAVE Control Server
    url = f"{BASE_URL}/getjson.cgi?json=mxsta"
    try:
        response = requests.get(url, timeout=2) # Short timeout for quick offline detection
        if response.status_code == 200:
            data = response.json()
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
        # Simulate local switch in mock state
        if MOCK_DEVICES is None:
            load_mock_devices()
            
        print(f"[Mock Server] Routing Encoder {encoder_id} to Decoders {decoder_ids}")
        for dev in MOCK_DEVICES:
            if dev['role'] == 'decoder' and dev['id'] in [str(d) for d in decoder_ids]:
                dev['source_id'] = str(encoder_id)
        return True
        
    # Real live routing command
    success_count = 0
    for dec_id in decoder_ids:
        cmd_url = f"{BASE_URL}/submit?cmd=SET DEC {dec_id} SWITCH {encoder_id} ALL USER admin"
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
