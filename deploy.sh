#!/bin/bash

# Script de Build e Deploy - GT-Vision VMS
# Uso: ./deploy.sh [dev|prod]

set -e

ENV=${1:-dev}

echo "🚀 Iniciando deploy do GT-Vision VMS (ambiente: $ENV)"

# 1. Verificar se .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copie .env.example para .env e configure as variáveis"
    exit 1
fi

# 2. Verificar Google Maps API Key
if grep -q "YOUR_GOOGLE_MAPS_API_KEY_HERE" .env; then
    echo "⚠️  AVISO: Configure GOOGLE_MAPS_API_KEY no arquivo .env"
fi

# 3. Build das imagens
echo "🔨 Building Docker images..."
docker-compose build

# 4. Subir serviços de infraestrutura primeiro
echo "🗄️  Iniciando infraestrutura..."
docker-compose up -d postgres redis rabbitmq minio mediamtx

# 5. Aguardar serviços ficarem prontos
echo "⏳ Aguardando serviços de infraestrutura..."
sleep 10

# 6. Rodar migrations
echo "📊 Executando migrations..."
docker-compose run --rm backend python manage.py migrate

# 7. Criar superuser (apenas em dev)
if [ "$ENV" = "dev" ]; then
    echo "👤 Criando superuser (dev)..."
    docker-compose run --rm backend python manage.py createsuperuser --noinput --username admin --email admin@gtvision.com || true
fi

# 8. Subir todos os serviços
echo "🚀 Iniciando todos os serviços..."
docker-compose up -d

# 9. Verificar status
echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📡 Serviços disponíveis:"
echo "  - Frontend:        http://localhost"
echo "  - Django Admin:    http://localhost/admin"
echo "  - API Backend:     http://localhost/api/admin"
echo "  - API Streaming:   http://localhost/api/v1"
echo "  - Grafana:         http://localhost:3000 (admin/admin)"
echo "  - RabbitMQ:        http://localhost:15672 (gtvision/gtvision_password)"
echo "  - MinIO Console:   http://localhost:9001 (minioadmin/minioadmin)"
echo ""
echo "📝 Logs: docker-compose logs -f"
echo "🛑 Parar: docker-compose down"
