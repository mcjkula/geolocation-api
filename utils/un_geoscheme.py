import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

UN_GEOSCHEME_PATH = 'data/un_geoscheme.json'
UN_GEOSCHEME_URL = "https://unstats.un.org/unsd/methodology/m49/overview/"
UPDATE_INTERVAL = timedelta(days=7)

def scrape_un_geoscheme():
    response = requests.get(UN_GEOSCHEME_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find('table', {'id': 'downloadTableEN'}).find('tbody').find_all('tr')
    
    geoscheme = {}
    for row in rows:
        cols = row.find_all('td')
        region, subregion, iso_alpha2 = cols[3].text.strip(), cols[5].text.strip(), cols[10].text.strip()
        geoscheme.setdefault(region, {}).setdefault(subregion, []).append(iso_alpha2)
    
    with open(UN_GEOSCHEME_PATH, 'w', encoding='utf-8') as f:
        json.dump(geoscheme, f)
    
    print("UN Geoscheme updated successfully.")
    return geoscheme

def get_un_geoscheme():
    if not os.path.exists(UN_GEOSCHEME_PATH) or \
       datetime.now() - datetime.fromtimestamp(os.path.getmtime(UN_GEOSCHEME_PATH)) > UPDATE_INTERVAL:
        return scrape_un_geoscheme()
    
    with open(UN_GEOSCHEME_PATH, 'r') as f:
        return json.load(f)

def get_subregion(country_code, un_geoscheme):
    for region in un_geoscheme.values():
        for subregion, countries in region.items():
            if country_code in countries:
                return subregion
    return None
