from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from pywebpush import webpush, WebPushException
import json
from sqlalchemy import create_engine, text

router = APIRouter(prefix="/notifications", tags=["notifications"])

engine = create_engine('postgresql://gtvision:gtvision_password@postgres:5432/gtvision')

# VAPID keys (TODO: Gerar e mover para .env)
VAPID_PRIVATE_KEY = "YOUR_VAPID_PRIVATE_KEY"
VAPID_PUBLIC_KEY = "YOUR_VAPID_PUBLIC_KEY"
VAPID_CLAIMS = {"sub": "mailto:admin@gtvision.com"}


class PushSubscription(BaseModel):
    endpoint: str
    keys: dict  # {p256dh, auth}


class NotificationPayload(BaseModel):
    title: str
    body: str
    icon: Optional[str] = "/icon.png"
    badge: Optional[str] = "/badge.png"
    data: Optional[dict] = None


@router.post("/subscribe")
async def subscribe_push(
    subscription: PushSubscription,
    x_tenant_id: str = Header(...),
    user_id: str = Header(...)
):
    """
    Registra subscription de push notification.
    
    Cliente deve usar Push API do navegador:
    ```javascript
    const registration = await navigator.serviceWorker.register('/sw.js');
    const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: 'VAPID_PUBLIC_KEY'
    });
    ```
    """
    
    with engine.connect() as conn:
        query = text("""
            INSERT INTO push_subscriptions (
                tenant_id, user_id, endpoint, p256dh, auth, created_at
            ) VALUES (
                :tenant_id, :user_id, :endpoint, :p256dh, :auth, NOW()
            )
            ON CONFLICT (endpoint) DO UPDATE
            SET updated_at = NOW()
        """)
        
        conn.execute(query, {
            "tenant_id": x_tenant_id,
            "user_id": user_id,
            "endpoint": subscription.endpoint,
            "p256dh": subscription.keys.get("p256dh"),
            "auth": subscription.keys.get("auth")
        })
        conn.commit()
    
    return {"status": "subscribed"}


@router.delete("/unsubscribe")
async def unsubscribe_push(
    endpoint: str,
    x_tenant_id: str = Header(...)
):
    """Remove subscription de push notification."""
    
    with engine.connect() as conn:
        query = text("""
            DELETE FROM push_subscriptions
            WHERE tenant_id = :tenant_id AND endpoint = :endpoint
        """)
        
        conn.execute(query, {
            "tenant_id": x_tenant_id,
            "endpoint": endpoint
        })
        conn.commit()
    
    return {"status": "unsubscribed"}


class PushNotificationService:
    """Serviço para envio de push notifications."""
    
    async def send_to_user(
        self,
        tenant_id: str,
        user_id: str,
        notification: NotificationPayload
    ):
        """Envia notificação para um usuário específico."""
        
        with engine.connect() as conn:
            query = text("""
                SELECT endpoint, p256dh, auth
                FROM push_subscriptions
                WHERE tenant_id = :tenant_id AND user_id = :user_id
            """)
            
            subscriptions = conn.execute(query, {
                "tenant_id": tenant_id,
                "user_id": user_id
            }).fetchall()
            
            payload = json.dumps({
                "title": notification.title,
                "body": notification.body,
                "icon": notification.icon,
                "badge": notification.badge,
                "data": notification.data or {}
            })
            
            failed_endpoints = []
            
            for sub in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": sub.endpoint,
                            "keys": {
                                "p256dh": sub.p256dh,
                                "auth": sub.auth
                            }
                        },
                        data=payload,
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims=VAPID_CLAIMS
                    )
                except WebPushException as e:
                    if e.response.status_code in [404, 410]:
                        # Subscription expirada
                        failed_endpoints.append(sub.endpoint)
            
            # Limpar subscriptions expiradas
            if failed_endpoints:
                delete_query = text("""
                    DELETE FROM push_subscriptions
                    WHERE endpoint = ANY(:endpoints)
                """)
                conn.execute(delete_query, {"endpoints": failed_endpoints})
                conn.commit()
    
    async def send_to_tenant(
        self,
        tenant_id: str,
        notification: NotificationPayload,
        role_filter: Optional[str] = None
    ):
        """Envia notificação para todos os usuários de um tenant."""
        
        with engine.connect() as conn:
            if role_filter:
                query = text("""
                    SELECT DISTINCT ps.endpoint, ps.p256dh, ps.auth
                    FROM push_subscriptions ps
                    JOIN users u ON ps.user_id = u.id
                    JOIN user_roles ur ON u.id = ur.user_id
                    JOIN roles r ON ur.role_id = r.id
                    WHERE ps.tenant_id = :tenant_id AND r.name = :role
                """)
                subscriptions = conn.execute(query, {
                    "tenant_id": tenant_id,
                    "role": role_filter
                }).fetchall()
            else:
                query = text("""
                    SELECT endpoint, p256dh, auth
                    FROM push_subscriptions
                    WHERE tenant_id = :tenant_id
                """)
                subscriptions = conn.execute(query, {
                    "tenant_id": tenant_id
                }).fetchall()
            
            payload = json.dumps({
                "title": notification.title,
                "body": notification.body,
                "icon": notification.icon,
                "badge": notification.badge,
                "data": notification.data or {}
            })
            
            for sub in subscriptions:
                try:
                    webpush(
                        subscription_info={
                            "endpoint": sub.endpoint,
                            "keys": {
                                "p256dh": sub.p256dh,
                                "auth": sub.auth
                            }
                        },
                        data=payload,
                        vapid_private_key=VAPID_PRIVATE_KEY,
                        vapid_claims=VAPID_CLAIMS
                    )
                except WebPushException:
                    pass  # Ignorar falhas individuais


push_service = PushNotificationService()


@router.post("/send")
async def send_notification(
    notification: NotificationPayload,
    x_tenant_id: str = Header(...),
    target_user_id: Optional[str] = None
):
    """
    Envia push notification.
    
    Se target_user_id for fornecido, envia apenas para esse usuário.
    Caso contrário, envia para todos do tenant.
    """
    
    if target_user_id:
        await push_service.send_to_user(x_tenant_id, target_user_id, notification)
    else:
        await push_service.send_to_tenant(x_tenant_id, notification)
    
    return {"status": "sent"}


# Exemplo de uso em eventos LPR
async def notify_lpr_detection(tenant_id: str, detection_data: dict):
    """Notifica gestores sobre detecção LPR."""
    
    notification = NotificationPayload(
        title="🚗 Detecção de Placa",
        body=f"Placa {detection_data['placa']} detectada",
        data={
            "type": "lpr_detection",
            "camera_id": detection_data["camera_id"],
            "placa": detection_data["placa"],
            "url": f"/detections/{detection_data['id']}"
        }
    )
    
    # Enviar apenas para gestores
    await push_service.send_to_tenant(tenant_id, notification, role_filter="gestor")
