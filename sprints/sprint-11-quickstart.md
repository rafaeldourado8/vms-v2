# Sprint 11 - Quick Start Guide

## 🎯 Objetivo
Migrar de in-memory para integração real com PostgreSQL, RabbitMQ e MinIO.

## 📋 Pré-requisitos
- Docker Desktop instalado e rodando
- Python 3.11+
- Poetry instalado

## 🚀 Setup Rápido

### 1. Iniciar Infraestrutura
```bash
# Executar script de setup
scripts\sprint11-setup.bat
```

Isso vai:
- ✅ Iniciar PostgreSQL (porta 5432)
- ✅ Iniciar Redis (porta 6379)
- ✅ Iniciar RabbitMQ (porta 5672, management 15672)
- ✅ Iniciar MinIO (porta 9000, console 9001)
- ✅ Iniciar MediaMTX (porta 8554 RTSP, 8888 HLS)
- ✅ Criar buckets no MinIO

### 2. Instalar Dependências
```bash
# Instalar/atualizar dependências (incluindo boto3 para MinIO)
poetry install
```

### 3. Aplicar Migrations
```bash
# Criar tabelas no PostgreSQL
poetry run python manage.py migrate
```

### 4. Verificar Conexões
```bash
# Testar conexão PostgreSQL
poetry run python -c "import psycopg2; conn = psycopg2.connect('dbname=gtvision user=gtvision password=gtvision_password host=localhost'); print('✅ PostgreSQL OK'); conn.close()"

# Testar conexão Redis
poetry run python -c "import redis; r = redis.Redis(host='localhost'); r.ping(); print('✅ Redis OK')"

# Testar conexão MinIO
poetry run python scripts\init_minio.py
```

## 📊 Status Atual

### ✅ Completo (Protótipos)
- Sprints 0-10: Lógica de domínio, use cases, testes unitários
- Repositórios in-memory funcionando
- APIs REST definidas

### 🚧 Em Andamento (Sprint 11)
- [ ] PostgreSQL migrations aplicadas
- [ ] Repositórios migrados para PostgreSQL
- [ ] RabbitMQ workers funcionando
- [ ] MinIO armazenando arquivos
- [ ] Testes de integração passando

## 🗄️ Estrutura do Banco

### Tabelas Criadas (init.sql)
1. **Admin Context**: users, roles, user_roles
2. **Cidades Context**: cidades, cameras
3. **Streaming Context**: streams, recordings, clips, mosaics
4. **AI Context**: lpr_events

Total: 9 tabelas + índices

## 🔧 Próximos Passos

### Fase 1: Verificar Ambiente (ATUAL)
- [x] Docker Compose configurado
- [x] MinIO adicionado
- [x] Migrations SQL criadas
- [x] Script de setup criado
- [ ] Executar setup e validar

### Fase 2: Migrar Repositories
- [ ] StreamRepository → PostgreSQL
- [ ] RecordingRepository → PostgreSQL
- [ ] ClipRepository → PostgreSQL
- [ ] MosaicRepository → PostgreSQL
- [ ] LPREventRepository → PostgreSQL
- [ ] CidadeRepository → PostgreSQL (já tem Django ORM)
- [ ] CameraRepository → PostgreSQL (já tem Django ORM)

### Fase 3: Integrar RabbitMQ
- [ ] Atualizar MessageBroker para RabbitMQ real
- [ ] RecordingWorker com RabbitMQ
- [ ] ClipWorker com RabbitMQ

### Fase 4: Validar MinIO
- [ ] Testar upload de recordings
- [ ] Testar upload de clips
- [ ] Testar upload de imagens LPR
- [ ] Testar lifecycle policies

### Fase 5: Testes E2E
- [ ] Criar stream → gravar → buscar gravação
- [ ] Criar clip → processar → download
- [ ] Receber evento LPR → armazenar imagem → buscar

## 🐳 Comandos Úteis

### Docker
```bash
# Ver logs
docker-compose -f docker-compose.dev.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.dev.yml logs -f postgres

# Parar tudo
docker-compose -f docker-compose.dev.yml down

# Parar e remover volumes (CUIDADO: apaga dados)
docker-compose -f docker-compose.dev.yml down -v

# Reiniciar um serviço
docker-compose -f docker-compose.dev.yml restart postgres
```

### PostgreSQL
```bash
# Conectar ao banco
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision

# Ver tabelas
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "\dt"

# Ver dados de uma tabela
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "SELECT * FROM users;"
```

### RabbitMQ
```bash
# Management UI
http://localhost:15672
# User: gtvision
# Pass: gtvision_password
```

### MinIO
```bash
# Console UI
http://localhost:9001
# User: minioadmin
# Pass: minioadmin

# Listar buckets
poetry run python -c "import boto3; s3=boto3.client('s3', endpoint_url='http://localhost:9000', aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin'); print(s3.list_buckets())"
```

## 📝 Checklist de Validação

### Infraestrutura
- [ ] PostgreSQL rodando e acessível
- [ ] Redis rodando e acessível
- [ ] RabbitMQ rodando e acessível
- [ ] MinIO rodando e acessível
- [ ] MediaMTX rodando e acessível
- [ ] Buckets criados no MinIO

### Aplicação
- [ ] Dependências instaladas (poetry install)
- [ ] Migrations aplicadas
- [ ] Django runserver funciona
- [ ] FastAPI streaming funciona
- [ ] Testes unitários passando
- [ ] Testes de integração passando

## 🎯 Meta da Sprint 11
**Tudo funcionando com integração real - sem in-memory!**

## 📞 Troubleshooting

### Erro: "Docker não encontrado"
- Instale Docker Desktop: https://www.docker.com/products/docker-desktop

### Erro: "Porta já em uso"
- Verifique se já tem serviços rodando nas portas 5432, 6379, 5672, 9000
- Pare os serviços ou mude as portas no docker-compose.dev.yml

### Erro: "MinIO buckets não criados"
- Execute manualmente: `poetry run python scripts\init_minio.py`
- Verifique se MinIO está rodando: `docker ps | findstr minio`

### Erro: "PostgreSQL connection refused"
- Aguarde 30s após `docker-compose up` para serviços iniciarem
- Verifique health: `docker-compose -f docker-compose.dev.yml ps`

## 📚 Documentação
- [Sprint 11 Integration Guide](sprint-11-integration-guide.md) - Guia completo
- [PROJECT_CONTEXT.md](../.context/PROJECT_CONTEXT.md) - Contexto do projeto
- [CURRENT_STATE.md](../.context/CURRENT_STATE.md) - Estado atual

---

**Status**: 📝 Pronto para execução
**Próximo passo**: Executar `scripts\sprint11-setup.bat`
