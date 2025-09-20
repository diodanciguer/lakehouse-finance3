# 🔧 Variáveis de Ambiente para Easypanel

Copie e cole essas variáveis exatamente como estão no Easypanel:

## 📋 Environment Variables (Easypanel)

```env
# ==== Imagem / usuário do container ====
AIRFLOW_IMAGE_NAME=apache/airflow:3.0.6
AIRFLOW_UID=50000

# ==== Banco / Redis ====
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
POSTGRES_PORT=5432
REDIS_PORT=6379

# ==== Admin (criado só na 1ª subida) ====
_AIRFLOW_WWW_USER_USERNAME=diego
_AIRFLOW_WWW_USER_PASSWORD=Dg@24282323
_AIRFLOW_WWW_USER_EMAIL=diego@danciguer.com.br

# ==== Segurança / sessão / CSRF ====
AIRFLOW_SECRET_KEY=f7285c3767c18f2d08bdf81246d6145541b7cf3206a2e345d41563a54fb2ef9296b9378263fc101550784cb17584db124e8cb851f93225061514a294ef39d791
AIRFLOW__API__SECRET_KEY=f7285c3767c18f2d08bdf81246d6145541b7cf3206a2e345d41563a54fb2ef9296b9378263fc101550784cb17584db124e8cb851f93225061514a294ef39d791
AIRFLOW__CORE__FERNET_KEY=-goZ-ts3QlbwayQYIpQExVoyVyn994NUltsF9zVUFM8=

# ==== Webserver (UI pública) - CRÍTICO PARA RESOLVER O PROBLEMA ====
AIRFLOW__WEBSERVER__BASE_URL=https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host
AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX=True
AIRFLOW__WEBSERVER__COOKIE_SECURE=True
AIRFLOW__WEBSERVER__COOKIE_SAMESITE=None
AIRFLOW__WEBSERVER__PROXY_FIX_X_FOR=1
AIRFLOW__WEBSERVER__PROXY_FIX_X_PROTO=1
AIRFLOW__WEBSERVER__PROXY_FIX_X_HOST=1
AIRFLOW__WEBSERVER__PROXY_FIX_X_PORT=1
AIRFLOW__WEBSERVER__PROXY_FIX_X_PREFIX=1
AIRFLOW__WEBSERVER__ALLOWED_HOSTS=lakehouse-finance3-airflow3.hjbbqx.easypanel.host
AIRFLOW__WEBSERVER__FORCE_SECURE=True
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=False

# ==== Timezone ====
TZ=America/Sao_Paulo
AIRFLOW__CORE__DEFAULT_TIMEZONE=America/Sao_Paulo

# ==== Auth/UI (FAB) ====
AIRFLOW__CORE__AUTH_MANAGER=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-fab

# ==== Logging local ====
AIRFLOW__LOGGING__TASK_LOG_READER=task
AIRFLOW__LOGGING__REMOTE_LOGGING=False
AIRFLOW__LOGGING__BASE_LOG_FOLDER=/opt/airflow/logs
AIRFLOW__LOGGING__DAG_PROCESSOR_LOG_TARGET=/opt/airflow/logs/dag_processor
AIRFLOW__LOGGING__LOGGING_LEVEL=INFO

# ==== Comunicação interna (IMPORTANTE) ====
NO_PROXY=localhost,127.0.0.1,airflow3-api-server,airflow3-api,postgres3,redis3
```

## ⚠️ IMPORTANTE

1. **Apague TODAS as variáveis de ambiente atuais** no Easypanel
2. **Copie e cole EXATAMENTE** as variáveis acima
3. **Não modifique nada** - use exatamente como está
4. **Salve e redeploy** o serviço

## 🔍 Se ainda redirecionar para URL errada:

Adicione esta variável extra:

```env
AIRFLOW__WEBSERVER__WEB_SERVER_MASTER_TIMEOUT=300
AIRFLOW__WEBSERVER__WEB_SERVER_WORKER_TIMEOUT=300
```

---

💡 **O problema está na configuração das variáveis de ambiente no Easypanel!**