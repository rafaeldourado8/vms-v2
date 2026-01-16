@echo off
echo ========================================
echo GT-Vision VMS - Iniciar Testes E2E
echo ========================================
echo.

echo [1/4] Verificando infraestrutura...
docker ps | findstr postgres >nul 2>&1
if errorlevel 1 (
    echo ERRO: PostgreSQL nao esta rodando
    echo Execute: scripts\sprint11-setup.bat
    pause
    exit /b 1
)
echo OK - Infraestrutura rodando
echo.

echo [2/4] Iniciando Django Backend (porta 8000)...
start "Django Backend" cmd /k "poetry run python manage.py runserver"
timeout /t 3 >nul
echo.

echo [3/4] Iniciando Streaming API (porta 8001)...
start "Streaming API" cmd /k "cd src\streaming && poetry run uvicorn infrastructure.web.main:app --reload --port 8001"
timeout /t 3 >nul
echo.

echo [4/4] Iniciando Detection API (porta 8002)...
start "Detection API" cmd /k "poetry run uvicorn src.detection.main:app --reload --port 8002"
timeout /t 3 >nul
echo.

echo ========================================
echo Todos os servicos foram iniciados!
echo ========================================
echo.
echo URLs:
echo   Django Backend:  http://localhost:8000
echo   Streaming API:   http://localhost:8001/docs
echo   Detection API:   http://localhost:8002/docs
echo.
echo Proximos passos:
echo   1. Teste Streaming:  python scripts\test_streaming_e2e.py
echo   2. Teste Deteccao:   python scripts\simulate_camera_detection.py
echo.
pause
