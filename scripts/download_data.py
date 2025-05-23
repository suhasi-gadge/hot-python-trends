#!/usr/bin/env python3
import os
import subprocess
import sys
import zipfile

# 1. Define where raw data should live
DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, 'data')
)
os.makedirs(DATA_DIR, exist_ok=True)

# 2. Kaggle dataset identifier 
KAGGLE_DATASET = 'berkayalan/stack-overflow-annual-developer-survey-2024'

def download_survey():
    # a) Download (force overwrite)
    result = subprocess.run(
        ['kaggle', 'datasets', 'download',
         '-d', KAGGLE_DATASET,
         '-p', DATA_DIR,
         '--force'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print('ERROR downloading data:', result.stderr, file=sys.stderr)
        sys.exit(1)

    # b) Extract the zip using Python
    zip_name = f"{KAGGLE_DATASET.split('/')[-1]}.zip"
    zip_path = os.path.join(DATA_DIR, zip_name)
    if not os.path.exists(zip_path):
        print(f"ERROR: Expected zip at {zip_path} not found.", file=sys.stderr)
        sys.exit(1)

    print('Download complete. Extracting', zip_path)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(DATA_DIR)
    print('Extraction complete.')

    # c) (Optional) remove the zip to save space
    try:
        os.remove(zip_path)
        print('Removed zip file to save space.')
    except OSError:
        pass

    print('Data ready in', DATA_DIR)

if __name__ == '__main__':
    download_survey()
