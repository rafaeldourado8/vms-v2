"""Integration tests for ELK Stack logging."""
import pytest
import logging
import json
from src.shared_kernel.infrastructure.logging_config import JSONFormatter, setup_logging


class TestJSONFormatter:
    """Test JSON log formatter."""

    def test_format_basic_log(self):
        """Test basic log formatting."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.module = "test"
        record.funcName = "test_func"

        result = formatter.format(record)
        log_data = json.loads(result)

        assert log_data["level"] == "INFO"
        assert log_data["logger"] == "test"
        assert log_data["message"] == "Test message"
        assert log_data["module"] == "test"
        assert log_data["function"] == "test_func"
        assert log_data["line"] == 10
        assert "timestamp" in log_data

    def test_format_with_extra_fields(self):
        """Test log formatting with extra fields."""
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        record.module = "test"
        record.funcName = "test_func"
        record.user_id = "user123"
        record.correlation_id = "corr456"
        record.audit_action = "CREATE"
        record.resource_type = "camera"
        record.resource_id = "cam789"

        result = formatter.format(record)
        log_data = json.loads(result)

        assert log_data["user_id"] == "user123"
        assert log_data["correlation_id"] == "corr456"
        assert log_data["audit_action"] == "CREATE"
        assert log_data["resource_type"] == "camera"
        assert log_data["resource_id"] == "cam789"

    def test_format_with_exception(self):
        """Test log formatting with exception."""
        formatter = JSONFormatter()
        try:
            raise ValueError("Test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="test.py",
            lineno=10,
            msg="Error occurred",
            args=(),
            exc_info=exc_info,
        )
        record.module = "test"
        record.funcName = "test_func"

        result = formatter.format(record)
        log_data = json.loads(result)

        assert log_data["level"] == "ERROR"
        assert "exception" in log_data
        assert "ValueError: Test error" in log_data["exception"]


class TestLoggingSetup:
    """Test logging setup."""

    def test_setup_logging(self):
        """Test logging setup creates handlers."""
        setup_logging("test_service")
        logger = logging.getLogger()

        assert len(logger.handlers) > 0
        assert logger.level == logging.INFO

    def test_get_logger(self):
        """Test getting logger instance."""
        from src.shared_kernel.infrastructure.logging_config import get_logger

        logger = get_logger("test_module")
        assert logger.name == "test_module"
        assert isinstance(logger, logging.Logger)
