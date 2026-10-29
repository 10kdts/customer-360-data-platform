"""DAG de referência. Importado apenas quando Airflow está disponível."""

from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
except ImportError:  # Permite análise estática sem instalar Airflow.
    DAG = None


if DAG:
    with DAG(
        dag_id="customer360_daily",
        start_date=datetime(2025, 1, 1),
        schedule="0 6 * * *",
        catchup=False,
        max_active_runs=1,
        default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
        tags=["customer360", "governed"],
    ) as dag:
        generate = BashOperator(task_id="generate_sources", bash_command="python -m src.customer360.generate")
        ingest = BashOperator(task_id="bronze_to_gold", bash_command="python -m src.customer360.pipeline")
        dbt_test = BashOperator(task_id="dbt_test", bash_command="dbt test")
        generate >> ingest >> dbt_test
