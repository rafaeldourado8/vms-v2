import hmac
import hashlib
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional
import aio_pika
import json


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


class LPRWebhookPayload(BaseModel):
    camera_id: str
    placa: str
    timestamp: datetime
    confianca: float = Field(ge=0.0, le=1.0)
    imagem_url: Optional[str] = None
    signature: str


class WebhookService:
    def __init__(self, rabbitmq_url: str, webhook_secret: str):
        self.rabbitmq_url = rabbitmq_url
        self.webhook_secret = webhook_secret
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.declare_exchange("deteccoes.events", aio_pika.ExchangeType.TOPIC, durable=True)

    def verify_signature(self, payload: dict, signature: str) -> bool:
        payload_str = json.dumps(payload, sort_keys=True, default=str)
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, expected_signature)

    async def publish_event(self, event_type: str, data: dict):
        if not self.channel:
            await self.connect()
        
        message = aio_pika.Message(
            body=json.dumps(data).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        
        await self.channel.default_exchange.publish(
            message,
            routing_key=f"deteccoes.{event_type}"
        )

    async def close(self):
        if self.connection:
            await self.connection.close()


webhook_service = WebhookService(
    rabbitmq_url="amqp://gtvision:gtvision_password@rabbitmq:5672/",
    webhook_secret="GT_VISION_WEBHOOK_SECRET_2025"
)


@router.post("/lpr", status_code=202)
async def receive_lpr_webhook(
    payload: LPRWebhookPayload,
    x_tenant_id: Optional[str] = Header(None)
):
    """
    Recebe eventos LPR de câmeras com detecção embarcada.
    
    Fluxo:
    1. Valida assinatura HMAC
    2. Enriquece dados com tenant_id
    3. Publica no RabbitMQ
    4. Retorna 202 Accepted
    """
    
    # Validar assinatura
    payload_dict = payload.model_dump(exclude={"signature"})
    if not webhook_service.verify_signature(payload_dict, payload.signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Enriquecer dados
    event_data = {
        "camera_id": payload.camera_id,
        "tenant_id": x_tenant_id,
        "tipo": "lpr",
        "placa": payload.placa,
        "confianca": payload.confianca,
        "timestamp": payload.timestamp.isoformat(),
        "imagem_url": payload.imagem_url,
        "received_at": datetime.utcnow().isoformat()
    }
    
    # Publicar no RabbitMQ
    await webhook_service.publish_event("lpr", event_data)
    
    return {"status": "accepted", "message": "Event queued for processing"}


@router.on_event("shutdown")
async def shutdown_event():
    await webhook_service.close()
