@echo off
REM GT-Vision VMS - Cleanup Script
REM Para e remove TODOS os containers antigos

echo ========================================
echo GT-Vision VMS - Cleanup
echo ========================================
echo.

echo [1/3] Parando TODOS os containers do projeto...
docker-compose -f docker-compose.yml down -v 2>nul
docker-compose -f docker-compose.dev.yml down -v 2>nul
docker-compose -f docker-compose.test.yml down -v 2>nul
echo OK: Containers parados
echo.

echo [2/3] Removendo containers orfaos...
docker container prune -f
echo OK: Containers orfaos removidos
echo.

echo [3/3] Verificando containers restantes...
docker ps -a | findstr gtvision
echo.

echo ========================================
echo Cleanup concluido!
echo ========================================
echo.
echo Agora execute:
echo   scripts\sprint11-setup.bat
echo.
