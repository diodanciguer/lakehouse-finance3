"""
DAG de teste de conexão com PostgreSQL Silver
Testa a conectividade com o banco lakehouse_finance_silver
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import logging

# Configurações padrão da DAG
default_args = {
    'owner': 'silver_admin',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Definir a DAG
dag = DAG(
    'test_postgres_silver_connection',
    default_args=default_args,
    description='Testa conexão com banco PostgreSQL Silver',
    schedule_interval=None,  # Execução manual apenas
    catchup=False,
    tags=['teste', 'postgresql', 'silver'],
)

def test_connection_python():
    """
    Função Python para testar conexão com PostgreSQL usando hook
    """
    try:
        # Usar o hook do PostgreSQL
        hook = PostgresHook(postgres_conn_id='postgres_silver_conn')
        
        # Executar query simples
        sql = "SELECT version(), current_database(), current_user, now() as test_time;"
        
        logging.info("🔌 Testando conexão com PostgreSQL Silver...")
        result = hook.get_first(sql)
        
        logging.info("✅ Conexão bem-sucedida!")
        logging.info(f"📊 Versão PostgreSQL: {result[0]}")
        logging.info(f"🏛️  Database: {result[1]}")
        logging.info(f"👤 Usuário: {result[2]}")
        logging.info(f"🕒 Timestamp: {result[3]}")
        
        return result
        
    except Exception as e:
        logging.error(f"❌ Erro na conexão: {str(e)}")
        raise

def test_tables_list():
    """
    Função para listar algumas tabelas do banco
    """
    try:
        hook = PostgresHook(postgres_conn_id='postgres_silver_conn')
        
        # Query para listar tabelas
        sql = """
        SELECT schemaname, tablename, tableowner 
        FROM pg_tables 
        WHERE schemaname NOT IN ('information_schema', 'pg_catalog')
        ORDER BY schemaname, tablename
        LIMIT 10;
        """
        
        logging.info("📋 Listando tabelas do banco...")
        results = hook.get_records(sql)
        
        if results:
            logging.info("✅ Tabelas encontradas:")
            for row in results:
                logging.info(f"  📄 {row[0]}.{row[1]} (owner: {row[2]})")
        else:
            logging.info("ℹ️  Nenhuma tabela de usuário encontrada")
            
        return results
        
    except Exception as e:
        logging.error(f"❌ Erro ao listar tabelas: {str(e)}")
        raise

# Task 1: Teste básico de conexão
test_connection_task = PythonOperator(
    task_id='test_basic_connection',
    python_callable=test_connection_python,
    dag=dag,
)

# Task 2: Query simples usando PostgresOperator
test_query_task = PostgresOperator(
    task_id='test_simple_query',
    postgres_conn_id='postgres_silver_conn',
    sql="""
    SELECT 
        'Teste PostgreSQL Silver' as message,
        current_database() as database_name,
        current_user as user_name,
        version() as postgres_version,
        now() as query_time;
    """,
    dag=dag,
)

# Task 3: Listar tabelas
list_tables_task = PythonOperator(
    task_id='list_database_tables',
    python_callable=test_tables_list,
    dag=dag,
)

# Task 4: Teste de contagem de registros (se houver tabelas)
count_test_task = PostgresOperator(
    task_id='test_count_queries',
    postgres_conn_id='postgres_silver_conn',
    sql="""
    -- Testa queries de contagem básicas
    SELECT 
        'Schema information_schema' as schema_name,
        COUNT(*) as table_count
    FROM information_schema.tables 
    WHERE table_schema = 'information_schema'
    
    UNION ALL
    
    SELECT 
        'Schema public' as schema_name,
        COUNT(*) as table_count
    FROM information_schema.tables 
    WHERE table_schema = 'public';
    """,
    dag=dag,
)

# Definir dependências das tasks
test_connection_task >> test_query_task >> list_tables_task >> count_test_task