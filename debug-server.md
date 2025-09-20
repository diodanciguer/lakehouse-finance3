# 🔍 Script de Diagnóstico - Airflow 3.0.6

Execute estes comandos **no servidor** para diagnosticar o problema:

## 1. 📊 Status dos Containers

```bash
cd /etc/easypanel/projects/lakehouse-finance3/airflow3/code
docker compose ps
```

**Procure por:**
- Status: `Up` ou `Exited`
- Health: `healthy` ou `unhealthy`

## 2. 🔍 Logs Completos do API Server

```bash
# Ver logs completos
docker compose logs airflow3-api-server

# Ver logs em tempo real
docker compose logs -f --tail=100 airflow3-api-server
```

**Procure por:**
- `[INIT_PATCHES]` - Patches sendo aplicados
- Erros de inicialização
- `airflow api-server` - Comando sendo executado
- Porta 8080 sendo aberta

## 3. 🔄 Verificar se Container Está Rodando

```bash
# Lista todos containers
docker ps -a | grep airflow3-api-server

# Status detalhado
docker compose ps airflow3-api-server
```

## 4. 🌐 Testar Conectividade Interna

```bash
# Testar se porta 8080 responde DENTRO do container
docker compose exec airflow3-api-server curl -I http://localhost:8080

# Se o container não estiver rodando, forçar start
docker compose up -d airflow3-api-server
```

## 5. 🔧 Debug de Inicialização

```bash
# Executar comando manualmente para ver erros
docker compose exec airflow3-api-server bash -c "
export PYTHONPATH=/opt/airflow/config:\$PYTHONPATH
python3 /opt/airflow/config/init_patches.py
echo '--- Patches aplicados, tentando iniciar API server ---'
airflow api-server --port 8080 --hostname 0.0.0.0
"
```

## 6. 🏥 Health Check

```bash
# Verificar saúde do container
docker compose exec airflow3-api-server curl -fsS http://localhost:8080/health
```

## 7. 📋 Variáveis de Ambiente

```bash
# Verificar variáveis críticas
docker compose exec airflow3-api-server env | grep -E "(AIRFLOW|SERVER|FLASK)"
```

## 8. 🔄 Reset Completo (Se Necessário)

```bash
# Parar tudo
docker compose down

# Remover volumes (CUIDADO: apaga dados)
docker compose down --volumes

# Recriar do zero
docker compose up -d
```

---

## 📝 **Relatório de Debug**

Depois de executar os comandos, me envie:

1. **Output do `docker compose ps`**
2. **Logs completos do airflow3-api-server**
3. **Resultado do teste de conectividade interna**
4. **Qualquer mensagem de erro específica**

Com essas informações, posso identificar exatamente onde está o problema e corrigir!