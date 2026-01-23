"""PlanoAtribuido domain event."""
from uuid import UUID

from src.shared.domain.domain_event import DomainEvent


class PlanoAtribuido(DomainEvent):
    """Event raised when plano is assigned to cidade."""

    def __init__(self, cidade_id: UUID, tipo_plano: str) -> None:
        """Initialize event."""
        super().__init__()
        self.cidade_id = cidade_id
        self.tipo_plano = tipo_plano
