@echo off
REM GT-Vision VMS - Stop Infrastructure

echo Parando infraestrutura...
docker-compose -f docker-compose.dev.yml down

echo.
echo Infraestrutura parada!
echo.
