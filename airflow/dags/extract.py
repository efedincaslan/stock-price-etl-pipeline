from dotenv import load_dotenv
import os
import requests
import json
import logging
import time
from config import SYMBOLS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

import datetime

def is_cache_fresh(cache_file):
    with open(cache_file) as f:
        data = json.load(f)
    cached_date = data.get('cached_date')
    if cached_date is None:
        return False
    return cached_date == str(datetime.date.today())


def extraction(symbol):
    CACHE_FILE = f"{symbol}_data_cache.json"
    if os.path.exists(CACHE_FILE) and is_cache_fresh(CACHE_FILE):
        logging.info("Loading from cache...")
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
 
    API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
    API_URL = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }

    try:
        time.sleep(12)
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if 'Time Series (Daily)' not in data:
            logging.error(f"Invalid response for {symbol}: {data}")
            return None
        
        
        with open(CACHE_FILE, "w") as f:
            data['cached_date'] = str(datetime.date.today())
            json.dump(data, f, indent=2)

        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    for symbol in SYMBOLS:
        print(extraction(symbol))

