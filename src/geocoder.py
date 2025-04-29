import os
import time
import argparse
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Constants
DAILY_LIMIT = 4900
SLEEP_TIME = 1.5
API_URL = "https://geocode.maps.co/search?"

def load_api_key():
    load_dotenv()
    api_key = os.getenv("GEO_API_KEY")
    if not api_key:
        raise EnvironmentError("The environment variable GEO_API_KEY is not set.")
    return api_key

def get_latlong(address, api_key):
    """
    Queries the geocoding API to retrieve coordinates for a given address.
    """
    try:
        response = requests.get(API_URL, params={"q": address, "api_key": api_key})
        response.raise_for_status()
        data = response.json()

        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
        else:
            return np.nan, np.nan

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            print(f"[RATE LIMIT] 429 for: {address}")
        else:
            print(f"[HTTP ERROR] {http_err}")
        return np.nan, np.nan
    except Exception as e:
        print(f"[ERROR] Failed to retrieve '{address}': {e}")
        return np.nan, np.nan

def process_file(path, start_index, api_key):
    """
    Processes the Excel file, geocodes addresses, and updates the coordinates.
    """
    try:
        df = pd.read_excel(path)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    df['LAT'] = pd.to_numeric(df.get('LAT', np.nan), errors='coerce')
    df['LONG'] = pd.to_numeric(df.get('LONG', np.nan), errors='coerce')

    rows_to_process = df[(df['LAT'].isna() | df['LONG'].isna()) & (df.index >= start_index)]

    if rows_to_process.empty:
        print("All rows are already geocoded. Nothing to process.")
        return

    print(f">>> {len(rows_to_process)} rows to geocode starting from index {start_index}.")
    indices = rows_to_process.head(DAILY_LIMIT).index

    processed = 0
    for idx in indices:
        address = df.loc[idx, "ADDRESS_CONCAT"]
        lat, lon = get_latlong(address, api_key)
        df.loc[idx, "LAT"] = lat
        df.loc[idx, "LONG"] = lon

        processed += 1
        if processed % 100 == 0:
            print(f"Progress: {processed} of {len(indices)} rows processed.")

        time.sleep(SLEEP_TIME)

    try:
        df.to_excel(path, index=False)
        print(f"File successfully saved at: {path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Geocode addresses from an Excel file.")
    parser.add_argument("--path", required=True, help="Path to the input Excel file.")
    parser.add_argument("--start_index", type=int, default=0, help="Start index for processing.")

    args = parser.parse_args()
    api_key = load_api_key()
    process_file(args.path, args.start_index, api_key)

if __name__ == "__main__":
    main()
