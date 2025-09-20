#!/usr/bin/env python3
"""
Script de debug para verificar logs das tasks no Airflow 3
Executa dentro do container para acessar logs diretamente
"""

import os
import sys
import glob
from datetime import datetime

def debug_log_system():
    """
    Debug completo do sistema de logging
    """
    print("🔍 DEBUG: Sistema de Logging do Airflow 3")
    print("=" * 50)
    
    # 1. Verificar diretório de logs
    log_base = os.environ.get('AIRFLOW__LOGGING__BASE_LOG_FOLDER', '/opt/airflow/logs')
    print(f"📁 Base log folder: {log_base}")
    
    if os.path.exists(log_base):
        print("✅ Diretório de logs existe")
        
        # Listar conteúdo
        try:
            files = os.listdir(log_base)
            print(f"📋 Conteúdo ({len(files)} itens):")
            for item in sorted(files)[:10]:  # Primeiros 10
                path = os.path.join(log_base, item)
                if os.path.isdir(path):
                    print(f"   📂 {item}/")
                else:
                    size = os.path.getsize(path)
                    print(f"   📄 {item} ({size} bytes)")
        except Exception as e:
            print(f"❌ Erro ao listar: {e}")
    else:
        print("❌ Diretório de logs não existe!")
        return

    # 2. Procurar logs da DAG test_logs_simple
    dag_pattern = f"{log_base}/dag_id=test_logs_simple"
    print(f"\n🔎 Procurando logs da DAG: {dag_pattern}")
    
    dag_dirs = glob.glob(dag_pattern)
    if dag_dirs:
        print("✅ Encontrou diretórios da DAG:")
        for dag_dir in dag_dirs:
            print(f"   📂 {dag_dir}")
            
            # Listar runs
            run_pattern = f"{dag_dir}/run_id=*"
            runs = glob.glob(run_pattern)
            
            for run in runs[-3:]:  # Últimas 3 execuções
                print(f"   📂 {run}")
                
                # Listar tasks
                task_pattern = f"{run}/task_id=*"
                tasks = glob.glob(task_pattern)
                
                for task in tasks:
                    print(f"     📂 {task}")
                    
                    # Listar arquivos de log
                    log_files = glob.glob(f"{task}/*.log")
                    for log_file in log_files:
                        size = os.path.getsize(log_file)
                        print(f"       📄 {os.path.basename(log_file)} ({size} bytes)")
                        
                        # Mostrar início do arquivo se não estiver vazio
                        if size > 0:
                            try:
                                with open(log_file, 'r', encoding='utf-8') as f:
                                    content = f.read(500)  # Primeiros 500 caracteres
                                    print(f"       📖 Início do conteúdo:")
                                    print(f"       {content[:200]}{'...' if len(content) > 200 else ''}")
                            except Exception as e:
                                print(f"       ❌ Erro ao ler: {e}")
    else:
        print("❌ Não encontrou logs da DAG test_logs_simple")

    # 3. Verificar configurações de logging
    print(f"\n⚙️  Configurações de Logging:")
    log_vars = [
        'AIRFLOW__LOGGING__BASE_LOG_FOLDER',
        'AIRFLOW__LOGGING__REMOTE_LOGGING', 
        'AIRFLOW__LOGGING__LOGGING_LEVEL',
        'AIRFLOW__LOGGING__LOG_FORMAT',
        'AIRFLOW__WEBSERVER__LOG_FETCH_TIMEOUT_SEC'
    ]
    
    for var in log_vars:
        value = os.environ.get(var, 'NÃO DEFINIDA')
        print(f"   {var}: {value}")

    # 4. Teste de escrita no diretório de logs
    print(f"\n✍️  Teste de Escrita:")
    test_file = f"{log_base}/debug_test.txt"
    try:
        with open(test_file, 'w') as f:
            f.write(f"Debug test - {datetime.now()}\n")
        print("✅ Consegue escrever no diretório de logs")
        os.remove(test_file)
    except Exception as e:
        print(f"❌ Não consegue escrever: {e}")

    # 5. Verificar permissões
    print(f"\n👤 Permissões:")
    try:
        stat = os.stat(log_base)
        print(f"   Dono: {stat.st_uid}:{stat.st_gid}")
        print(f"   Modo: {oct(stat.st_mode)[-3:]}")
    except Exception as e:
        print(f"❌ Erro ao verificar permissões: {e}")

if __name__ == "__main__":
    try:
        debug_log_system()
    except Exception as e:
        print(f"💥 Erro inesperado: {e}")
        sys.exit(1)