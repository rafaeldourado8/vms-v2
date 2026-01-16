@echo off
echo ========================================
echo GT-Vision VMS - Start ELK Stack
echo ========================================
echo.

echo Starting ELK Stack (Elasticsearch, Logstash, Kibana)...
docker-compose -f docker-compose.dev.yml up -d elasticsearch logstash kibana

echo.
echo Waiting for services to be ready...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo ELK Stack Status
echo ========================================
echo Elasticsearch: http://localhost:9200
echo Kibana: http://localhost:5601
echo Logstash: localhost:5000 (TCP)
echo.

echo Checking Elasticsearch...
curl -s http://localhost:9200/_cluster/health

echo.
echo.
echo ========================================
echo ELK Stack is ready!
echo ========================================
