#!/usr/bin/env python3
"""
Script para patching do Flask url_for no Airflow
Força todas as URLs geradas a usarem o domínio público correto
"""

import os
from functools import wraps
from flask import url_for as original_url_for, request
from werkzeug.urls import url_parse, url_unparse
import logging

logger = logging.getLogger(__name__)

# Configurações fixas
PUBLIC_BASE_URL = "https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host"
INTERNAL_PATTERNS = [
    "http://airflow3-api-server:8080",
    "https://airflow3-api-server:8080", 
    "airflow3-api-server:8080",
    "http://localhost:8080",
    "https://localhost:8080"
]

def fix_url(url):
    """Corrige URLs problemáticas"""
    if not url:
        return url
    
    original_url = url
    
    # Substituir padrões problemáticos
    for pattern in INTERNAL_PATTERNS:
        if pattern in url:
            url = url.replace(pattern, PUBLIC_BASE_URL)
            logger.info(f"[URL_PATCHER] Corrigido: {original_url} -> {url}")
            break
    
    # Se a URL não tem esquema mas parece ser uma URL completa, forçar HTTPS
    if url.startswith('//'):
        url = 'https:' + url
        logger.info(f"[URL_PATCHER] Adicionado https: {original_url} -> {url}")
    
    return url

def patched_url_for(endpoint, **values):
    """url_for patcheado que sempre usa o domínio público"""
    
    # Se há um parâmetro 'next', corrigir também
    if 'next' in values:
        values['next'] = fix_url(values['next'])
    
    try:
        # Forçar contexto com host correto se não estivermos em um request
        if not request:
            # Simular contexto de request com host correto
            with request.app.test_request_context(
                base_url=PUBLIC_BASE_URL,
                environ_overrides={'HTTP_HOST': 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'}
            ):
                url = original_url_for(endpoint, **values)
        else:
            url = original_url_for(endpoint, **values)
        
        # Aplicar correção na URL gerada
        return fix_url(url)
        
    except Exception as e:
        logger.error(f"[URL_PATCHER] Erro ao gerar URL para {endpoint}: {e}")
        # Fallback: tentar gerar URL básica
        try:
            url = original_url_for(endpoint, **values)
            return fix_url(url) 
        except:
            return f"{PUBLIC_BASE_URL}/{endpoint}"

def apply_patches():
    """Aplica os patches necessários"""
    logger.info("[URL_PATCHER] Aplicando patches de URL...")
    
    # Patch do Flask url_for
    import flask
    flask.url_for = patched_url_for
    
    # Patch do Airflow se disponível
    try:
        import airflow.www.app
        # Monkey patch no módulo do Airflow também
        airflow.www.app.url_for = patched_url_for
        logger.info("[URL_PATCHER] Patch aplicado ao módulo airflow.www.app")
    except ImportError:
        pass
    
    # Patch global
    import builtins
    builtins.url_for = patched_url_for
    
    logger.info("[URL_PATCHER] Patches aplicados com sucesso!")

if __name__ == "__main__":
    apply_patches()