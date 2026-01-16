@echo off
echo ========================================
echo GT-Vision VMS - Setup (Desenvolvimento Local)
echo ========================================

echo.
echo [1/4] Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Docker nao encontrado. Instale o Docker Desktop.
    exit /b 1
)
echo OK: Docker instalado

echo.
echo [2/4] Criando arquivo .env...
if not exist .env (
    copy .env.example .env
    echo OK: Arquivo .env criado
) else (
    echo OK: Arquivo .env ja existe
)

echo.
echo [3/4] Instalando dependencias Python...
pip install poetry
poetry install
echo OK: Dependencias instaladas

echo.
echo [4/4] Instalando pre-commit hooks...
poetry run pre-commit install
echo OK: Pre-commit hooks instalados

echo.
echo ========================================
echo Setup concluido com sucesso!
echo ========================================
echo.
echo IMPORTANTE: Para Sprint 11, use:
echo   scripts\sprint11-setup.bat
echo.
echo Proximos passos (desenvolvimento local):
echo   1. Edite o arquivo .env se necessario
echo   2. Execute: scripts\sprint11-setup.bat
echo   3. Execute: poetry run python manage.py runserver
echo.
