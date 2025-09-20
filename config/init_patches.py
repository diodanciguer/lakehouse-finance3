#!/usr/bin/env python3
"""
Script de inicialização para aplicar patches de URL antes de iniciar o API server
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('init_patches')

def apply_environment_fixes():
    """Aplica correções de variáveis de ambiente"""
    logger.info("[INIT_PATCHES] Aplicando correções de ambiente...")
    
    # Força variáveis de ambiente corretas
    os.environ['AIRFLOW__WEBSERVER__BASE_URL'] = 'https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
    os.environ['SERVER_NAME'] = 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
    os.environ['PREFERRED_URL_SCHEME'] = 'https'
    os.environ['FLASK_ENV'] = 'production'
    
    logger.info(f"[INIT_PATCHES] BASE_URL: {os.environ['AIRFLOW__WEBSERVER__BASE_URL']}")
    logger.info(f"[INIT_PATCHES] SERVER_NAME: {os.environ['SERVER_NAME']}")
    logger.info(f"[INIT_PATCHES] URL_SCHEME: {os.environ['PREFERRED_URL_SCHEME']}")

def apply_python_patches():
    """Aplica patches Python para URL handling"""
    logger.info("[INIT_PATCHES] Aplicando patches Python...")
    
    try:
        # Adicionar caminho dos patches
        sys.path.insert(0, '/opt/airflow/config')
        
        # Importar e aplicar patches
        from url_patcher import apply_patches
        apply_patches()
        
        logger.info("[INIT_PATCHES] Patches Python aplicados com sucesso!")
        
    except Exception as e:
        logger.error(f"[INIT_PATCHES] Erro ao aplicar patches Python: {e}")
        # Não falhar - continuar sem patches se houver problemas
        
def main():
    """Função principal"""
    logger.info("[INIT_PATCHES] ========== INICIANDO PATCHES ==========")
    
    # Aplicar correções
    apply_environment_fixes()
    apply_python_patches()
    
    logger.info("[INIT_PATCHES] ========== PATCHES CONCLUÍDOS ==========")
    logger.info("[INIT_PATCHES] Pronto para iniciar Airflow API Server!")

if __name__ == "__main__":
    main()