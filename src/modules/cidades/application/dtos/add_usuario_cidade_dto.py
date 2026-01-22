"""Add Usuario Cidade DTO."""
from uuid import UUID

from src.shared_kernel.application.dto import DTO


class AddUsuarioCidadeDTO(DTO):
    """DTO for adding usuario to cidade."""

    cidade_id: UUID
    user_id: UUID
    tipo: str  # GESTOR or VISUALIZADOR
