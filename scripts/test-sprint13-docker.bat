@echo off
REM Script para executar testes Sprint 13 no Docker

echo ========================================
echo GT-Vision VMS - Sprint 13 Tests (Docker)
echo ========================================
echo.

echo [1/5] Iniciando servicos Docker...
docker-compose -f docker-compose.dev.yml up -d
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Falha ao iniciar servicos
    exit /b 1
)
echo.

echo Aguardando servicos ficarem prontos (30s)...
timeout /t 30 /nobreak
echo.

echo [2/5] Verificando saude dos servicos...
docker-compose -f docker-compose.dev.yml ps
echo.

echo [3/5] Executando testes de integracao (HAProxy + Kong)...
poetry run pytest tests/integration/test_haproxy.py tests/integration/test_kong.py -v --tb=short
if %ERRORLEVEL% NEQ 0 (
    echo AVISO: Alguns testes de integracao falharam
)
echo.

echo [4/5] Executando testes E2E...
poetry run pytest tests/e2e/test_full_flow.py -v -m e2e --tb=short
if %ERRORLEVEL% NEQ 0 (
    echo AVISO: Alguns testes E2E falharam
)
echo.

echo [5/5] Verificando logs dos servicos...
echo.
echo === Streaming API Logs ===
docker-compose -f docker-compose.dev.yml logs --tail=20 streaming
echo.
echo === Prometheus Logs ===
docker-compose -f docker-compose.dev.yml logs --tail=10 prometheus
echo.
echo === Elasticsearch Logs ===
docker-compose -f docker-compose.dev.yml logs --tail=10 elasticsearch
echo.

echo ========================================
echo Testes concluidos!
echo ========================================
echo.
echo Para parar os servicos:
echo   docker-compose -f docker-compose.dev.yml down
echo.
echo Para ver logs em tempo real:
echo   docker-compose -f docker-compose.dev.yml logs -f streaming
echo.
