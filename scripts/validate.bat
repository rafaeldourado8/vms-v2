@echo off
echo ========================================
echo GT-Vision VMS - Validacao Completa
echo ========================================

set ERROR=0

echo.
echo [1/8] Verificando estrutura de pastas...
if not exist "src\shared_kernel" (
    echo ERRO: Pasta shared_kernel nao encontrada
    set ERROR=1
)
if not exist "src\admin" (
    echo ERRO: Pasta admin nao encontrada
    set ERROR=1
)
if not exist "src\cidades" (
    echo ERRO: Pasta cidades nao encontrada
    set ERROR=1
)
if not exist "src\streaming" (
    echo ERRO: Pasta streaming nao encontrada
    set ERROR=1
)
if not exist "src\ai" (
    echo ERRO: Pasta ai nao encontrada
    set ERROR=1
)
if %ERROR%==0 (
    echo OK: Estrutura de pastas correta
)

echo.
echo [2/8] Verificando arquivos de configuracao...
if not exist "pyproject.toml" (
    echo ERRO: pyproject.toml nao encontrado
    set ERROR=1
)
if not exist ".env.example" (
    echo ERRO: .env.example nao encontrado
    set ERROR=1
)
if not exist "docker-compose.yml" (
    echo ERRO: docker-compose.yml nao encontrado
    set ERROR=1
)
if %ERROR%==0 (
    echo OK: Arquivos de configuracao presentes
)

echo.
echo [3/8] Executando testes unitarios...
poetry run pytest -m unit -v
if %errorlevel% neq 0 (
    echo ERRO: Testes unitarios falharam
    set ERROR=1
) else (
    echo OK: Testes unitarios passaram
)

echo.
echo [4/8] Verificando cobertura de testes...
poetry run pytest --cov=src --cov-report=term-missing --cov-fail-under=90
if %errorlevel% neq 0 (
    echo ERRO: Cobertura abaixo de 90%%
    set ERROR=1
) else (
    echo OK: Cobertura acima de 90%%
)

echo.
echo [5/8] Verificando formatacao (black)...
poetry run black --check src/
if %errorlevel% neq 0 (
    echo ERRO: Codigo nao formatado
    set ERROR=1
) else (
    echo OK: Codigo formatado corretamente
)

echo.
echo [6/8] Verificando imports (isort)...
poetry run isort --check-only src/
if %errorlevel% neq 0 (
    echo ERRO: Imports nao ordenados
    set ERROR=1
) else (
    echo OK: Imports ordenados corretamente
)

echo.
echo [7/8] Verificando linting (flake8)...
poetry run flake8 src/
if %errorlevel% neq 0 (
    echo ERRO: Problemas de linting encontrados
    set ERROR=1
) else (
    echo OK: Linting passou
)

echo.
echo [8/8] Verificando type hints (mypy)...
poetry run mypy src/shared_kernel/
if %errorlevel% neq 0 (
    echo AVISO: Problemas de type hints encontrados
    echo (Continuando...)
) else (
    echo OK: Type hints corretos
)

echo.
echo ========================================
if %ERROR%==0 (
    echo SUCESSO: Todas as validacoes passaram!
    echo ========================================
    exit /b 0
) else (
    echo FALHA: Algumas validacoes falharam
    echo ========================================
    exit /b 1
)
