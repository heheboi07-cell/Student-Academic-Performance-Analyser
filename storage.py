"""
storage.py - Data Storage: Handles JSON persistence, auto-seeding, backup & restore.
"""
import json
import shutil
from datetime import datetime
from pathlib import Path

class StorageManager:
    def __init__(self, filepath: str = "data/students.json"):
        self.filepath = Path(filepath)
        self.backup_dir = Path("backups")
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_seed_data()

    def _ensure_seed_data(self):
        """Auto-seed default student data so fresh clones and automated tests run immediately."""
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            seed = {
                "26BCE12345": {
                    "roll_no": "26BCE12345",
                    "name": "Mohit Dongare",
                    "semester": 1,
                    "section": "C",
                    "attendance": 87.0,
                    "marks": {
                        "Mathematics": 82.0,
                        "Python": 91.0,
                        "Physics": 74.0,
                        "Electronics": 78.0,
                        "English": 86.0
                    }
                }
            }
            self.save_all(seed)

    def load_all(self) -> dict:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_all(self, data: dict):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def backup_data(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = self.backup_dir / f"students_backup_{timestamp}.json"
        shutil.copy(self.filepath, backup_file)
        return str(backup_file)

    def restore_data(self, backup_path: str) -> bool:
        src = Path(backup_path)
        if src.exists():
            shutil.copy(src, self.filepath)
            return True
        return False