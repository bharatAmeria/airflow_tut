import os
import sys
import zipfile
import gdown
from src.logger import logging
from src.exception import MyException
from src.config import CONFIG


def download_file_step() -> str:
    """Downloads dataset from Google Drive and returns the path to the zip file."""
    try:
        config = CONFIG["data"]
        dataset_url = config["source_URL"]
        zip_download_dir = config["local_data_file"]
        os.makedirs("artifacts/data", exist_ok=True)

        logging.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

        # Extract file ID from URL
        parts = dataset_url.split('/')
        if "drive.google.com" in dataset_url and "file" in parts and "d" in parts:
            file_id_index = parts.index("d") + 1
            file_id = parts[file_id_index]
        else:
            raise ValueError(f"Invalid Google Drive URL format: {dataset_url}")

        prefix = 'https://drive.google.com/uc?export=download&id='
        gdown.download(prefix + file_id, zip_download_dir)

        logging.info(f"Successfully downloaded data into {zip_download_dir}")
        return zip_download_dir
    except Exception as e:
        logging.error("Error occurred while downloading file", exc_info=True)
        raise MyException(e, sys)


def extract_zip_step(zip_path: str) -> str:
    """Extracts the zip file and returns the path to the extracted directory."""
    try:
        config = CONFIG["data"]
        unzip_path = config["unzip_dir"]

        os.makedirs(unzip_path, exist_ok=True)
        logging.info(f"Extracting zip file {zip_path} to {unzip_path}")

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

        logging.info(f"Successfully extracted zip file to {unzip_path}")
        return unzip_path
    except Exception as e:
        logging.error("Error occurred while extracting zip file", exc_info=True)
        raise MyException(e, sys)

