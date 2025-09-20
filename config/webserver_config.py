"""
Configuração do Webserver do Airflow para resolver problemas de proxy reverso
"""
import os
from airflow import configuration as conf
from flask_appbuilder.security.manager import AUTH_REMOTE_USER

# Configurações de proxy reverso
ENABLE_PROXY_FIX = True

# Trust proxy headers for HTTPS termination
PROXY_FIX_X_FOR = 1
PROXY_FIX_X_PROTO = 1
PROXY_FIX_X_HOST = 1  
PROXY_FIX_X_PORT = 1
PROXY_FIX_X_PREFIX = 1

# Base URL pública
base_url = os.environ.get('AIRFLOW__WEBSERVER__BASE_URL', 'https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host')

# Configuração de autenticação (se necessário no futuro)
AUTH_TYPE = AUTH_REMOTE_USER
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Viewer"

# Security settings
SECRET_KEY = os.environ.get('AIRFLOW_SECRET_KEY', os.environ.get('AIRFLOW__API__SECRET_KEY'))
WTF_CSRF_ENABLED = True
WTF_CSRF_TIME_LIMIT = None

# Session settings for reverse proxy
PERMANENT_SESSION_LIFETIME = 1800
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = None

# Configuração adicional para evitar redirecionamentos incorretos
PREFERRED_URL_SCHEME = 'https'

print(f"[WEBSERVER CONFIG] Base URL configurada: {base_url}")
print(f"[WEBSERVER CONFIG] Proxy Fix habilitado: {ENABLE_PROXY_FIX}")