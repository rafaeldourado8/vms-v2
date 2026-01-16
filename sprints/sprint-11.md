# Sprint 11 - Integração Real

**Data Início**: 2025-01-15  
**Status**: 🚧 EM ANDAMENTO - FASE 1  
**Objetivo**: Migrar de in-memory para PostgreSQL + RabbitMQ + MinIO

---

## 🎯 Objetivo da Sprint

Transformar os protótipos funcionais (Sprints 0-10) em um sistema real integrado com:
- ✅ PostgreSQL (banco de dados real)
- ✅ RabbitMQ (message broker real)
- ✅ MinIO (storage S3-compatible real)
- ✅ Redis (cache real)
- ✅ Docker Compose (orquestração)

---

## 📊 Escopo

### Repositórios a Migrar (9)
1. **StreamRepository** (in-memory → PostgreSQL)
2. **RecordingRepository** (in-memory → PostgreSQL)
3. **ClipRepository** (in-memory → PostgreSQL)
4. **MosaicRepository** (in-memory → PostgreSQL)
5. **LPREventRepository** (in-memory → PostgreSQL)
6. **CidadeRepository** (já usa Django ORM - validar)
7. **CameraRepository** (já usa Django ORM - validar)
8. **UserRepository** (já usa Django ORM - validar)
9. **RoleRepository** (já usa Django ORM - validar)

### Workers a Integrar (2)
1. **RecordingWorker** (mock → RabbitMQ real)
2. **ClipWorker** (mock → RabbitMQ real)

### Storage a Validar (1)
1. **MinIOStorageService** (já implementado - validar funcionamento)

---

## 🗄️ Banco de Dados

### Tabelas Criadas (init.sql)

#### Admin Context (3 tabelas)
- `users` - Usuários do sistema
- `roles` - Papéis/permissões
- `user_roles` - Relacionamento N:N

#### Cidades Context (2 tabelas)
- `cidades` - Prefeituras
- `cameras` - Câmeras das prefeituras

#### Streaming Context (4 tabelas)
- `streams` - Streams RTSP ativos
- `recordings` - Gravações cíclicas
- `clips` - Clipes de vídeo
- `mosaics` - Mosaicos de câmeras

#### AI Context (1 tabela)
- `lpr_events` - Eventos de detecção de placas

**Total**: 9 tabelas + 12 índices

---

## 🚀 Como Começar

### 1. Setup Inicial (5 minutos)

```bash
# Executar script de setup
scripts\sprint11-setup.bat
```

Isso vai:
- Iniciar PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX
- Criar buckets no MinIO
- Validar conexões

### 2. Instalar Dependências

```bash
poetry install
```

### 3. Aplicar Migrations

```bash
# Django migrations (se necessário)
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

### 4. Validar Setup

```bash
# Ver status dos containers
docker-compose -f docker-compose.dev.yml ps

# Testar PostgreSQL
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "\dt"

# Testar MinIO
poetry run python scripts\init_minio.py
```

---

## 📁 Arquivos Criados

### Infraestrutura
- ✅ `docker-compose.dev.yml` - Infraestrutura para dev local
- ✅ `docker/postgres/init.sql` - Migrations SQL completas
- ✅ `.env` - Configurações de desenvolvimento

### Scripts
- ✅ `scripts/sprint11-setup.bat` - Setup automatizado
- ✅ `scripts/init_minio.py` - Inicialização MinIO

### Documentação
- ✅ `sprints/sprint-11-quickstart.md` - Guia rápido
- ✅ `sprints/sprint-11-integration-guide.md` - Guia completo (já existia)
- ✅ `sprints/sprint-11.md` - Este arquivo

### Configuração
- ✅ `pyproject.toml` - Atualizado com boto3

---

## 📋 Fases da Sprint

### ✅ Fase 1: Setup de Infraestrutura (COMPLETA)
- [x] Docker Compose atualizado
- [x] MinIO adicionado
- [x] Migrations SQL criadas
- [x] Scripts de setup criados
- [x] Documentação criada
- [ ] **PRÓXIMO**: Executar setup e validar

### 🚧 Fase 2: Migrar Repositories (EM PLANEJAMENTO)
- [ ] Criar base class PostgreSQLRepository
- [ ] StreamRepositoryPostgreSQL
- [ ] RecordingRepositoryPostgreSQL
- [ ] ClipRepositoryPostgreSQL
- [ ] MosaicRepositoryPostgreSQL
- [ ] LPREventRepositoryPostgreSQL
- [ ] Testes de integração para cada repository

### ⏳ Fase 3: Integrar RabbitMQ (PENDENTE)
- [ ] Atualizar MessageBroker para RabbitMQ real
- [ ] RecordingWorker com RabbitMQ
- [ ] ClipWorker com RabbitMQ
- [ ] Dead letter queues
- [ ] Retry policies

### ⏳ Fase 4: Validar MinIO (PENDENTE)
- [ ] Testar upload de recordings
- [ ] Testar upload de clips
- [ ] Testar upload de imagens LPR
- [ ] Testar thumbnails
- [ ] Lifecycle policies (retention)

### ⏳ Fase 5: Testes E2E (PENDENTE)
- [ ] Fluxo completo: criar stream → gravar → buscar
- [ ] Fluxo completo: criar clip → processar → download
- [ ] Fluxo completo: evento LPR → armazenar → buscar
- [ ] Smoke tests
- [ ] Load tests básicos

---

## 🎯 Critérios de Sucesso

### Infraestrutura
- ✅ PostgreSQL rodando e acessível
- ✅ Redis rodando e acessível
- ✅ RabbitMQ rodando e acessível
- ✅ MinIO rodando e acessível
- ✅ MediaMTX rodando e acessível
- ✅ Buckets criados no MinIO

### Aplicação
- [ ] Todos os repositories usando PostgreSQL
- [ ] Workers processando mensagens via RabbitMQ
- [ ] Arquivos sendo armazenados no MinIO
- [ ] Testes unitários passando (>90% cobertura)
- [ ] Testes de integração passando (>80% cobertura)
- [ ] APIs REST funcionando end-to-end

### Qualidade
- [ ] Zero repositórios in-memory em produção
- [ ] Zero mocks de infraestrutura em produção
- [ ] Cobertura de testes mantida >90%
- [ ] Documentação atualizada

---

## 🐳 Serviços Disponíveis

Após executar `scripts\sprint11-setup.bat`:

| Serviço | Porta | URL | Credenciais |
|---------|-------|-----|-------------|
| PostgreSQL | 5432 | localhost:5432 | gtvision / gtvision_password |
| Redis | 6379 | localhost:6379 | - |
| RabbitMQ | 5672 | localhost:5672 | gtvision / gtvision_password |
| RabbitMQ Management | 15672 | http://localhost:15672 | gtvision / gtvision_password |
| MinIO API | 9000 | http://localhost:9000 | minioadmin / minioadmin |
| MinIO Console | 9001 | http://localhost:9001 | minioadmin / minioadmin |
| MediaMTX RTSP | 8554 | rtsp://localhost:8554 | - |
| MediaMTX HLS | 8888 | http://localhost:8888 | - |
| MediaMTX API | 9997 | http://localhost:9997 | - |

---

## 📝 Comandos Úteis

### Docker
```bash
# Ver logs de todos os serviços
docker-compose -f docker-compose.dev.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.dev.yml logs -f postgres

# Reiniciar um serviço
docker-compose -f docker-compose.dev.yml restart postgres

# Parar tudo
docker-compose -f docker-compose.dev.yml down

# Parar e limpar volumes (CUIDADO!)
docker-compose -f docker-compose.dev.yml down -v
```

### PostgreSQL
```bash
# Conectar ao banco
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision

# Listar tabelas
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "\dt"

# Ver estrutura de uma tabela
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "\d streams"

# Contar registros
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "SELECT COUNT(*) FROM streams;"
```

### MinIO
```bash
# Listar buckets
poetry run python -c "import boto3; s3=boto3.client('s3', endpoint_url='http://localhost:9000', aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin'); print([b['Name'] for b in s3.list_buckets()['Buckets']])"

# Listar objetos em um bucket
poetry run python -c "import boto3; s3=boto3.client('s3', endpoint_url='http://localhost:9000', aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin'); print([o['Key'] for o in s3.list_objects_v2(Bucket='recordings').get('Contents', [])])"
```

### RabbitMQ
```bash
# Listar queues
docker exec -it gtvision-rabbitmq-dev rabbitmqctl list_queues

# Listar exchanges
docker exec -it gtvision-rabbitmq-dev rabbitmqctl list_exchanges
```

---

## 🔧 Troubleshooting

### Problema: Docker não inicia
**Solução**: Verifique se Docker Desktop está rodando

### Problema: Porta já em uso
**Solução**: Pare serviços conflitantes ou mude portas no docker-compose.dev.yml

### Problema: MinIO buckets não criados
**Solução**: Execute manualmente `poetry run python scripts\init_minio.py`

### Problema: PostgreSQL connection refused
**Solução**: Aguarde 30s após docker-compose up para serviços iniciarem

### Problema: Migrations não aplicadas
**Solução**: Execute `poetry run python manage.py migrate`

---

## 📚 Documentação Relacionada

- [Quick Start Guide](sprint-11-quickstart.md) - Guia rápido de início
- [Integration Guide](sprint-11-integration-guide.md) - Guia completo de integração
- [PROJECT_CONTEXT.md](../.context/PROJECT_CONTEXT.md) - Contexto do projeto
- [CURRENT_STATE.md](../.context/CURRENT_STATE.md) - Estado atual

---

## 📊 Métricas

### Progresso Geral
- **Fase 1**: ✅ 100% (Setup completo)
- **Fase 2**: ⏳ 0% (Repositories)
- **Fase 3**: ⏳ 0% (RabbitMQ)
- **Fase 4**: ⏳ 0% (MinIO)
- **Fase 5**: ⏳ 0% (Testes E2E)

**Total Sprint**: 20% completo

### Tempo Estimado
- Fase 1: ✅ 0.5 dia (COMPLETO)
- Fase 2: 2 dias
- Fase 3: 1 dia
- Fase 4: 0.5 dia
- Fase 5: 1 dia

**Total**: 5 dias

---

## 🎉 Próximos Passos

1. ✅ **AGORA**: Executar `scripts\sprint11-setup.bat`
2. Validar todos os serviços rodando
3. Começar Fase 2: Migrar repositories
4. Criar testes de integração
5. Validar fluxos E2E

---

**Status**: 🚧 EM ANDAMENTO - FASE 1 COMPLETA  
**Última atualização**: 2025-01-15  
**Próxima ação**: Executar setup e validar infraestrutura
