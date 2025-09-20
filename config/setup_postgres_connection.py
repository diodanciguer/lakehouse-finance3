#!/usr/bin/env python3
"""
Script para configurar connection PostgreSQL Silver no Airflow
Deve ser executado dentro do container do Airflow
"""

import os
import sys
from airflow.models import Connection
from airflow.utils.db import provide_session

@provide_session
def create_postgres_connection(session=None):
    """
    Cria connection para o PostgreSQL Silver baseado nas credenciais do EasyPanel
    """
    
    # Configurações da conexão baseadas na imagem
    conn_id = 'postgres_silver_conn'
    host = 'lakehouse-finance3_db-silver3'  # Host interno do EasyPanel
    port = 5432
    database = 'lakehouse_finance_silver'
    username = 'silver_admin'
    password = 'S1lv3r!_pR72Lm#'  # Senha da imagem
    
    print(f"🔧 Configurando connection '{conn_id}'...")
    
    # Verificar se connection já existe
    existing_conn = session.query(Connection).filter(Connection.conn_id == conn_id).first()
    
    if existing_conn:
        print(f"⚠️  Connection '{conn_id}' já existe. Atualizando...")
        existing_conn.host = host
        existing_conn.port = port
        existing_conn.schema = database
        existing_conn.login = username
        existing_conn.password = password
        existing_conn.conn_type = 'postgres'
        connection = existing_conn
    else:
        print(f"✨ Criando nova connection '{conn_id}'...")
        connection = Connection(
            conn_id=conn_id,
            conn_type='postgres',
            host=host,
            port=port,
            schema=database,
            login=username,
            password=password,
            description='Conexão com PostgreSQL Silver via EasyPanel'
        )
        session.add(connection)
    
    try:
        session.commit()
        print(f"✅ Connection '{conn_id}' configurada com sucesso!")
        print(f"   📡 Host: {host}:{port}")
        print(f"   🏛️  Database: {database}")
        print(f"   👤 Usuário: {username}")
        return True
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao configurar connection: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Configurando PostgreSQL Silver Connection...")
    
    try:
        success = create_postgres_connection()
        if success:
            print("🎉 Connection configurada! Agora você pode executar a DAG de teste.")
            sys.exit(0)
        else:
            print("💥 Falha na configuração da connection.")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 Erro inesperado: {str(e)}")
        sys.exit(1)