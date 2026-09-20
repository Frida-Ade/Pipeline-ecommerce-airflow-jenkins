from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import BranchPythonOperator

from airflow.utils.trigger_rule import TriggerRule

default_args = {
    "owner": "boyede",
}

dag = DAG(
    dag_id="ecommerce_sales_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args
)

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/opt/airflow/data/processed/dataset.csv",
    poke_interval=30,
    timeout=300,
    dag=dag
)

def check_file_exists():
    print("Fichier détecté")


def check_file_not_empty():
    import pandas as pd

    df = pd.read_csv(
        "data/processed/dataset.csv"
    )

    if len(df) == 0:
        raise ValueError(
            "Le fichier est vide"
        )

    print("Fichier valide")


def quality_check():
    print("Contrôle qualité effectué")

def choose_branch():

    print("Validation terminée")

    return "load_data"
def load_data():

    print("Chargement des données")
def calculate_metrics(**context):

    metrics = {
        "status": "success"
    }

    context["ti"].xcom_push(
        key="metrics",
        value=metrics
    )

    print("KPI calculés")
def generate_report(**context):

    metrics = context["ti"].xcom_pull(
        task_ids="calculate_metrics",
        key="metrics"
    )

    with open(
        "data/processed/report.txt",
        "w"
    ) as f:
        f.write(str(metrics))

    print("Rapport généré")
def finalize():

    print("Workflow terminé")

check_file_task = PythonOperator(
    task_id="check_file_exists",
    python_callable=check_file_exists,
    dag=dag
)

check_empty_task = PythonOperator(
    task_id="check_file_not_empty",
    python_callable=check_file_not_empty,
    dag=dag
)

quality_task = PythonOperator(
    task_id="quality_check",
    python_callable=quality_check,
    dag=dag
)
branch_task = BranchPythonOperator(
    task_id="branch_validation",
    python_callable=choose_branch,
    dag=dag
)
load_data_task = PythonOperator(
    task_id="load_data",
    python_callable=load_data,
    dag=dag
)
calculate_metrics_task = PythonOperator(
    task_id="calculate_metrics",
    python_callable=calculate_metrics,
    dag=dag
)
report_task = PythonOperator(
    task_id="generate_report",
    python_callable=generate_report,
    dag=dag
)
final_task = PythonOperator(
    task_id="finalize",
    python_callable=finalize,
    trigger_rule=TriggerRule.ALL_DONE,
    dag=dag
)
categories = [
    "electronics",
    "computers",
    "furniture"
]

dynamic_tasks = []

for category in categories:

    task = PythonOperator(
        task_id=f"analyse_{category}",
        python_callable=lambda c=category:
            print(f"Analyse catégorie : {c}"),
        dag=dag
    )

    dynamic_tasks.append(task)

wait_for_file >> check_file_task

check_file_task >> check_empty_task

check_empty_task >> quality_task

quality_task >> branch_task

branch_task >> load_data_task

load_data_task >> calculate_metrics_task

calculate_metrics_task >> dynamic_tasks

for task in dynamic_tasks:
    task >> report_task

report_task >> final_task