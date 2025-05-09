import sys
import pandas as pd
from typing import Any
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from train_model import train_model
from src.logger import logging
from src.exception import MyException
from src.components.model import ModelTrainingConfig, ModelTraining
from src.config import CONFIG


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

def train_model(processed_df: pd.DataFrame) -> Any:
    try:
        logging.info(">>>>>Model Training Started...<<<<<")
        processed_df = CONFIG["processed_data_path"]
        model_training_strategy = ModelTraining(data=processed_df, strategy=ModelTrainingConfig())
        trained_model = model_training_strategy.handle_training()
        logging.info(">>>>>Model Training Completed<<<<<\n")
        return trained_model
    except MyException as e:
        logging.exception(e, sys)
        raise e



with DAG(
    dag_id='model_training_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['model-training']
) as dag:

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model
    )
