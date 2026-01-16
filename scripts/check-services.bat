@echo off
echo ========================================
echo Status dos Servicos
echo ========================================
echo.
docker-compose -f docker-compose.dev.yml ps
echo.
echo ========================================
echo Testando APIs
echo ========================================
echo.
echo Streaming API:
curl -s http://localhost:8001/health
echo.
echo.
echo Detection API:
curl -s http://localhost:8002/health
echo.
echo.
echo MediaMTX:
curl -s http://localhost:9997/v3/config/get
echo.
pause
