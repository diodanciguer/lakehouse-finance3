#!/bin/bash
set -e

echo "[ENTRYPOINT] Inicializando Airflow Webserver com patches personalizados..."

# Aplicar patches de URL antes do Airflow inicializar
export PYTHONPATH="/opt/airflow/config:$PYTHONPATH"

# Forçar variáveis de ambiente corretas
export AIRFLOW__WEBSERVER__BASE_URL="https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host"
export SERVER_NAME="lakehouse-finance3-airflow3.hjbbqx.easypanel.host"
export PREFERRED_URL_SCHEME="https"
export FLASK_ENV="production"

echo "[ENTRYPOINT] Variáveis de ambiente configuradas:"
echo "  AIRFLOW__WEBSERVER__BASE_URL: $AIRFLOW__WEBSERVER__BASE_URL"
echo "  SERVER_NAME: $SERVER_NAME" 
echo "  PREFERRED_URL_SCHEME: $PREFERRED_URL_SCHEME"

# Aplicar patches de URL
python3 -c "
import sys
sys.path.insert(0, '/opt/airflow/config')
from url_patcher import apply_patches
apply_patches()
print('[ENTRYPOINT] URL patches aplicados com sucesso!')
"

echo "[ENTRYPOINT] Iniciando API server na porta 8080..."

# Executar o API server do Airflow (Airflow 3.x usa api-server em vez de webserver)
exec airflow api-server --port 8080 --hostname 0.0.0.0 "$@"
