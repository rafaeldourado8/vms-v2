@echo off
echo ========================================
echo Reiniciando servicos...
echo ========================================
echo.

echo Parando RabbitMQ...
docker-compose stop rabbitmq
docker-compose rm -f rabbitmq

echo.
echo Iniciando RabbitMQ com novo healthcheck...
docker-compose up -d rabbitmq

echo.
echo Aguardando RabbitMQ ficar saudavel (60s)...
timeout /t 60 /nobreak

echo.
echo Iniciando servicos dependentes...
docker-compose up -d backend streaming frontend nginx haproxy kong

echo.
echo ========================================
echo Verificando status...
echo ========================================
docker-compose ps

echo.
echo Para ver logs: docker-compose logs -f [service_name]
