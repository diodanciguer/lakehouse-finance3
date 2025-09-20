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
from flask import request, redirect, url_for
import re

# Hook para interceptar redirects problemáticos
def check_redirect_url(endpoint, values):
    """Intercepta URLs de redirect e corrige se necessário"""
    if values and 'next' in values:
        next_url = values['next']
        # Se a URL contém o hostname interno, substituir pelo público
        if 'airflow3-api-server:8080' in next_url:
            values['next'] = next_url.replace(
                'http://airflow3-api-server:8080',
                'https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
            )
            print(f"[WEBSERVER CONFIG] URL de redirect corrigida: {values['next']}")
    return endpoint, values

# Middleware personalizado para interceptar redirects
class RedirectFixMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        def new_start_response(status, response_headers):
            # Interceptar redirects 302/301
            if status.startswith('302') or status.startswith('301'):
                for i, (header, value) in enumerate(response_headers):
                    if header.lower() == 'location':
                        # Corrigir URL de redirect se contém hostname interno
                        if 'airflow3-api-server:8080' in value:
                            new_value = value.replace(
                                'http://airflow3-api-server:8080',
                                'https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host'
                            )
                            response_headers[i] = (header, new_value)
                            print(f"[REDIRECT FIX] Corrigido: {value} -> {new_value}")
            return start_response(status, response_headers)
        return self.app(environ, new_start_response)

def init_app_proxy_fix(app):
    """Aplica o ProxyFix e middleware de correção de redirect"""
    # Aplicar ProxyFix primeiro
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1,
        x_prefix=1
    )
    # Aplicar middleware de correção de redirect
    app.wsgi_app = RedirectFixMiddleware(app.wsgi_app)
    return app

print(f"[WEBSERVER CONFIG] Base URL FORÇADA: {base_url}")
print(f"[WEBSERVER CONFIG] Proxy Fix habilitado: {ENABLE_PROXY_FIX}")
print(f"[WEBSERVER CONFIG] Cookie domain: {SESSION_COOKIE_DOMAIN}")
print(f"[WEBSERVER CONFIG] Middleware de correção de redirect ativado")
