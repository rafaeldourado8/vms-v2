@echo off
echo ========================================
echo GT-Vision VMS - Executando Testes
echo ========================================

echo.
echo [1/3] Executando testes unitarios...
poetry run pytest -v -m unit
if %errorlevel% neq 0 (
    echo ERRO: Testes unitarios falharam
    exit /b 1
)

echo.
echo [2/3] Executando testes de integracao...
poetry run pytest -v -m integration
if %errorlevel% neq 0 (
    echo ERRO: Testes de integracao falharam
    exit /b 1
)

echo.
echo [3/3] Gerando relatorio de cobertura...
poetry run pytest --cov=src --cov-report=html --cov-report=term-missing --cov-fail-under=0

echo.
echo ========================================
echo Testes concluidos!
echo Relatorio: htmlcov/index.html
echo ========================================
echo.
echo NOTA: Meta de cobertura e 90%% (atual sera exibido acima)

