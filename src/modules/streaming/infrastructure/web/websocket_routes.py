from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Dict, Set
import json
import asyncio
import aio_pika
import jwt
from datetime import datetime

router = APIRouter()

SECRET_KEY = "GT_VISION_SECRET_2025"
ALGORITHM = "HS256"


class ConnectionManager:
    """Gerencia conexões WebSocket por tenant."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
    
    async def connect(self, websocket: WebSocket, tenant_id: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = set()
        self.active_connections[tenant_id].add(websocket)
    
    def disconnect(self, websocket: WebSocket, tenant_id: str):
        if tenant_id in self.active_connections:
            self.active_connections[tenant_id].discard(websocket)
            if not self.active_connections[tenant_id]:
                del self.active_connections[tenant_id]
    
    async def broadcast_to_tenant(self, tenant_id: str, message: dict):
        """Envia mensagem para todos os clientes de um tenant."""
        if tenant_id not in self.active_connections:
            return
        
        dead_connections = set()
        for connection in self.active_connections[tenant_id]:
            try:
                await connection.send_json(message)
            except:
                dead_connections.add(connection)
        
        # Limpar conexões mortas
        for conn in dead_connections:
            self.disconnect(conn, tenant_id)
    
    async def start_rabbitmq_consumer(self):
        """Consome eventos do RabbitMQ e distribui via WebSocket."""
        self.rabbitmq_connection = await aio_pika.connect_robust(
            "amqp://gtvision:gtvision_password@rabbitmq:5672/"
        )
        self.rabbitmq_channel = await self.rabbitmq_connection.channel()
        
        # Declarar exchange
        exchange = await self.rabbitmq_channel.declare_exchange(
            "deteccoes.events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        
        # Criar fila temporária
        queue = await self.rabbitmq_channel.declare_queue("", exclusive=True)
        await queue.bind(exchange, routing_key="deteccoes.lpr")
        
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    try:
                        data = json.loads(message.body.decode())
                        tenant_id = data.get("tenant_id")
                        
                        if tenant_id:
                            # Enriquecer com timestamp de envio
                            data["ws_sent_at"] = datetime.utcnow().isoformat()
                            
                            # Broadcast para tenant
                            await self.broadcast_to_tenant(tenant_id, {
                                "type": "lpr_detection",
                                "data": data
                            })
                    except Exception as e:
                        print(f"Error processing message: {e}")


manager = ConnectionManager()


def verify_token(token: str) -> dict:
    """Valida JWT e retorna payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        return None


@router.websocket("/ws/alerts")
async def websocket_alerts(
    websocket: WebSocket,
    token: str = Query(...)
):
    """
    WebSocket para alertas em tempo real.
    
    Autenticação via JWT no query string.
    Filtra eventos por tenant_id do token.
    
    Exemplo de conexão:
    ws://localhost/ws/alerts?token=eyJ0eXAiOiJKV1QiLCJhbGc...
    """
    
    # Validar token
    payload = verify_token(token)
    if not payload:
        await websocket.close(code=1008, reason="Invalid token")
        return
    
    tenant_id = payload.get("tenant_id")
    if not tenant_id:
        await websocket.close(code=1008, reason="Missing tenant_id in token")
        return
    
    # Conectar
    await manager.connect(websocket, tenant_id)
    
    try:
        # Enviar mensagem de boas-vindas
        await websocket.send_json({
            "type": "connected",
            "tenant_id": tenant_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Manter conexão viva
        while True:
            # Receber ping do cliente (heartbeat)
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, tenant_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, tenant_id)


@router.on_event("startup")
async def startup_event():
    """Inicia consumer do RabbitMQ ao iniciar aplicação."""
    asyncio.create_task(manager.start_rabbitmq_consumer())
