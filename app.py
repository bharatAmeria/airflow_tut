import sys
from typing import Any
import pandas as pd
from src.constants import *
from src.logger import logging
from src.exception import MyException
from src.components.dataIngestion import download_file_step, extract_zip_step
from src.components.data_preprocessing import DataPreProcessing, DataPreprocessStrategy
from src.components.model import ModelTrainingConfig, ModelTraining
from src.config import CONFIG

def ingest_data() -> str:
    try:
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} started <<<<<<")
        zip_path = download_file_step()
        extract_zip_step(zip_path)
        logging.info(f">>>>>> stage {INGESTION_STAGE_NAME} completed <<<<<<\n\nx==========x")
        return CONFIG["data_path"]
    except Exception as e:
        logging.exception(f"Error during ingestion: {e}")
        raise MyException(e, sys)

def preprocess_data(data_path: str) -> pd.DataFrame:
    try:
        raw_data = pd.read_csv(data_path)
        strategy = DataPreprocessStrategy()
        processor = DataPreProcessing(data=raw_data, strategy=strategy)
        processed_df = processor.handle_data()
        return processed_df
    except Exception as e:
        raise MyException(e, sys)

def train_model(processed_df: pd.DataFrame) -> Any:
    try:
        logging.info(">>>>>Model Training Started...<<<<<")
        model_training_strategy = ModelTraining(data=processed_df, strategy=ModelTrainingConfig())
        trained_model = model_training_strategy.handle_training()
        logging.info(">>>>>Model Training Completed<<<<<\n")
        return trained_model
    except MyException as e:
        logging.exception(e, sys)
        raise e


def training_pipeline():
    data_path = ingest_data()
    processed_df = preprocess_data(data_path)
    train_model(processed_df)


# ------------------------
# Entry Point
# ------------------------

if __name__ == "__main__":
    try:
        training_pipeline()
    except Exception as e:
        logging.error("Pipeline failed")
        raise e