import time
import requests

CONTROL_SERVER_IP = "192.168.2.10"
BASE_URL = f"http://{CONTROL_SERVER_IP}/cgi-bin"

def fetch_devices_from_server():
    """
    Fetches the live list of devices from the VAVE Control Server.
    Maps them into the application's required JSON format.
    """
    url = f"{BASE_URL}/getjson.cgi?json=mxsta"
    try:
        response = requests.get(url, timeout=5)
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
                    "role": "decoder"
                })
                
            return devices
    except Exception as e:
        print(f"[!] Error fetching devices from VAVE Server: {e}")
        
    return []

def send_switch_command(encoder_id, decoder_ids):
    """
    Sends the routing command to the VAVE AVIP-H265-1G-T Control Server.
    API Format: GET /cgi-bin/submit?cmd=SET DEC {dec_id} SWITCH {enc_id} ALL USER admin
    """
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
            
    time.sleep(0.1)
    return success_count > 0
