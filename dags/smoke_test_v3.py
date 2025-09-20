from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from pendulum import datetime

@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1, tz="America/Sao_Paulo"),
    catchup=False,
    tags=["smoke", "airflow3"],
)
def smoke_test_v3():
    @task
    def info():
        import os, socket, platform
        return {
            "hostname": socket.gethostname(),
            "python": platform.python_version(),
            "airflow_home": os.environ.get("AIRFLOW_HOME"),
        }

    @task
    def soma(a: int, b: int) -> int:
        return a + b

    @task
    def check(resultado: int, meta: dict):
        assert resultado == 3, f"Esperava 3, veio {resultado}"
        print("METADADOS:", meta)

    bash = BashOperator(
        task_id="bash_echo",
        bash_command="echo 'Hello from '$(hostname)'; date: '$(date -Iseconds)",
    )

    meta = info()
    total = soma(1, 2)
    bash >> check(total, meta)

dag = smoke_test_v3()