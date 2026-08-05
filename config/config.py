from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "library.db"
LOG_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backups"
CONFIG_PATH = BASE_DIR / "config" / "settings.json"

DEFAULTS = {
    "app_name": "Library Management System",
    "date_format": "%Y-%m-%d",
    "overdue_days": 14,
    "theme": "System",
    "accent_color": "blue"
}

def load_settings():
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULTS, indent=2), encoding="utf-8")
    data = DEFAULTS.copy()
    try:
        data.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    except Exception:
        pass
    return data

def save_settings(data):
    CONFIG_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")
