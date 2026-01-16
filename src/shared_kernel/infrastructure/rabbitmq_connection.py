"""RabbitMQ connection helper."""
import os


def get_rabbitmq_url() -> str:
    """Get RabbitMQ connection URL from environment variables."""
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = os.getenv("RABBITMQ_PORT", "5672")
    user = os.getenv("RABBITMQ_USER", "gtvision")
    password = os.getenv("RABBITMQ_PASSWORD", "gtvision_password")
    vhost = os.getenv("RABBITMQ_VHOST", "/")
    
    return f"amqp://{user}:{password}@{host}:{port}{vhost}"
