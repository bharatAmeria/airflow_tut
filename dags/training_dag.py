from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='training_pipeline_orchestrator',
    default_args=default_args,
    description='Orchestrates data download, preprocessing, and training',
    schedule_interval=None,
    catchup=False,
    tags=['orchestration'],
) as dag:

    trigger_gdrive_pipeline = TriggerDagRunOperator(
        task_id='trigger_gdrive_pipeline',
        trigger_dag_id='gdrive_data_pipeline',
        wait_for_completion=True,
        reset_dag_run=True
    )

    trigger_preprocessing_pipeline = TriggerDagRunOperator(
        task_id='trigger_preprocessing_pipeline',
        trigger_dag_id='data_preprocessing_pipeline',
        wait_for_completion=True,
        reset_dag_run=True
    )

    trigger_model_training_pipeline = TriggerDagRunOperator(
        task_id='trigger_model_training_pipeline',
        trigger_dag_id='model_training_pipeline',
        wait_for_completion=True,
        reset_dag_run=True
    )

    # DAG execution flow
    trigger_gdrive_pipeline >> trigger_preprocessing_pipeline >> trigger_model_training_pipeline
