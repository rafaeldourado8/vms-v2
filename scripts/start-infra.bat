@echo off
REM GT-Vision VMS - Start Infrastructure Only
REM Para desenvolvimento local Sprint 11

echo ========================================
echo GT-Vision VMS - Infraestrutura Dev
echo ========================================
echo.

echo Iniciando APENAS infraestrutura:
echo - PostgreSQL
echo - Redis
echo - RabbitMQ
echo - MinIO
echo - MediaMTX
echo.

docker-compose -f docker-compose.dev.yml up -d

echo.
echo ========================================
echo Infraestrutura iniciada!
echo ========================================
echo.
echo Ver status:
echo   docker-compose -f docker-compose.dev.yml ps
echo.
echo Ver logs:
echo   docker-compose -f docker-compose.dev.yml logs -f
echo.
echo Parar:
echo   docker-compose -f docker-compose.dev.yml down
echo.
