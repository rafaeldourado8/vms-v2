"""Unit tests for Stream entity."""
import pytest
from uuid import uuid4
from src.streaming.domain.entities.stream import Stream
from src.streaming.domain.value_objects.stream_status import StreamStatus


@pytest.mark.unit
class TestStream:
    """Stream entity tests."""

    def test_create_stream(self):
        """Test create stream."""
        stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream",
            status=StreamStatus.STOPPED
        )
        assert stream.status == StreamStatus.STOPPED
        assert not stream.is_active()

    def test_start_stream(self):
        """Test start stream."""
        stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream"
        )
        stream.start()
        assert stream.status == StreamStatus.STARTING
        assert stream.started_at is not None
        assert stream.is_active()

    def test_mark_running(self):
        """Test mark stream as running."""
        stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream"
        )
        stream.start()
        stream.mark_running()
        assert stream.status == StreamStatus.RUNNING
        assert stream.is_active()

    def test_stop_stream(self):
        """Test stop stream."""
        stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream"
        )
        stream.start()
        stream.stop()
        assert stream.status == StreamStatus.STOPPED
        assert stream.stopped_at is not None
        assert not stream.is_active()

    def test_mark_error(self):
        """Test mark stream as error."""
        stream = Stream(
            id=uuid4(),
            camera_id=uuid4(),
            source_url="rtsp://192.168.1.100:554/stream"
        )
        stream.start()
        stream.mark_error()
        assert stream.status == StreamStatus.ERROR
        assert not stream.is_active()
