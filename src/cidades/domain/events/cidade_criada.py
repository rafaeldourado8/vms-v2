"""CidadeCriada domain event."""
from uuid import UUID

from src.shared_kernel.domain.domain_event import DomainEvent


class CidadeCriada(DomainEvent):
    """Event raised when cidade is created."""

    def __init__(self, cidade_id: UUID, nome: str, cnpj: str) -> None:
        """Initialize event."""
        super().__init__()
        self.cidade_id = cidade_id
        self.nome = nome
        self.cnpj = cnpj
