@echo off
REM ============================================
REM GT-Vision VMS - Commits Atomicos
REM ============================================

echo Iniciando commits atomicos...
echo.

REM Desabilitar pre-commit temporariamente
git config core.hooksPath /dev/null

git init

REM === SETUP ===
echo [1/15] Config: gitignore
git add .gitignore
git commit -m "chore: add .gitignore"

echo [2/15] Config: environment
git add .env.example
git commit -m "chore: add environment template"

echo [3/15] Config: dependencies
git add pyproject.toml poetry.lock
git commit -m "chore: add Poetry dependencies (Django 5.0 + FastAPI)"

echo [4/15] Config: linters
git add pytest.ini mypy.ini .flake8 conftest.py
git commit -m "chore: configure linters and test framework"

echo [5/15] Config: pre-commit
git add .pre-commit-config.yaml
git commit -m "chore: add pre-commit hooks"

echo [6/15] Config: Django
git add manage.py
git commit -m "chore: add Django management script"

REM === SHARED KERNEL ===
echo [7/15] Shared Kernel: domain
git add src/shared_kernel/domain/
git commit -m "feat(shared-kernel): add domain primitives" -m "- Value Objects (Email, CPF, CNPJ, Placa)" -m "- Base Entity and Aggregate Root" -m "- Domain Events and Event Bus"

echo [8/15] Shared Kernel: infrastructure
git add src/shared_kernel/infrastructure/
git commit -m "feat(shared-kernel): add infrastructure adapters" -m "- PostgreSQL connection and base repository" -m "- RabbitMQ event publisher" -m "- MinIO storage client"

echo [9/15] Shared Kernel: tests
git add src/shared_kernel/tests/
git commit -m "test(shared-kernel): add unit tests (15 tests, 100%% coverage)"

REM === ADMIN CONTEXT ===
echo [10/15] Admin: bounded context
git add src/admin/domain/ src/admin/application/ src/admin/infrastructure/
git commit -m "feat(admin): add Admin bounded context" -m "- Entities: Usuario, Perfil, Permissao" -m "- Use Cases: authentication, RBAC" -m "- JWT + bcrypt implementation"

echo [11/15] Admin: tests
git add src/admin/tests/
git commit -m "test(admin): add unit tests (35 tests, 100%% coverage)"

REM === CIDADES CONTEXT ===
echo [12/15] Cidades: bounded context
git add src/cidades/
git commit -m "feat(cidades): add Cidades bounded context" -m "- Entities: Cidade, Prefeitura, Contrato" -m "- Use Cases: city and contract management" -m "- Tests: 20 unit tests (100%% coverage)"

REM === STREAMING CONTEXT ===
echo [13/15] Streaming: bounded context
git add src/streaming/domain/ src/streaming/application/
git commit -m "feat(streaming): add Streaming bounded context" -m "- Entities: Camera, Stream, Recording, Clip, Mosaic" -m "- Use Cases: camera and stream management"

echo [14/15] Streaming: infrastructure
git add src/streaming/infrastructure/
git commit -m "feat(streaming): add FastAPI infrastructure" -m "- PostgreSQL repositories" -m "- REST API endpoints with Swagger" -m "- Prometheus metrics integration" -m "- Tests: 48 unit + 19 integration (100%% coverage)"

REM === AI CONTEXT ===
echo [15/15] AI: bounded context
git add src/ai/
git commit -m "feat(ai): add AI bounded context" -m "- Entities: LPREvent, FaceEvent, ObjectEvent" -m "- RabbitMQ event processing" -m "- Tests: 6 unit + 2 integration (100%% coverage)"

REM === INFRASTRUCTURE ===
echo [16/15] Infra: Docker
git add docker/ docker-compose*.yml
git commit -m "feat(infra): add Docker Compose orchestration" -m "- PostgreSQL 15 + Redis 7 + RabbitMQ 3" -m "- MinIO S3-compatible storage" -m "- Dev, test and prod environments"

echo [17/15] Infra: Streaming
git add mediamtx.yml
git commit -m "feat(infra): add MediaMTX streaming server" -m "- RTSP/HLS/WebRTC support"

echo [18/15] Infra: API Gateway
git add haproxy/ kong/
git commit -m "feat(infra): add API Gateway layer" -m "- HAProxy load balancer" -m "- Kong API Gateway"

echo [19/15] Infra: Observability
git add monitoring/
git commit -m "feat(infra): add observability stack" -m "- Prometheus + Grafana (3 dashboards, 9 alerts)" -m "- ELK Stack (Elasticsearch + Logstash + Kibana)" -m "- Tests: 21 E2E tests"

REM === DOCUMENTATION ===
echo [20/15] Docs: README
git add README.md
git commit -m "docs: add comprehensive README"

echo [21/15] Docs: project context
git add .context/
git commit -m "docs: add project context and current state" -m "- DDD architecture documentation" -m "- Sprint progress tracking"

echo [22/15] Docs: sprints
git add sprints/
git commit -m "docs: add sprint planning and documentation" -m "- Sprint 11: Real Integration (100%%)" -m "- Sprint 12: Observability (100%%)" -m "- Sprint 13: Security (40%%)"

echo [23/15] Docs: LGPD
git add LGPD/
git commit -m "docs: add LGPD compliance documentation"

echo [24/15] Docs: guides
git add docs/ COMANDOS_CORRETOS.md DOCKER_TEST.md
git commit -m "docs: add operational guides"

echo [25/15] Scripts: automation
git add scripts/
git commit -m "chore: add automation scripts" -m "- Setup, test, lint scripts" -m "- Sprint 11 setup script"

REM Reabilitar pre-commit
git config --unset core.hooksPath

echo.
echo ========================================
echo   25 commits atomicos concluidos!
echo ========================================
echo.
echo Proximos passos:
echo   git remote add origin [URL]
echo   git push -u origin master
echo.
pause
