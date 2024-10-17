import requests
from tqdm import tqdm
import os
import logging


def download_file(url, filename, download_folder):
    """Downloads a file with a progress bar."""
    resp = requests.get(url, stream=True)
    directory = os.path.join(download_folder, filename)
    total = int(resp.headers.get("content-length", 0))

    with open(directory, "wb") as file, tqdm(
        desc=filename,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    logging.info(f"Download of {filename} completed successfully.")
