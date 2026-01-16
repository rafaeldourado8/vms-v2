"""Logging configuration for GT-Vision VMS."""
import logging
import logging.handlers
import json
import os
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for Logstash."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "correlation_id"):
            log_data["correlation_id"] = record.correlation_id
        if hasattr(record, "audit_action"):
            log_data["audit_action"] = record.audit_action
        if hasattr(record, "resource_type"):
            log_data["resource_type"] = record.resource_type
        if hasattr(record, "resource_id"):
            log_data["resource_id"] = record.resource_id

        # Add exception info
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(service_name: str = "gtvision") -> None:
    """Setup structured logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler (development)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # Logstash handler disabled for now (pickle format issue)
    # Will be enabled when proper JSON TCP handler is implemented


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name)
