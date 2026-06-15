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
