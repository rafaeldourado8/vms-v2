@echo off
echo ========================================
echo GT-Vision VMS - Code Quality Check
echo ========================================

echo.
echo [1/5] Black (formatacao)...
poetry run black src/
if %errorlevel% neq 0 (
    echo ERRO: Black falhou
    exit /b 1
)

echo.
echo [2/5] isort (imports)...
poetry run isort src/
if %errorlevel% neq 0 (
    echo ERRO: isort falhou
    exit /b 1
)

echo.
echo [3/5] flake8 (linting)...
poetry run flake8 src/
if %errorlevel% neq 0 (
    echo ERRO: flake8 falhou
    exit /b 1
)

echo.
echo [4/5] mypy (type checking)...
poetry run mypy src/
if %errorlevel% neq 0 (
    echo ERRO: mypy falhou
    exit /b 1
)

echo.
echo [5/5] bandit (security)...
poetry run bandit -r src/ -c pyproject.toml
if %errorlevel% neq 0 (
    echo ERRO: bandit falhou
    exit /b 1
)

echo.
echo ========================================
echo Code quality check passou!
echo ========================================
