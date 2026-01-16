@echo off
REM Script para executar testes Sprint 13

echo ========================================
echo GT-Vision VMS - Sprint 13 Tests
echo ========================================
echo.

echo [1/4] Testando HAProxy...
poetry run pytest tests/integration/test_haproxy.py -v
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Testes HAProxy falharam
    exit /b 1
)
echo.

echo [2/4] Testando Kong...
poetry run pytest tests/integration/test_kong.py -v
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Testes Kong falharam
    exit /b 1
)
echo.

echo [3/4] Testando E2E...
poetry run pytest tests/e2e/test_full_flow.py -v -m e2e
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Testes E2E falharam
    exit /b 1
)
echo.

echo [4/4] Testando Seguranca (Sprint 13 anterior)...
poetry run pytest tests/integration/test_auth.py tests/integration/test_lgpd.py -v
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Testes Seguranca falharam
    exit /b 1
)
echo.

echo ========================================
echo SUCESSO! Todos os testes passaram
echo ========================================
