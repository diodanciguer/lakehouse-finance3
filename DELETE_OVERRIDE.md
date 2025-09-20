# 🗑️ Deletar docker-compose.override.yml do Servidor

## 🚨 ESSE ARQUIVO PODE ESTAR CAUSANDO O PROBLEMA!

O `docker-compose.override.yml` no servidor está sobrescrevendo nossas configurações.

## 💻 Comando para executar no servidor:

```bash
# Entrar na pasta do projeto
cd /etc/easypanel/projects/lakehouse-finance3/airflow3/code

# Deletar o arquivo problemático
rm docker-compose.override.yml

# Verificar se foi deletado
ls -la | grep override
```

## 🔄 Depois de deletar:

1. **No Easypanel**: Fazer um redeploy manual
2. **Ou via SSH**: Reiniciar os containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## ✅ Resultado esperado:

- URL não deve mais redirecionar para `airflow3-api-server:8080`
- Deve manter `https://lakehouse-finance3-airflow3.hjbbqx.easypanel.host`

---

💡 **Execute esse comando AGORA no servidor!**