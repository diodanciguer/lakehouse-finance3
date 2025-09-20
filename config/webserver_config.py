"""
Configuração do Webserver do Airflow para resolver problemas de proxy reverso
"""
import os
from airflow import configuration as conf
from flask_appbuilder.security.manager import AUTH_DB

# Configurações de proxy reverso
ENABLE_PROXY_FIX = True

# Trust proxy headers for HTTPS termination
PROXY_FIX_X_FOR = 1
PROXY_FIX_X_PROTO = 1
PROXY_FIX_X_HOST = 1  
PROXY_FIX_X_PORT = 1
PROXY_FIX_X_PREFIX = 1

# Base URL pública - FORÇAR A URL CORRETA
base_url = 'https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host'

# Configuração de autenticação padrão
AUTH_TYPE = AUTH_DB
AUTH_USER_REGISTRATION = False
AUTH_USER_REGISTRATION_ROLE = "Viewer"

# Security settings
SECRET_KEY = os.environ.get('AIRFLOW_SECRET_KEY', os.environ.get('AIRFLOW__API__SECRET_KEY', 'default-secret'))
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# Session settings for reverse proxy
PERMANENT_SESSION_LIFETIME = 1800
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_DOMAIN = 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'

# Configuração adicional para evitar redirecionamentos incorretos
PREFERRED_URL_SCHEME = 'https'
SERVER_NAME = 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'

# Força configuração de proxy
from werkzeug.middleware.proxy_fix import ProxyFix
from flask import request, redirect, url_for, Response
import re
from urllib.parse import urlparse, urlunparse

# Função para corrigir URLs problemáticas
def fix_internal_url(url):
    """Corrige URLs internas para URLs públicas"""
    if not url:
        return url
    
    # Lista de padrões problemáticos para corrigir
    internal_patterns = [
        'http://airflow3-api-server:8080',
        'https://airflow3-api-server:8080',
        'airflow3-api-server:8080'
    ]
    
    fixed_url = url
    for pattern in internal_patterns:
        if pattern in fixed_url:
            fixed_url = fixed_url.replace(pattern, 'https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host')
            print(f"[URL FIX] Corrigido: {url} -> {fixed_url}")
    
    return fixed_url

# Middleware mais robusto
class URLFixMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        # Corrigir HOST e SERVER_NAME no environ se necessário
        if environ.get('HTTP_HOST') == 'airflow3-api-server:8080':
            environ['HTTP_HOST'] = 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
            print(f"[ENVIRON FIX] HTTP_HOST corrigido para: {environ['HTTP_HOST']}")
            
        if environ.get('SERVER_NAME') == 'airflow3-api-server':
            environ['SERVER_NAME'] = 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
            environ['SERVER_PORT'] = '443'
            print(f"[ENVIRON FIX] SERVER_NAME corrigido para: {environ['SERVER_NAME']}")
        
        def new_start_response(status, response_headers):
            # Interceptar e corrigir redirects
            if status.startswith('30'):
                for i, (header, value) in enumerate(response_headers):
                    if header.lower() == 'location':
                        fixed_value = fix_internal_url(value)
                        if fixed_value != value:
                            response_headers[i] = (header, fixed_value)
            return start_response(status, response_headers)
        
        return self.app(environ, new_start_response)

def init_app_proxy_fix(app):
    """Aplica ProxyFix e configurações para proxy reverso"""
    
    # Configurar Flask app para usar HTTPS e host correto
    app.config.update({
        'PREFERRED_URL_SCHEME': 'https',
        'SERVER_NAME': 'lakehouse-finance3-airflow3.hjbbqx.easypanel.host',
        'APPLICATION_ROOT': '/',
    })
    
    # Aplicar ProxyFix para cabeçalhos de proxy
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1,
        x_prefix=1
    )
    
    # Aplicar middleware de correção de URL como segunda camada
    app.wsgi_app = URLFixMiddleware(app.wsgi_app)
    
    print(f"[WEBSERVER CONFIG] ProxyFix e URLFixMiddleware aplicados!")
    return app

# Aplicar patches de URL ANTES de tudo
try:
    import sys
    import os
    sys.path.insert(0, '/opt/airflow/config')
    from url_patcher import apply_patches
    apply_patches()
    print(f"[WEBSERVER CONFIG] URL Patcher aplicado com sucesso!")
except Exception as e:
    print(f"[WEBSERVER CONFIG] ERRO ao aplicar URL Patcher: {e}")

print(f"[WEBSERVER CONFIG] Base URL FORÇADA: {base_url}")
print(f"[WEBSERVER CONFIG] Proxy Fix habilitado: {ENABLE_PROXY_FIX}")
print(f"[WEBSERVER CONFIG] Cookie domain: {SESSION_COOKIE_DOMAIN}")
print(f"[WEBSERVER CONFIG] Middleware de correção de redirect ativado")
