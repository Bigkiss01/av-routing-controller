import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and set default values if needed."""
    with get_db_connection() as conn:
        # Templates table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                color TEXT DEFAULT '#3b82f6',
                icon TEXT DEFAULT '🖥️',
                routing_map TEXT NOT NULL,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Config table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # Activity Log table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action_type TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Device Labels table (custom display names)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS device_labels (
                device_id TEXT PRIMARY KEY,
                label TEXT NOT NULL
            )
        ''')
        
        # Custom Devices table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS custom_devices (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                ip TEXT NOT NULL,
                role TEXT NOT NULL,
                source_id TEXT DEFAULT '0'
            )
        ''')
        
        # Insert default admin PIN if not set
        cursor = conn.execute("SELECT value FROM config WHERE key = 'admin_pin'")
        if not cursor.fetchone():
            conn.execute("INSERT INTO config (key, value) VALUES ('admin_pin', '1234')")
            
        # Insert default system language if not set
        cursor = conn.execute("SELECT value FROM config WHERE key = 'system_language'")
        if not cursor.fetchone():
            conn.execute("INSERT INTO config (key, value) VALUES ('system_language', 'th')")
        
        # Insert default VAVE server IP if not set
        cursor = conn.execute("SELECT value FROM config WHERE key = 'vave_server_ip'")
        if not cursor.fetchone():
            conn.execute("INSERT INTO config (key, value) VALUES ('vave_server_ip', '192.168.2.10')")
            
        conn.commit()

def get_all_templates():
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM templates ORDER BY sort_order ASC, id ASC")
        rows = cursor.fetchall()
        
        templates = []
        for r in rows:
            template = dict(r)
            # Try to parse the JSON string back into a Python structure
            try:
                template['routing_map'] = json.loads(template['routing_map'])
            except Exception:
                template['routing_map'] = []
            templates.append(template)
            
        return templates

def get_template(template_id):
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
        row = cursor.fetchone()
        if row:
            template = dict(row)
            try:
                template['routing_map'] = json.loads(template['routing_map'])
            except Exception:
                template['routing_map'] = []
            return template
        return None

def create_template(name, description, color, icon, routing_map):
    with get_db_connection() as conn:
        routing_map_str = json.dumps(routing_map)
        cursor = conn.execute(
            """INSERT INTO templates (name, description, color, icon, routing_map) 
               VALUES (?, ?, ?, ?, ?)""",
            (name, description, color, icon, routing_map_str)
        )
        conn.commit()
        return cursor.lastrowid

def update_template(template_id, name, description, color, icon, routing_map):
    with get_db_connection() as conn:
        routing_map_str = json.dumps(routing_map)
        cursor = conn.execute(
            """UPDATE templates 
               SET name = ?, description = ?, color = ?, icon = ?, routing_map = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (name, description, color, icon, routing_map_str, template_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_template(template_id):
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM templates WHERE id = ?", (template_id,))
        conn.commit()
        return cursor.rowcount > 0

def verify_admin_pin(pin):
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT value FROM config WHERE key = 'admin_pin'")
        row = cursor.fetchone()
        if row:
            return row['value'] == str(pin)
        return False

def update_admin_pin(old_pin, new_pin):
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT value FROM config WHERE key = 'admin_pin'")
        row = cursor.fetchone()
        if not row or row['value'] != str(old_pin):
            return False
            
        conn.execute("UPDATE config SET value = ? WHERE key = 'admin_pin'", (str(new_pin),))
        conn.commit()
        return True

def get_config(key, default_value=None):
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT value FROM config WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            return row['value']
        return default_value

def set_config(key, value):
    with get_db_connection() as conn:
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", (key, str(value)))
        conn.commit()
        return True

# ==========================================
# --- Activity Log ---
# ==========================================

def log_activity(action_type, description):
    """Record an action in the activity log."""
    with get_db_connection() as conn:
        conn.execute(
            "INSERT INTO activity_log (action_type, description) VALUES (?, ?)",
            (action_type, description)
        )
        conn.commit()

def get_activity_log(limit=100):
    """Retrieve recent activity log entries."""
    with get_db_connection() as conn:
        cursor = conn.execute(
            "SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]

def clear_activity_log():
    """Clear all activity log entries."""
    with get_db_connection() as conn:
        conn.execute("DELETE FROM activity_log")
        conn.commit()

# ==========================================
# --- Device Labels (Custom Names) ---
# ==========================================

def get_device_labels():
    """Get all custom device labels as a dict {device_id: label}."""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT device_id, label FROM device_labels")
        return {row['device_id']: row['label'] for row in cursor.fetchall()}

def set_device_label(device_id, label):
    """Set or update a custom label for a device."""
    with get_db_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO device_labels (device_id, label) VALUES (?, ?)",
            (str(device_id), str(label))
        )
        conn.commit()
        return True

def delete_device_label(device_id):
    """Remove a custom label for a device (revert to VAVE server name)."""
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM device_labels WHERE device_id = ?", (str(device_id),))
        conn.commit()
        return cursor.rowcount > 0

def set_device_labels_bulk(labels_dict):
    """Set multiple labels at once. labels_dict = {device_id: label}"""
    with get_db_connection() as conn:
        for device_id, label in labels_dict.items():
            if label and label.strip():
                conn.execute(
                    "INSERT OR REPLACE INTO device_labels (device_id, label) VALUES (?, ?)",
                    (str(device_id), str(label).strip())
                )
            else:
                # Empty label = delete custom label
                conn.execute("DELETE FROM device_labels WHERE device_id = ?", (str(device_id),))
        conn.commit()
        return True

# ==========================================
# --- Template Export / Import ---
# ==========================================

def export_templates():
    """Export all templates as a list of dicts (ready for JSON serialization)."""
    templates = get_all_templates()
    return {
        "export_version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "templates": templates
    }

def import_templates(import_data, overwrite=False):
    """Import templates from exported JSON data. Returns (imported_count, skipped_count)."""
    templates = import_data.get("templates", [])
    imported = 0
    skipped = 0

    for tpl in templates:
        name = tpl.get("name")
        description = tpl.get("description", "")
        color = tpl.get("color", "#3b82f6")
        icon = tpl.get("icon", "🖥️")
        routing_map = tpl.get("routing_map", [])

        if not name or not routing_map:
            skipped += 1
            continue

        if overwrite:
            # Check if a template with the same name exists and update it
            with get_db_connection() as conn:
                cursor = conn.execute("SELECT id FROM templates WHERE name = ?", (name,))
                existing = cursor.fetchone()
                if existing:
                    update_template(existing['id'], name, description, color, icon, routing_map)
                    imported += 1
                    continue

        create_template(name, description, color, icon, routing_map)
        imported += 1

    return imported, skipped

# ==========================================
# --- Custom Devices (Manually Added) ---
# ==========================================

def get_custom_devices():
    """Retrieve all manually registered custom devices."""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM custom_devices")
        return [dict(row) for row in cursor.fetchall()]

def save_custom_device(device_id, name, ip, role):
    """Save or update a custom device registration."""
    with get_db_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO custom_devices (id, name, ip, role) VALUES (?, ?, ?, ?)",
            (str(device_id), str(name), str(ip), str(role))
        )
        conn.commit()
        return True

def delete_custom_device(device_id):
    """Delete a custom device registration."""
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM custom_devices WHERE id = ?", (str(device_id),))
        conn.commit()
        return cursor.rowcount > 0

def update_custom_device_source(device_id, source_id):
    """Update active routing source for a custom device."""
    with get_db_connection() as conn:
        conn.execute("UPDATE custom_devices SET source_id = ? WHERE id = ?", (str(source_id), str(device_id)))
        conn.commit()
        return True
