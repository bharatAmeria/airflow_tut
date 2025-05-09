from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import logging

from src.components.data_preprocessing import DataPreprocessStrategy, DataPreProcessing
from src.config import CONFIG 

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

def preprocess_task():
    try:
        # Load raw dataset
        raw_data_path = CONFIG["raw_data_path"]
        df = pd.read_csv(raw_data_path)

        # Apply preprocessing strategy
        strategy = DataPreprocessStrategy()
        processor = DataPreProcessing(data=df, strategy=strategy)
        processed_df = processor.handle_data()

        logging.info("Data preprocessing completed.")
        return True, processed_df

    except Exception as e:
        logging.error("Failed in preprocessing task", exc_info=True)
        raise

with DAG(
    dag_id='data_preprocessing_pipeline',
    default_args=default_args,
    description='Preprocess data using strategy pattern',
    schedule_interval=None,
    catchup=False,
    tags=['preprocessing'],
) as dag:

    run_preprocessing = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_task
    )

    run_preprocessing
