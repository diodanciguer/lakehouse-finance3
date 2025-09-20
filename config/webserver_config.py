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

def init_app_proxy_fix(app):
    """Aplica o ProxyFix para resolver problemas de proxy reverso"""
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
        x_port=1,
        x_prefix=1
    )
    return app

print(f"[WEBSERVER CONFIG] Base URL FORÇADA: {base_url}")
print(f"[WEBSERVER CONFIG] Proxy Fix habilitado: {ENABLE_PROXY_FIX}")
print(f"[WEBSERVER CONFIG] Cookie domain: {SESSION_COOKIE_DOMAIN}")
