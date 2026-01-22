"""Domain exceptions for DDD."""


class DomainException(Exception):
    """Base exception for domain errors."""

    pass


class EntityNotFoundException(DomainException):
    """Raised when entity is not found."""

    pass


class ValidationException(DomainException):
    """Raised when validation fails."""

    pass


class BusinessRuleViolationException(DomainException):
    """Raised when business rule is violated."""

    pass


class ConcurrencyException(DomainException):
    """Raised when concurrency conflict occurs."""

    pass
