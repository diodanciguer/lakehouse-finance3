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
    
    # Log para depuração
    logger.info(f"[URL_PATCHER] Gerando URL para endpoint: {endpoint}, values: {values}")
    
    # Se há um parâmetro 'next', corrigir também
    if 'next' in values:
        original_next = values['next']
        values['next'] = fix_url(values['next'])
        logger.info(f"[URL_PATCHER] Parâmetro 'next' corrigido: {original_next} -> {values['next']}")
    
    try:
        # Sempre forçar base_url pública independente do contexto
        from flask import current_app
        
        # Salvar configuração original
        original_config = {}
        if current_app:
            original_config = {
                'SERVER_NAME': current_app.config.get('SERVER_NAME'),
                'PREFERRED_URL_SCHEME': current_app.config.get('PREFERRED_URL_SCHEME'),
            }
            
            # Forçar configurações corretas
            current_app.config['SERVER_NAME'] = 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
            current_app.config['PREFERRED_URL_SCHEME'] = 'https'
        
        # Gerar URL com contexto forçado
        try:
            url = original_url_for(endpoint, **values)
        finally:
            # Restaurar configuração original
            if current_app and original_config:
                for key, value in original_config.items():
                    if value is not None:
                        current_app.config[key] = value
        
        # Aplicar correção adicional na URL gerada
        fixed_url = fix_url(url)
        
        # Se ainda contém URL interna, forçar substituição completa
        if 'airflow3-api-server:8080' in fixed_url:
            fixed_url = fixed_url.replace('http://airflow3-api-server:8080', PUBLIC_BASE_URL)
            fixed_url = fixed_url.replace('https://airflow3-api-server:8080', PUBLIC_BASE_URL)
        
        logger.info(f"[URL_PATCHER] URL final: {fixed_url}")
        return fixed_url
        
    except Exception as e:
        logger.error(f"[URL_PATCHER] Erro ao gerar URL para {endpoint}: {e}")
        # Fallback mais robusto
        fallback_url = f"{PUBLIC_BASE_URL}/{endpoint.lstrip('/')}"
        if values:
            params = '&'.join([f"{k}={v}" for k, v in values.items()])
            fallback_url += f"?{params}"
        logger.info(f"[URL_PATCHER] Usando fallback: {fallback_url}")
        return fallback_url

def patch_flask_redirect():
    """Patch do Flask redirect para interceptar redirects diretos"""
    from flask import redirect as original_redirect
    
    def patched_redirect(location, code=302, Response=None):
        # Interceptar e corrigir a URL de redirect
        fixed_location = fix_url(location)
        logger.info(f"[URL_PATCHER] Redirect interceptado: {location} -> {fixed_location}")
        return original_redirect(fixed_location, code, Response)
    
    import flask
    flask.redirect = patched_redirect
    
    # Patch também no builtins
    import builtins
    builtins.redirect = patched_redirect
    
    logger.info("[URL_PATCHER] Patch de redirect aplicado!")

def patch_werkzeug_redirect():
    """Patch do Werkzeug para interceptar redirects em nível mais baixo"""
    try:
        from werkzeug.utils import redirect as werkzeug_redirect
        
        def patched_werkzeug_redirect(location, code=302, Response=None):
            fixed_location = fix_url(location)
            logger.info(f"[URL_PATCHER] Werkzeug redirect interceptado: {location} -> {fixed_location}")
            return werkzeug_redirect(fixed_location, code, Response)
        
        import werkzeug.utils
        werkzeug.utils.redirect = patched_werkzeug_redirect
        logger.info("[URL_PATCHER] Patch de Werkzeug redirect aplicado!")
    except ImportError:
        logger.info("[URL_PATCHER] Werkzeug não encontrado, pulando patch")

def apply_patches():
    """Aplica os patches necessários"""
    logger.info("[URL_PATCHER] Aplicando patches de URL...")
    
    # Patch do Flask url_for
    import flask
    flask.url_for = patched_url_for
    
    # Patch de redirects
    patch_flask_redirect()
    patch_werkzeug_redirect()
    
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