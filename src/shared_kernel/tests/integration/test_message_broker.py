"""Integration tests for RabbitMQ MessageBrokerConfig."""
import pytest
import pytest_asyncio
import asyncio
from uuid import uuid4

from shared_kernel.infrastructure.message_broker import MessageBrokerConfig
from shared_kernel.infrastructure.rabbitmq_connection import get_rabbitmq_url


@pytest_asyncio.fixture
async def message_broker():
    broker = MessageBrokerConfig(get_rabbitmq_url(), max_retries=2)
    await broker.connect()
    yield broker
    await broker.close()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_publish_and_consume_message(message_broker):
    """Test publishing and consuming a message."""
    test_queue = f"test_queue_{uuid4()}"
    received_messages = []
    
    async def callback(message: dict):
        received_messages.append(message)
    
    consume_task = asyncio.create_task(
        message_broker.consume(test_queue, callback)
    )
    
    await asyncio.sleep(0.5)
    
    test_message = {"test_id": str(uuid4()), "data": "test_data"}
    await message_broker.publish("", test_queue, test_message)
    
    await asyncio.sleep(1)
    
    assert len(received_messages) == 1
    assert received_messages[0]["test_id"] == test_message["test_id"]
    
    consume_task.cancel()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_connection_resilience(message_broker):
    """Test that connection is resilient."""
    assert message_broker.connection is not None
    assert not message_broker.connection.is_closed
    
    test_queue = f"test_queue_{uuid4()}"
    test_message = {"test": "resilience"}
    
    await message_broker.publish("", test_queue, test_message)
    
    assert not message_broker.connection.is_closed
