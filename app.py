from flask import Flask, request, jsonify, send_from_directory
import os
from scanner import scan_network
from device_manager import load_devices, save_devices, add_or_update_device, remove_device
from vave_controller import send_switch_command, fetch_devices_from_server
import template_manager

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

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get all templates."""
    return jsonify(template_manager.get_all_templates())

@app.route('/api/templates', methods=['POST'])
def create_template():
    """Create a new template. Requires admin PIN in headers."""
    data = request.json
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    
    name = data.get('name')
    description = data.get('description', '')
    color = data.get('color', '#3b82f6')
    icon = data.get('icon', '🖥️')
    routing_map = data.get('routing_map')
    
    if not name or not routing_map:
        return jsonify({"error": "Missing name or routing_map"}), 400
        
    template_id = template_manager.create_template(name, description, color, icon, routing_map)
    return jsonify({"status": "success", "id": template_id, "message": "Template created successfully"})

@app.route('/api/templates/<int:template_id>', methods=['PUT'])
def update_template(template_id):
    """Update an existing template. Requires admin PIN in headers."""
    data = request.json
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
        
    name = data.get('name')
    description = data.get('description', '')
    color = data.get('color', '#3b82f6')
    icon = data.get('icon', '🖥️')
    routing_map = data.get('routing_map')
    
    if not name or not routing_map:
        return jsonify({"error": "Missing name or routing_map"}), 400
        
    success = template_manager.update_template(template_id, name, description, color, icon, routing_map)
    if success:
        return jsonify({"status": "success", "message": "Template updated successfully"})
    return jsonify({"error": "Template not found"}), 404

@app.route('/api/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete a template. Requires admin PIN in headers."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
        
    success = template_manager.delete_template(template_id)
    if success:
        return jsonify({"status": "success", "message": "Template deleted successfully"})
    return jsonify({"error": "Template not found"}), 404

@app.route('/api/templates/<int:template_id>/apply', methods=['POST'])
def apply_template(template_id):
    """Apply a template by sending routing commands."""
    template = template_manager.get_template(template_id)
    if not template:
        return jsonify({"error": "Template not found"}), 404
        
    routing_map = template.get('routing_map', [])
    success = True
    errors = []
    
    for item in routing_map:
        enc_id = item.get('encoder_id')
        dec_ids = item.get('decoder_ids')
        if enc_id and dec_ids:
            res = send_switch_command(enc_id, dec_ids)
            if not res:
                success = False
                errors.append(f"Failed routing Encoder {enc_id} to decoders {dec_ids}")
                
    if success:
        return jsonify({"status": "success", "message": f"Template '{template['name']}' applied successfully"})
    else:
        return jsonify({"status": "partial_success", "message": "Template applied with errors", "errors": errors}), 500

@app.route('/api/admin/verify', methods=['POST'])
def verify_admin():
    """Verify admin PIN."""
    data = request.json
    pin = data.get('pin')
    if template_manager.verify_admin_pin(pin):
        return jsonify({"status": "success", "message": "PIN verified successfully"})
    return jsonify({"error": "Invalid PIN"}), 401

@app.route('/api/admin/change-pin', methods=['POST'])
def change_pin():
    """Change admin PIN. Requires old PIN for verification."""
    data = request.json
    old_pin = data.get('old_pin')
    new_pin = data.get('new_pin')
    
    if not old_pin or not new_pin:
        return jsonify({"error": "Missing old_pin or new_pin"}), 400
        
    if template_manager.update_admin_pin(old_pin, new_pin):
        return jsonify({"status": "success", "message": "PIN updated successfully"})
    return jsonify({"error": "Invalid old PIN"}), 401

@app.route('/api/config', methods=['GET'])
def get_system_config():
    """Get all public system configurations."""
    return jsonify({
        "system_language": template_manager.get_config("system_language", "th")
    })

@app.route('/api/config', methods=['POST'])
def save_system_config():
    """Save system configurations. Requires admin PIN in headers."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
        
    data = request.json
    if not data:
        return jsonify({"error": "Missing config data"}), 400
        
    if 'system_language' in data:
        lang = data.get('system_language')
        if lang in ['th', 'en']:
            template_manager.set_config('system_language', lang)
        else:
            return jsonify({"error": "Unsupported language value"}), 400
            
    return jsonify({"status": "success", "message": "System configuration updated successfully"})

if __name__ == '__main__':
    # Initialize SQLite database
    template_manager.init_db()
    
    # Initialize an empty config if not exists
    if not os.path.exists('devices.json'):
        save_devices([])
        
    print("Starting VAVE AVIP Matrix Controller on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
