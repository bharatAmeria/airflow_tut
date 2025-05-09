import sys
import json
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from src.logger import logging
from src.exception import MyException
from src.utils import log_to_file  #log_to_db, log_to_file
from src.components.dataIngestion import download_file_step, extract_zip_step

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(dag_id='gdrive_data_pipeline',
    default_args=default_args,
    description='Download and extract data from Google Drive',
    schedule_interval=None,  # Can be '0 6 * * *' for daily at 6am
    catchup=False,
    tags=['example'],
) as dag:

    def download_task(**kwargs):
        try:
            zip_path = download_file_step()
            log_to_file("Download", "Success")
            # log_to_db("Download", "Success", {"path": zip_path})
            # log_to_file("Download", "Success", {"path": zip_path})
            # kwargs['ti'].xcom_push(key='zip_path', value=zip_path)
            kwargs['ti'].xcom_push(key='zip_path', value=zip_path)
        except Exception as e:
            log_to_file("Download", f"Failed: {str(e)}")
            raise MyException(e, sys)


    def extract_task(**kwargs):
        try:
            zip_path = kwargs['ti'].xcom_pull(key='zip_path')
            log_to_file("Download", "Success")
            extract_zip_step(zip_path)
            # extracted_path = extract_zip_step(zip_path)
            # log_to_db("Extract", "Success", {"output_path": extracted_path})
            # log_to_file("Extract", "Success", {"output_path": extracted_path})
        except Exception as e:
            log_to_file("Download", f"Failed: {str(e)}")
            raise MyException(e, sys)

    t1 = PythonOperator(
        task_id='download_from_gdrive',
        python_callable=download_task,
        provide_context=True,
    )

    t2 = PythonOperator(
        task_id='extract_zip_file',
        python_callable=extract_task,
        provide_context=True,
    )

    t1 >> t2

def log_to_file(event: str, status: str, file_path="tracking_log.json"):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "status": status
    }
    with open(file_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
