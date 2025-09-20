# 🚀 Como Aplicar as Correções no Servidor

## 1. 📥 Fazer Pull das Mudanças

No servidor, execute:

```bash
cd /etc/easypanel/projects/lakehouse-finance3/airflow3/code
git pull origin main
```

## 2. 🔄 Reiniciar o Serviço

**⚠️ IMPORTANTE:** Use `docker compose` (sem hífen) no servidor:

```bash
# Parar o webserver
docker compose stop airflow3-api-server

# Remover o container (para forçar recriação)
docker compose rm -f airflow3-api-server

# Recriar e iniciar
docker compose up -d airflow3-api-server
```

## 3. 📊 Monitorar os Logs

```bash
# Ver logs em tempo real
docker compose logs -f airflow3-api-server

# Ver apenas as últimas 50 linhas
docker compose logs --tail=50 airflow3-api-server
```

## 4. 🔍 O que Procurar nos Logs

Você deve ver mensagens como:
- `[ENTRYPOINT] URL patches aplicados com sucesso!`
- `[URL_PATCHER] Patch aplicado ao módulo airflow.www.app`
- `[URL_PATCHER] Patch de redirect aplicado!`
- `[URL_PATCHER] Redirect interceptado: http://airflow3-api-server:8080/... -> https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host/...`

## 5. 🧪 Testar

Após o restart, acesse:
```
https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host/
```

Se ainda houver redirects problemáticos, você verá nos logs como eles estão sendo interceptados e corrigidos.

## 6. 🔧 Troubleshooting

Se ainda não funcionar:

```bash
# Verificar se os arquivos foram atualizados
ls -la config/url_patcher.py entrypoint.sh

# Verificar se o entrypoint tem permissões
chmod +x entrypoint.sh

# Rebuild completo (se necessário)
docker compose down
docker compose up -d
```

## 7. 📋 Comandos de Debug

```bash
# Ver estrutura dos containers
docker compose ps

# Ver variáveis de ambiente do container
docker compose exec airflow3-api-server env | grep -i airflow

# Acessar shell do container para debug
docker compose exec airflow3-api-server bash
```