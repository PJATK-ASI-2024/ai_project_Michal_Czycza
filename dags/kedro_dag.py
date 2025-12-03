"""
Apache Airflow DAG dla projektu ai_project_movies.
Integruje pipeline'y Kedro: EDA → Preprocessing → Modeling → Evaluation
"""

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Ścieżka do projektu Kedro w Dockerze
PROJECT_PATH = "/opt/project"

# Domyślne argumenty dla DAG-u
default_args = {
    "owner": "Michal_Czycza",
    "depends_on_past": False,
    "start_date": datetime(2025, 12, 3),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Definicja DAG-u
with DAG(
    dag_id="kedro_project_pipeline",
    default_args=default_args,
    description="Pełny pipeline ML: EDA → Preprocessing → Modeling → Evaluation",
    schedule_interval=None,  # Manualne uruchamianie (można zmienić na "@daily" dla codziennego uruchamiania)
    catchup=False,
    tags=["kedro", "ml", "mlops", "movies", "recommendation"],
) as dag:

    # Task 1: EDA Pipeline
    eda_task = BashOperator(
        task_id="eda_pipeline",
        bash_command=f"cd {PROJECT_PATH} && python -m kedro run --pipeline=eda",
        env={"PYTHONUNBUFFERED": "1"},
    )

    # Task 2: Preprocessing Pipeline
    preprocessing_task = BashOperator(
        task_id="preprocessing_pipeline",
        bash_command=f"cd {PROJECT_PATH} && python -m kedro run --pipeline=preprocessing",
        env={"PYTHONUNBUFFERED": "1"},
    )

    # Task 3: Modeling Pipeline
    modeling_task = BashOperator(
        task_id="modeling_pipeline",
        bash_command=f"cd {PROJECT_PATH} && python -m kedro run --pipeline=modeling",
        env={"PYTHONUNBUFFERED": "1"},
    )

    # Task 4: Evaluation Pipeline
    evaluation_task = BashOperator(
        task_id="evaluation_pipeline",
        bash_command=f"cd {PROJECT_PATH} && python -m kedro run --pipeline=evaluation",
        env={"PYTHONUNBUFFERED": "1"},
    )

    # Definicja zależności między taskami (Workflow)
    # EDA → Preprocessing → Modeling → Evaluation
    eda_task >> preprocessing_task >> modeling_task >> evaluation_task
