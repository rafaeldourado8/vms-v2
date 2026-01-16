"""Message broker configuration and utilities."""
import json
from typing import Any, Callable, Optional
import asyncio

import aio_pika
from aio_pika import ExchangeType, DeliveryMode
from aio_pika.abc import AbstractIncomingMessage


class MessageBrokerConfig:
    """RabbitMQ message broker configuration."""

    def __init__(self, rabbitmq_url: str, max_retries: int = 3) -> None:
        """Initialize message broker config."""
        self.rabbitmq_url = rabbitmq_url
        self.max_retries = max_retries
        self.connection: Optional[aio_pika.abc.AbstractRobustConnection] = None
        self.channel: Optional[aio_pika.abc.AbstractChannel] = None

    async def connect(self) -> None:
        """Connect to RabbitMQ with retry logic."""
        if self.connection and not self.connection.is_closed:
            return
        
        self.connection = await aio_pika.connect_robust(
            self.rabbitmq_url,
            timeout=10
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

    async def declare_queue_with_dlx(self, queue_name: str) -> aio_pika.abc.AbstractQueue:
        """Declare queue with dead letter exchange."""
        if not self.channel:
            await self.connect()
        
        # Declare dead letter exchange and queue
        dlx_name = f"{queue_name}.dlx"
        dlq_name = f"{queue_name}.dlq"
        
        dlx = await self.channel.declare_exchange(dlx_name, ExchangeType.DIRECT, durable=True)
        dlq = await self.channel.declare_queue(dlq_name, durable=True)
        await dlq.bind(dlx, routing_key=queue_name)
        
        # Declare main queue with DLX
        queue = await self.channel.declare_queue(
            queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": dlx_name,
                "x-dead-letter-routing-key": queue_name
            }
        )
        
        return queue

    async def publish(self, exchange: str, routing_key: str, message: dict, retry_count: int = 0) -> None:
        """Publish message to exchange with retry logic."""
        if not self.channel:
            await self.connect()
        
        headers = {"x-retry-count": retry_count}
        
        # Use default exchange for direct queue publishing
        if exchange == "":
            await self.channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT,
                    headers=headers
                ),
                routing_key=routing_key
            )
        else:
            exchange_obj = await self.channel.declare_exchange(
                exchange,
                ExchangeType.TOPIC,
                durable=True
            )
            
            await exchange_obj.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=DeliveryMode.PERSISTENT,
                    headers=headers
                ),
                routing_key=routing_key
            )

    async def consume(self, queue: str, callback: Callable) -> None:
        """Subscribe to queue with automatic retry."""
        if not self.channel:
            await self.connect()
        
        queue_obj = await self.declare_queue_with_dlx(queue)
        
        async def wrapped_callback(message: AbstractIncomingMessage) -> None:
            async with message.process(ignore_processed=True):
                try:
                    body = json.loads(message.body.decode())
                    await callback(body)
                    await message.ack()
                except Exception as e:
                    retry_count = message.headers.get("x-retry-count", 0) if message.headers else 0
                    
                    if retry_count < self.max_retries:
                        # Retry with exponential backoff
                        await asyncio.sleep(2 ** retry_count)
                        await self.publish(
                            exchange="",
                            routing_key=queue,
                            message=body,
                            retry_count=retry_count + 1
                        )
                        await message.ack()
                    else:
                        # Send to DLQ
                        await message.reject(requeue=False)
        
        await queue_obj.consume(wrapped_callback)

    async def close(self) -> None:
        """Close connection."""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()


# Alias for backward compatibility
MessageBroker = MessageBrokerConfig
