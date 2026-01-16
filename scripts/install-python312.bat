@echo off
REM Instalar Python 3.12 via Chocolatey

echo ========================================
echo Instalando Python 3.12
echo ========================================
echo.

echo Verificando Chocolatey...
where choco >nul 2>&1
if %errorlevel% neq 0 (
    echo Chocolatey nao encontrado. Instalando...
    echo.
    echo Execute este comando no PowerShell como Administrador:
    echo.
    echo Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    echo.
    echo Depois execute este script novamente.
    pause
    exit /b 1
)

echo Chocolatey encontrado!
echo.

echo Instalando Python 3.12...
choco install python312 -y

echo.
echo Atualizando PATH...
refreshenv

echo.
echo Verificando instalacao...
python --version

echo.
echo ========================================
echo Python 3.12 instalado!
echo ========================================
echo.
echo Proximos passos:
echo 1. Feche e reabra o terminal
echo 2. Execute: python --version
echo 3. Execute: poetry install
echo.

pause
