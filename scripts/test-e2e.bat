@echo off
echo ========================================
echo Sprint 13 - Testes E2E Completos
echo ========================================
echo.

echo [1/3] Verificando servicos...
curl -s http://localhost:8001/health > nul
if %errorlevel% neq 0 (
    echo ERRO: Streaming API nao esta rodando
    echo Execute: docker-compose -f docker-compose.dev.yml up -d streaming
    exit /b 1
)
echo Streaming API: OK

echo.
echo [2/3] Executando testes E2E...
poetry run pytest src/streaming/tests/e2e/test_full_system_e2e.py -v -m e2e

echo.
echo [3/3] Relatorio de testes...
echo.
echo ========================================
echo Testes E2E concluidos!
echo ========================================
