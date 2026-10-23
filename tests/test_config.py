"""
tests/test_config.py
--------------------
Unit tests for configuration loading, saving, and schema defaults (config/config.py).
Ensures settings persistence meets Q11 maintainability criteria.
"""

import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from config.config import DEFAULTS, load_settings, save_settings


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_cfg_path = Path(self.temp_dir.name) / "test_settings.json"

        self.patcher = patch("config.config.CONFIG_PATH", self.test_cfg_path)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.temp_dir.cleanup()

    def test_default_settings_creation(self):
        # File doesn't exist yet
        self.assertFalse(self.test_cfg_path.exists())

        settings = load_settings()
        self.assertTrue(self.test_cfg_path.exists())
        self.assertEqual(settings["app_name"], DEFAULTS["app_name"])
        self.assertEqual(settings["overdue_days"], DEFAULTS["overdue_days"])

    def test_save_and_reload_settings(self):
        new_data = {
            "app_name": "Updated TQM Library",
            "overdue_days": 21,
            "fine_per_day": 10,
            "max_books_per_member": 5,
            "date_format": "%d-%m-%Y",
            "theme": "Dark Slate"
        }
        save_settings(new_data)

        loaded = load_settings()
        self.assertEqual(loaded["app_name"], "Updated TQM Library")
        self.assertEqual(loaded["overdue_days"], 21)
        self.assertEqual(loaded["fine_per_day"], 10)
        self.assertEqual(loaded["max_books_per_member"], 5)


if __name__ == "__main__":
    unittest.main()
