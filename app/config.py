import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = os.environ.get("ZIVA_UPLOAD_DIR", str(BASE_DIR / "static_uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///" + str(BASE_DIR.parent / "ziva_expenses.db"))
