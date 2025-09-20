"""
DAG simples para testar se os logs aparecem no Airflow 3
Usa apenas operadores básicos, sem dependências externas
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import logging

# Configurações padrão
default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
}

# Definir a DAG
dag = DAG(
    'test_logs_simple',
    default_args=default_args,
    description='Teste simples de logs no Airflow 3',
    schedule_interval=None,
    catchup=False,
    tags=['teste', 'logs', 'simples'],
)

def python_function_test():
    """
    Função Python simples para testar logs
    """
    logging.info("🚀 Iniciando teste de logs Python...")
    logging.info("📝 Esta é uma mensagem de INFO")
    logging.warning("⚠️  Esta é uma mensagem de WARNING")
    logging.error("❌ Esta é uma mensagem de ERROR (não é erro real)")
    
    print("✅ Print normal funcionando")
    print("🔢 Testando números: 123, 456.789")
    print("🔤 Testando texto com acentos: çãõáéí")
    
    # Teste com dados
    dados = {
        'timestamp': datetime.now().isoformat(),
        'status': 'success',
        'contador': 42,
        'lista': [1, 2, 3, 'teste']
    }
    
    logging.info(f"📊 Dados de teste: {dados}")
    
    # Loop para testar múltiplas linhas
    for i in range(5):
        logging.info(f"🔄 Iteração {i+1}/5 - Tudo funcionando!")
    
    logging.info("🎉 Teste de logs Python concluído com sucesso!")
    return "Python test completed"

# Task 1: Teste básico com Bash
test_bash = BashOperator(
    task_id='test_bash_logs',
    bash_command='''
    echo "🚀 Iniciando teste Bash..."
    echo "📅 Data atual: $(date)"
    echo "👤 Usuário: $(whoami)"
    echo "📂 Diretório: $(pwd)"
    echo "🖥️  Sistema: $(uname -a)"
    echo ""
    echo "✅ Teste Bash concluído!"
    ''',
    dag=dag,
)

# Task 2: Teste com Python
test_python = PythonOperator(
    task_id='test_python_logs',
    python_callable=python_function_test,
    dag=dag,
)

# Task 3: Teste de comandos do sistema
test_system = BashOperator(
    task_id='test_system_info',
    bash_command='''
    echo "🔧 Informações do sistema:"
    echo "Memory usage:"
    free -h || echo "Comando free não disponível"
    echo ""
    echo "Disk usage:"
    df -h | head -10
    echo ""
    echo "Processes:"
    ps aux | head -10
    echo ""
    echo "Network:"
    ifconfig | head -20 || ip addr | head -20
    echo "✅ Informações coletadas!"
    ''',
    dag=dag,
)

# Task 4: Teste de variáveis de ambiente
test_env = BashOperator(
    task_id='test_environment_vars',
    bash_command='''
    echo "🌍 Variáveis de ambiente do Airflow:"
    echo "AIRFLOW_HOME: $AIRFLOW_HOME"
    echo "AIRFLOW__CORE__DAGS_FOLDER: $AIRFLOW__CORE__DAGS_FOLDER"
    echo "AIRFLOW__CORE__EXECUTOR: $AIRFLOW__CORE__EXECUTOR"
    echo "AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: [HIDDEN]"
    echo "PYTHONPATH: $PYTHONPATH"
    echo "PATH: $(echo $PATH | head -c 200)..."
    echo ""
    echo "Python version:"
    python3 --version
    echo ""
    echo "Airflow version:"
    airflow version || echo "Comando airflow não encontrado no PATH"
    echo "✅ Variáveis listadas!"
    ''',
    dag=dag,
)

def test_airflow_context(**context):
    """
    Testa o contexto do Airflow
    """
    logging.info("🎯 Testando contexto do Airflow...")
    
    # Informações básicas
    dag_id = context.get('dag').dag_id
    task_id = context.get('task').task_id
    execution_date = context.get('execution_date')
    run_id = context.get('run_id')
    
    logging.info(f"🔖 DAG ID: {dag_id}")
    logging.info(f"📋 Task ID: {task_id}")
    logging.info(f"📅 Execution Date: {execution_date}")
    logging.info(f"🆔 Run ID: {run_id}")
    
    # Teste de configurações
    conf = context.get('conf')
    if conf:
        logging.info(f"⚙️  Config: {conf}")
    
    # Variáveis do contexto
    logging.info("📝 Variáveis disponíveis no contexto:")
    for key in sorted(context.keys()):
        logging.info(f"   - {key}: {type(context[key])}")
    
    logging.info("🎉 Teste de contexto concluído!")
    return "Context test completed"

# Task 5: Teste de contexto
test_context = PythonOperator(
    task_id='test_airflow_context',
    python_callable=test_airflow_context,
    dag=dag,
)

# Definir dependências (sequencial)
test_bash >> test_python >> test_system >> test_env >> test_context