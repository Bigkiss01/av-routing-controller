from flask import Flask, request, jsonify, send_from_directory
import os
from scanner import scan_network
from device_manager import load_devices, save_devices, add_or_update_device, remove_device
from vave_controller import send_switch_command, fetch_devices_from_server

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Return live list of devices from VAVE Control Server."""
    devices = fetch_devices_from_server()
    return jsonify(devices)

@app.route('/api/devices', methods=['POST'])
def save_device():
    return jsonify({"error": "Devices are managed by VAVE Control Server"}), 403

@app.route('/api/devices/<ip>', methods=['DELETE'])
def delete_device(ip):
    return jsonify({"error": "Devices are managed by VAVE Control Server"}), 403

@app.route('/api/scan', methods=['POST'])
def scan():
    """Scan the network for devices."""
    data = request.json
    subnet = data.get('subnet', '192.168.1.0/24')
    found = scan_network(subnet)
    return jsonify(found)

@app.route('/api/route', methods=['POST'])
def route_video():
    """Route an encoder stream to one or more decoders."""
    data = request.json
    encoder_id = data.get('encoder_id')
    decoder_ids = data.get('decoder_ids')
    
    if not encoder_id or not decoder_ids or not isinstance(decoder_ids, list):
        return jsonify({"error": "Missing encoder_id or decoder_ids list"}), 400
        
    success = send_switch_command(encoder_id, decoder_ids)
    
    if success:
        return jsonify({"status": "success", "message": f"Routed Encoder {encoder_id} to {len(decoder_ids)} decoder(s)"})
    else:
        return jsonify({"status": "error", "message": "Failed to route video"}), 500

if __name__ == '__main__':
    # Initialize an empty config if not exists
    if not os.path.exists('devices.json'):
        save_devices([])
        
    print("Starting VAVE AVIP Matrix Controller on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
