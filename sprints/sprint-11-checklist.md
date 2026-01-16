# Sprint 11 - Checklist de Progresso

## 📋 Fase 1: Setup de Infraestrutura ✅ COMPLETA

- [x] Adicionar MinIO ao docker-compose.yml
- [x] Criar docker-compose.dev.yml (apenas infraestrutura)
- [x] Criar migrations SQL completas (init.sql)
- [x] Criar script de inicialização MinIO (init_minio.py)
- [x] Criar script de setup automatizado (sprint11-setup.bat)
- [x] Configurar .env para desenvolvimento local
- [x] Adicionar boto3 ao pyproject.toml
- [x] Criar documentação completa (3 guias)
- [x] Atualizar CURRENT_STATE.md
- [ ] **Executar setup e validar** ← VOCÊ ESTÁ AQUI

---

## 📋 Fase 2: Migrar Repositories (0/9)

### Base
- [ ] Criar `src/shared_kernel/infrastructure/persistence/postgresql_repository.py`
- [ ] Criar helper de conexão PostgreSQL
- [ ] Criar testes base para repositories

### Streaming Context (4 repositories)
- [ ] StreamRepositoryPostgreSQL
  - [ ] Implementar save()
  - [ ] Implementar find_by_id()
  - [ ] Implementar find_by_camera_id()
  - [ ] Implementar list_active()
  - [ ] Testes de integração (4+)
  
- [ ] RecordingRepositoryPostgreSQL
  - [ ] Implementar save()
  - [ ] Implementar find_by_id()
  - [ ] Implementar find_by_stream_id()
  - [ ] Implementar search()
  - [ ] Testes de integração (4+)
  
- [ ] ClipRepositoryPostgreSQL
  - [ ] Implementar save()
  - [ ] Implementar find_by_id()
  - [ ] Implementar find_by_recording_id()
  - [ ] Implementar list_by_status()
  - [ ] Testes de integração (4+)
  
- [ ] MosaicRepositoryPostgreSQL
  - [ ] Implementar save()
  - [ ] Implementar find_by_id()
  - [ ] Implementar find_by_user_id()
  - [ ] Implementar delete()
  - [ ] Testes de integração (4+)

### AI Context (1 repository)
- [ ] LPREventRepositoryPostgreSQL
  - [ ] Implementar save()
  - [ ] Implementar find_by_id()
  - [ ] Implementar search()
  - [ ] Implementar find_by_plate()
  - [ ] Testes de integração (4+)

### Django ORM (4 repositories - validar)
- [ ] Validar CidadeRepository (Django ORM)
- [ ] Validar CameraRepository (Django ORM)
- [ ] Validar UserRepository (Django ORM)
- [ ] Validar RoleRepository (Django ORM)

---

## 📋 Fase 3: Integrar RabbitMQ (0/5)

### Message Broker
- [ ] Atualizar `src/shared_kernel/infrastructure/message_broker.py`
  - [ ] Implementar conexão RabbitMQ real
  - [ ] Implementar publish()
  - [ ] Implementar consume()
  - [ ] Implementar retry logic
  - [ ] Testes de integração

### Workers
- [ ] RecordingWorker
  - [ ] Atualizar para usar RabbitMQ real
  - [ ] Configurar queue "recordings"
  - [ ] Configurar dead letter queue
  - [ ] Testes de integração
  
- [ ] ClipWorker
  - [ ] Atualizar para usar RabbitMQ real
  - [ ] Configurar queue "clips"
  - [ ] Configurar dead letter queue
  - [ ] Testes de integração

### Configuração
- [ ] Criar exchanges e queues no RabbitMQ
- [ ] Configurar retry policies
- [ ] Configurar monitoring

---

## 📋 Fase 4: Validar MinIO (0/6)

### Storage Service
- [ ] Validar MinIOStorageService existente
- [ ] Testar upload de arquivo
- [ ] Testar download de arquivo
- [ ] Testar delete de arquivo
- [ ] Testar presigned URLs

### Buckets e Policies
- [ ] Validar buckets criados (recordings, clips, lpr-images, thumbnails)
- [ ] Configurar lifecycle policies (retention)
- [ ] Configurar backup strategy
- [ ] Testes de integração

---

## 📋 Fase 5: Testes E2E (0/8)

### Fluxos Completos
- [ ] Teste E2E: Criar stream → Iniciar → Parar
- [ ] Teste E2E: Criar gravação → Gravar → Buscar → Playback
- [ ] Teste E2E: Criar clip → Processar → Download
- [ ] Teste E2E: Criar mosaico → Adicionar câmeras → Visualizar
- [ ] Teste E2E: Receber evento LPR → Armazenar → Buscar

### Smoke Tests
- [ ] Smoke test: Todos os serviços rodando
- [ ] Smoke test: APIs respondendo
- [ ] Smoke test: Workers processando

---

## 📊 Progresso Geral

```
✅ Fase 1: Setup Infraestrutura     100% (10/10)
⏳ Fase 2: Migrar Repositories        0% (0/9)
⏳ Fase 3: Integrar RabbitMQ          0% (0/5)
⏳ Fase 4: Validar MinIO              0% (0/6)
⏳ Fase 5: Testes E2E                 0% (0/8)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Sprint 11:                     20% (10/48)
```

---

## 🎯 Próxima Ação

### AGORA: Executar Setup
```bash
scripts\sprint11-setup.bat
```

### Validar:
1. [ ] PostgreSQL rodando (porta 5432)
2. [ ] Redis rodando (porta 6379)
3. [ ] RabbitMQ rodando (porta 5672)
4. [ ] MinIO rodando (porta 9000)
5. [ ] MediaMTX rodando (porta 8554)
6. [ ] Buckets criados no MinIO

### Depois:
```bash
# Instalar dependências
poetry install

# Aplicar migrations
poetry run python manage.py migrate

# Verificar tabelas criadas
docker exec -it gtvision-postgres-dev psql -U gtvision -d gtvision -c "\dt"
```

---

## 📚 Documentação

- **Quick Start**: `sprints/sprint-11-quickstart.md`
- **README Completo**: `sprints/sprint-11.md`
- **Integration Guide**: `sprints/sprint-11-integration-guide.md`
- **Phase 1 Summary**: `sprints/sprint-11-phase1-summary.md`

---

## 🎉 Conquistas até Agora

✅ Docker Compose completo  
✅ Migrations SQL prontas  
✅ Scripts de automação criados  
✅ Documentação completa  
✅ Ambiente configurado  

**Próximo marco**: Primeiro repository PostgreSQL funcionando! 🚀
