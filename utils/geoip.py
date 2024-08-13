import os
import requests
import tarfile
import shutil
import threading
import time
from datetime import datetime, timedelta

GEOIP_DB_PATH = 'data/GeoLite2-City.mmdb'
DOWNLOAD_URL = "https://download.maxmind.com/app/geoip_download"
TMP_DIR = 'tmp'
UPDATE_INTERVAL = timedelta(days=7)
CONFIG_PATH = 'config/GeoIP.conf'

def get_license_key():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r') as f:
        return next((line.split()[1] for line in f if line.startswith('LicenseKey')), None)

def download_geoip_database():
    license_key = get_license_key()
    if not license_key:
        raise ValueError("License key not found in config file")

    response = requests.get(DOWNLOAD_URL, params={
        'edition_id': 'GeoLite2-City',
        'license_key': license_key,
        'suffix': 'tar.gz'
    }, stream=True)
    
    if response.status_code == 200:
        with open('GeoLite2-City.tar.gz', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        os.makedirs(TMP_DIR, exist_ok=True)
        with tarfile.open('GeoLite2-City.tar.gz', 'r:gz') as tar:
            tar.extractall(path=TMP_DIR)
        
        os.remove('GeoLite2-City.tar.gz')
        
        for root, dirs, files in os.walk(TMP_DIR):
            for file in files:
                if file.endswith('.mmdb'):
                    os.makedirs(os.path.dirname(GEOIP_DB_PATH), exist_ok=True)
                    shutil.move(os.path.join(root, file), GEOIP_DB_PATH)
                    print("Database moved successfully to 'data' directory.")
                    break
        
        shutil.rmtree(TMP_DIR)
        print("Temporary directory removed.")
    else:
        print(f"Failed to download GeoIP database. Status code: {response.status_code}")

def update_geoip_database_if_needed():
    if not os.path.exists(GEOIP_DB_PATH) or \
       datetime.now() - datetime.fromtimestamp(os.path.getmtime(GEOIP_DB_PATH)) > UPDATE_INTERVAL:
        download_geoip_database()

def periodic_update():
    while True:
        update_geoip_database_if_needed()
        time.sleep(UPDATE_INTERVAL.total_seconds())

def start_periodic_update():
    thread = threading.Thread(target=periodic_update, daemon=True)
    thread.start()

def get_geoip_db_path():
    return GEOIP_DB_PATH
