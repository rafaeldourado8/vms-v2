from celery import Celery
import httpx
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    'observability_worker',
    broker='amqp://gtvision:gtvision_password@rabbitmq:5672/',
    backend='redis://redis:6379/0'
)


class ObservabilityService:
    """Serviço de observabilidade para monitorar infraestrutura."""
    
    def __init__(self):
        self.rabbitmq_api = "http://rabbitmq:15672/api"
        self.auth = ("gtvision", "gtvision_password")
        
        # Thresholds
        self.queue_message_threshold = 1000
        self.queue_consumer_threshold = 0
        self.memory_threshold_percent = 80
    
    async def check_rabbitmq_queues(self) -> List[Dict]:
        """Verifica filas do RabbitMQ."""
        
        alerts = []
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.rabbitmq_api}/queues",
                    auth=self.auth
                )
                
                if response.status_code != 200:
                    return [{
                        "severity": "critical",
                        "service": "RabbitMQ",
                        "message": "Cannot access RabbitMQ API"
                    }]
                
                queues = response.json()
                
                for queue in queues:
                    queue_name = queue.get("name")
                    messages = queue.get("messages", 0)
                    consumers = queue.get("consumers", 0)
                    
                    # Alerta: Muitas mensagens acumuladas
                    if messages > self.queue_message_threshold:
                        alerts.append({
                            "severity": "warning",
                            "service": "RabbitMQ",
                            "queue": queue_name,
                            "message": f"Queue {queue_name} has {messages} messages (threshold: {self.queue_message_threshold})",
                            "metric": "messages",
                            "value": messages
                        })
                    
                    # Alerta: Fila sem consumers
                    if messages > 0 and consumers == 0:
                        alerts.append({
                            "severity": "critical",
                            "service": "RabbitMQ",
                            "queue": queue_name,
                            "message": f"Queue {queue_name} has no consumers but {messages} messages pending",
                            "metric": "consumers",
                            "value": consumers
                        })
        
        except Exception as e:
            logger.error(f"Failed to check RabbitMQ: {e}")
            alerts.append({
                "severity": "critical",
                "service": "RabbitMQ",
                "message": f"Health check failed: {str(e)}"
            })
        
        return alerts
    
    async def check_rabbitmq_memory(self) -> List[Dict]:
        """Verifica uso de memória do RabbitMQ."""
        
        alerts = []
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{self.rabbitmq_api}/nodes",
                    auth=self.auth
                )
                
                if response.status_code == 200:
                    nodes = response.json()
                    
                    for node in nodes:
                        mem_used = node.get("mem_used", 0)
                        mem_limit = node.get("mem_limit", 1)
                        mem_percent = (mem_used / mem_limit) * 100
                        
                        if mem_percent > self.memory_threshold_percent:
                            alerts.append({
                                "severity": "warning",
                                "service": "RabbitMQ",
                                "node": node.get("name"),
                                "message": f"Memory usage at {mem_percent:.1f}% (threshold: {self.memory_threshold_percent}%)",
                                "metric": "memory_percent",
                                "value": round(mem_percent, 2)
                            })
        
        except Exception as e:
            logger.error(f"Failed to check RabbitMQ memory: {e}")
        
        return alerts
    
    async def send_admin_notification(self, alerts: List[Dict]):
        """Envia notificação para admin."""
        
        if not alerts:
            return
        
        # Filtrar apenas alertas críticos e warnings
        critical_alerts = [a for a in alerts if a.get("severity") in ["critical", "warning"]]
        
        if not critical_alerts:
            return
        
        # TODO: Integrar com serviço de notificação (email, Slack, etc)
        logger.critical(f"ADMIN ALERT: {len(critical_alerts)} issues detected")
        for alert in critical_alerts:
            logger.critical(f"  - [{alert['severity'].upper()}] {alert['message']}")


observability_service = ObservabilityService()


@celery_app.task(name='check_infrastructure_health')
def check_infrastructure_health():
    """
    Worker periódico de observabilidade.
    
    Verifica:
    - Filas do RabbitMQ engargaladas
    - Uso de memória
    - Consumers inativos
    
    Envia alertas para admin se necessário.
    """
    
    import asyncio
    
    async def run_checks():
        alerts = []
        
        # Verificar filas
        queue_alerts = await observability_service.check_rabbitmq_queues()
        alerts.extend(queue_alerts)
        
        # Verificar memória
        memory_alerts = await observability_service.check_rabbitmq_memory()
        alerts.extend(memory_alerts)
        
        # Enviar notificações
        await observability_service.send_admin_notification(alerts)
        
        return {
            "status": "completed",
            "alerts_count": len(alerts),
            "alerts": alerts
        }
    
    return asyncio.run(run_checks())


# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    'check-infrastructure-every-5min': {
        'task': 'check_infrastructure_health',
        'schedule': 300.0,  # 5 minutos
    },
}
