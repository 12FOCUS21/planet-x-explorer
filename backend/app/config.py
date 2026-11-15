"""Rutas comunes y límites de red seguros."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / 'frontend'
CACHE = ROOT / 'data' / 'cache'
CACHE.mkdir(parents=True, exist_ok=True)
REQUEST_TIMEOUT = max(3, min(120, int(os.getenv('PX_REQUEST_TIMEOUT', '60'))))
MAX_DOWNLOAD = max(5, min(150, int(os.getenv('PX_MAX_DOWNLOAD_MB', '35')))) * 1024 * 1024
