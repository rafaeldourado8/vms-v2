@echo off
REM GT-Vision VMS - Sprint 11 Setup Script
REM Inicializa infraestrutura e prepara ambiente

echo ========================================
echo GT-Vision VMS - Sprint 11 Setup
echo ========================================
echo.

REM 1. Verificar Docker
echo [1/6] Verificando Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Docker nao encontrado. Instale o Docker Desktop.
    exit /b 1
)
echo OK: Docker encontrado
echo.

REM 2. Parar containers antigos
echo [2/6] Parando containers antigos...
docker-compose -f docker-compose.dev.yml down -v
echo.

REM 3. Iniciar infraestrutura
echo [3/6] Iniciando infraestrutura (PostgreSQL, Redis, RabbitMQ, MinIO, MediaMTX)...
docker-compose -f docker-compose.dev.yml up -d
echo.

REM 4. Aguardar serviços ficarem prontos
echo [4/6] Aguardando servicos ficarem prontos (30s)...
timeout /t 30 /nobreak >nul
echo.

REM 5. Inicializar MinIO (criar buckets)
echo [5/6] Inicializando MinIO (criando buckets)...
poetry run python scripts\init_minio.py
if errorlevel 1 (
    echo AVISO: Erro ao inicializar MinIO. Verifique se o servico esta rodando.
)
echo.

REM 6. Verificar status
echo [6/6] Verificando status dos servicos...
docker-compose -f docker-compose.dev.yml ps
echo.

echo ========================================
echo Setup concluido!
echo ========================================
echo.
echo Servicos disponiveis:
echo - PostgreSQL:  localhost:5432
echo - Redis:       localhost:6379
echo - RabbitMQ:    localhost:5672 (Management: http://localhost:15672)
echo - MinIO:       localhost:9000 (Console: http://localhost:9001)
echo - MediaMTX:    localhost:8554 (RTSP), localhost:8888 (HLS)
echo.
echo Proximos passos:
echo 1. poetry install (instalar dependencias)
echo 2. poetry run python manage.py migrate (criar tabelas)
echo 3. poetry run python manage.py runserver (iniciar Django)
echo.
echo Para parar: docker-compose -f docker-compose.dev.yml down
echo ========================================
