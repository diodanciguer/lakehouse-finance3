"""
DAG simples Hello World para testar Airflow 3.0.6
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Configuração padrão da DAG
default_args = {
    'owner': 'diego',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definição da DAG
dag = DAG(
    'hello_world',
    default_args=default_args,
    description='DAG simples Hello World - Teste Airflow 3.0.6',
    schedule=None,  # Manual trigger only
    catchup=False,
    tags=['teste', 'hello_world', 'airflow3'],
)

def print_hello_python():
    """Função Python simples"""
    print("🎉 Hello World from Python!")
    print("✅ Airflow 3.0.6 está funcionando!")
    print(f"📅 Executado em: {datetime.now()}")
    return "Hello World Success!"

# Task 1: Bash Hello World
hello_bash = BashOperator(
    task_id='hello_bash',
    bash_command='echo "🚀 Hello World from Bash!" && echo "✅ Task Bash executada com sucesso!"',
    dag=dag,
)

# Task 2: Python Hello World
hello_python = PythonOperator(
    task_id='hello_python',
    python_callable=print_hello_python,
    dag=dag,
)

# Task 3: Verificar ambiente
check_env = BashOperator(
    task_id='check_environment',
    bash_command='''
        echo "🔍 Verificando ambiente:"
        echo "📂 Diretório atual: $(pwd)"
        echo "🖥️  Sistema: $(uname -a)"
        echo "🐍 Python: $(python --version)"
        echo "⚡ Airflow: $(airflow version)"
        echo "✅ Ambiente verificado com sucesso!"
    ''',
    dag=dag,
)

# Definir dependências: bash -> python -> check_env
hello_bash >> hello_python >> check_env
