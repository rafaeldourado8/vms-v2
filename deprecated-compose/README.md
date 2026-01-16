# Arquivos Docker Compose Deprecados

Estes arquivos foram movidos para cá e desabilitados (extensão `.disabled`).

**NÃO USE ESTES ARQUIVOS!**

Use apenas o `docker-compose.yml` principal na raiz do projeto.

## Arquivos

- `docker-compose.dev.yml.disabled` - Antigo arquivo de desenvolvimento
- `docker-compose.test.yml.disabled` - Antigo arquivo de testes

Para usar o ambiente correto:

```bash
# Produção/Desenvolvimento
docker-compose up -d

# Apenas infraestrutura
docker-compose up -d postgres redis rabbitmq minio mediamtx
```
