from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
EXPORT_DIR = BASE_DIR / "exports"

DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

PLATFORMS = {
    "skool": {
        "base_url": "https://www.skool.com",
        "api_endpoint": "https://api.skool.com",
    },
    "whop": {
        "base_url": "https://whop.com",
        "api_endpoint": "https://api.whop.com",
    }
}

TIME_RANGES = {
    "1week": timedelta(days=7),
    "30days": timedelta(days=30),
    "3months": timedelta(days=90),
    "1year": timedelta(days=365),
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
