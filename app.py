from flask import Flask, request, jsonify, send_from_directory, Response
import os
import json
from scanner import scan_network
from device_manager import load_devices, save_devices
from vave_controller import (
    send_switch_command, fetch_devices_from_server,
    get_server_status, send_blackout_command
)
import template_manager

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# ==========================================
# --- Device Endpoints ---
# ==========================================

@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Return live list of devices from VAVE Control Server merged with custom devices."""
    devices = fetch_devices_from_server()
    
    # Fetch manually registered custom devices
    custom_devs = template_manager.get_custom_devices()
    
    # Merge custom devices, marking them with is_custom = True
    existing_ids = {d['id'] for d in devices}
    existing_ips = {d['ip'] for d in devices}
    
    for cd in custom_devs:
        if cd['id'] not in existing_ids and cd['ip'] not in existing_ips:
            cd['is_custom'] = True
            devices.append(cd)
            
    labels = template_manager.get_device_labels()
    # Merge custom labels into device list
    for dev in devices:
        if dev.get('is_custom'):
            dev['is_custom'] = True
        else:
            dev['is_custom'] = False
            
        if dev['id'] in labels:
            dev['display_name'] = labels[dev['id']]
        else:
            dev['display_name'] = dev['name']
            
    return jsonify(devices)

@app.route('/api/devices', methods=['POST'])
def save_device():
    """Add or update a manually registered custom device. Requires Admin PIN."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
        
    data = request.json
    dev_id = data.get('id')
    name = data.get('name')
    ip = data.get('ip')
    role = data.get('role')
    
    if not dev_id or not name or not ip or not role:
        return jsonify({"error": "Missing required fields: id, name, ip, role"}), 400
        
    if role not in ['encoder', 'decoder']:
        return jsonify({"error": "Role must be 'encoder' or 'decoder'"}), 400
        
    template_manager.save_custom_device(dev_id, name, ip, role)
    template_manager.log_activity("DEVICE_ADD", f"Added/Updated custom device: {name} (ID: {dev_id}, IP: {ip}, Role: {role})")
    return jsonify({"status": "success", "message": f"Custom device {name} saved successfully"})

@app.route('/api/devices/<device_id>', methods=['DELETE'])
def delete_device(device_id):
    """Delete a manually registered custom device. Requires Admin PIN."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
        
    success = template_manager.delete_custom_device(device_id)
    if success:
        template_manager.log_activity("DEVICE_DELETE", f"Deleted custom device ID: {device_id}")
        return jsonify({"status": "success", "message": f"Custom device {device_id} deleted successfully"})
    else:
        return jsonify({"error": "Device not found or is managed by VAVE Control Server"}), 404

@app.route('/api/devices/labels', methods=['GET'])
def get_device_labels():
    """Get all custom device display labels."""
    return jsonify(template_manager.get_device_labels())

@app.route('/api/devices/labels', methods=['POST'])
def save_device_labels():
    """Save custom device labels in bulk. Requires Admin PIN."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Expected a JSON object {device_id: label}"}), 400
    template_manager.set_device_labels_bulk(data)
    template_manager.log_activity("LABELS_UPDATED", f"Updated custom labels for {len(data)} device(s)")
    return jsonify({"status": "success", "message": "Device labels saved"})

# ==========================================
# --- Network Scanner ---
# ==========================================

@app.route('/api/scan', methods=['POST'])
def scan():
    """Scan the network for devices."""
    data = request.json
    subnet = data.get('subnet', '192.168.1.0/24')
    found = scan_network(subnet)
    return jsonify(found)

# ==========================================
# --- Routing & Blackout ---
# ==========================================

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
        # Also update custom devices source in database
        for d in decoder_ids:
            template_manager.update_custom_device_source(d, encoder_id)
        # Log activity
        labels = template_manager.get_device_labels()
        enc_name = labels.get(str(encoder_id), f"Encoder {encoder_id}")
        dec_names = [labels.get(str(d), f"Decoder {d}") for d in decoder_ids]
        template_manager.log_activity(
            "ROUTE",
            f"{enc_name} → {', '.join(dec_names)}"
        )
        return jsonify({"status": "success", "message": f"Routed Encoder {encoder_id} to {len(decoder_ids)} decoder(s)"})
    else:
        return jsonify({"status": "error", "message": "Failed to route video"}), 500

@app.route('/api/blackout', methods=['POST'])
def blackout():
    """Send blackout (no signal) to one or more decoders."""
    data = request.json
    decoder_ids = data.get('decoder_ids')
    
    if not decoder_ids or not isinstance(decoder_ids, list):
        return jsonify({"error": "Missing decoder_ids list"}), 400

    success = send_blackout_command(decoder_ids)

    if success:
        for d in decoder_ids:
            template_manager.update_custom_device_source(d, '0')
        labels = template_manager.get_device_labels()
        dec_names = [labels.get(str(d), f"Decoder {d}") for d in decoder_ids]
        template_manager.log_activity(
            "BLACKOUT",
            f"Blackout applied to: {', '.join(dec_names)}"
        )
        return jsonify({"status": "success", "message": f"Blackout applied to {len(decoder_ids)} decoder(s)"})
    else:
        return jsonify({"status": "error", "message": "Failed to send blackout command"}), 500

# ==========================================
# --- Templates ---
# ==========================================

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
    template_manager.log_activity("TEMPLATE_CREATE", f"Created template: \"{name}\"")
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
        template_manager.log_activity("TEMPLATE_EDIT", f"Edited template: \"{name}\"")
        return jsonify({"status": "success", "message": "Template updated successfully"})
    return jsonify({"error": "Template not found"}), 404

@app.route('/api/templates/<int:template_id>', methods=['DELETE'])
def delete_template(template_id):
    """Delete a template. Requires admin PIN in headers."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    
    tpl = template_manager.get_template(template_id)
    tpl_name = tpl['name'] if tpl else f"ID {template_id}"
    success = template_manager.delete_template(template_id)
    if success:
        template_manager.log_activity("TEMPLATE_DELETE", f"Deleted template: \"{tpl_name}\"")
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
        template_manager.log_activity(
            "TEMPLATE_APPLY",
            f"Applied template: \"{template['name']}\""
        )
        return jsonify({"status": "success", "message": f"Template '{template['name']}' applied successfully"})
    else:
        return jsonify({"status": "partial_success", "message": "Template applied with errors", "errors": errors}), 500

# ==========================================
# --- Template Export / Import ---
# ==========================================

@app.route('/api/templates/export', methods=['GET'])
def export_templates():
    """Export all templates as downloadable JSON file."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    
    export_data = template_manager.export_templates()
    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
    template_manager.log_activity("EXPORT", f"Exported {len(export_data['templates'])} template(s)")
    return Response(
        json_str,
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=metrix_templates.json'}
    )

@app.route('/api/templates/import', methods=['POST'])
def import_templates():
    """Import templates from JSON file upload. Requires admin PIN."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    
    overwrite = request.args.get('overwrite', 'false').lower() == 'true'
    
    if 'file' in request.files:
        file = request.files['file']
        try:
            import_data = json.load(file)
        except Exception:
            return jsonify({"error": "Invalid JSON file"}), 400
    elif request.is_json:
        import_data = request.json
    else:
        return jsonify({"error": "No file or JSON body provided"}), 400

    imported, skipped = template_manager.import_templates(import_data, overwrite=overwrite)
    template_manager.log_activity("IMPORT", f"Imported {imported} template(s), skipped {skipped}")
    return jsonify({
        "status": "success",
        "imported": imported,
        "skipped": skipped,
        "message": f"Imported {imported} template(s), skipped {skipped}"
    })

# ==========================================
# --- Admin ---
# ==========================================

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
        template_manager.log_activity("SECURITY", "Admin PIN changed")
        return jsonify({"status": "success", "message": "PIN updated successfully"})
    return jsonify({"error": "Invalid old PIN"}), 401

# ==========================================
# --- System Config ---
# ==========================================

@app.route('/api/config', methods=['GET'])
def get_system_config():
    """Get all public system configurations."""
    return jsonify({
        "system_language": template_manager.get_config("system_language", "th"),
        "vave_server_ip": template_manager.get_config("vave_server_ip", "192.168.2.10")
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
    
    changes = []
    if 'system_language' in data:
        lang = data.get('system_language')
        if lang in ['th', 'en']:
            template_manager.set_config('system_language', lang)
            changes.append(f"language={lang}")
        else:
            return jsonify({"error": "Unsupported language value"}), 400

    if 'vave_server_ip' in data:
        ip = data.get('vave_server_ip', '').strip()
        if ip:
            template_manager.set_config('vave_server_ip', ip)
            changes.append(f"vave_server_ip={ip}")
        else:
            return jsonify({"error": "Invalid IP address"}), 400

    if changes:
        template_manager.log_activity("CONFIG_UPDATE", f"System config updated: {', '.join(changes)}")
    return jsonify({"status": "success", "message": "System configuration updated successfully"})

# ==========================================
# --- Server Status ---
# ==========================================

@app.route('/api/server-status', methods=['GET'])
def server_status():
    """Check VAVE Control Server connectivity."""
    status = get_server_status()
    return jsonify(status)

# ==========================================
# --- Activity Log ---
# ==========================================

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get activity log. Requires admin PIN in headers."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    limit = int(request.args.get('limit', 100))
    logs = template_manager.get_activity_log(limit=limit)
    return jsonify(logs)

@app.route('/api/logs', methods=['DELETE'])
def clear_logs():
    """Clear all activity logs. Requires admin PIN."""
    pin = request.headers.get('X-Admin-PIN')
    if not template_manager.verify_admin_pin(pin):
        return jsonify({"error": "Unauthorized: Invalid PIN"}), 401
    template_manager.clear_activity_log()
    return jsonify({"status": "success", "message": "Activity log cleared"})

# ==========================================
# --- App Entry Point ---
# ==========================================

if __name__ == '__main__':
    template_manager.init_db()
    
    if not os.path.exists('devices.json'):
        save_devices([])
        
    print("Starting VAVE AVIP Matrix Controller on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
