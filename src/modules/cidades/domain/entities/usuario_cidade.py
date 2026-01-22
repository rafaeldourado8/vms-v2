"""Usuario Cidade entity."""
from enum import Enum
from uuid import UUID

from src.shared_kernel.domain.entity import Entity


class TipoUsuarioCidade(str, Enum):
    """Tipos de usuário cidade."""

    GESTOR = "GESTOR"
    VISUALIZADOR = "VISUALIZADOR"


class UsuarioCidade(Entity):
    """Usuario Cidade entity."""

    def __init__(
        self,
        entity_id: UUID | None = None,
        user_id: UUID | None = None,
        tipo: TipoUsuarioCidade = TipoUsuarioCidade.VISUALIZADOR,
    ) -> None:
        """Initialize usuario cidade."""
        super().__init__(entity_id)
        self.user_id = user_id
        self.tipo = tipo

    def is_gestor(self) -> bool:
        """Check if is gestor."""
        return self.tipo == TipoUsuarioCidade.GESTOR

    def is_visualizador(self) -> bool:
        """Check if is visualizador."""
        return self.tipo == TipoUsuarioCidade.VISUALIZADOR

    def __repr__(self) -> str:
        """String representation."""
        return f"UsuarioCidade(user_id={self.user_id}, tipo={self.tipo})"
