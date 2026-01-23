"""Plano entity."""
from enum import Enum
from uuid import UUID

from src.shared.domain.entity import Entity


class TipoPlano(str, Enum):
    """Tipos de plano disponíveis."""

    BASICO = "BASICO"  # 7 dias
    INTERMEDIARIO = "INTERMEDIARIO"  # 15 dias
    AVANCADO = "AVANCADO"  # 30 dias


class Plano(Entity):
    """Plano entity."""

    DIAS_RETENCAO = {
        TipoPlano.BASICO: 7,
        TipoPlano.INTERMEDIARIO: 15,
        TipoPlano.AVANCADO: 30,
    }

    def __init__(
        self,
        entity_id: UUID | None = None,
        tipo: TipoPlano = TipoPlano.BASICO,
        nome: str = "",
        descricao: str = "",
    ) -> None:
        """Initialize plano."""
        super().__init__(entity_id)
        self.tipo = tipo
        self.nome = nome
        self.descricao = descricao

    @property
    def dias_retencao(self) -> int:
        """Get dias de retenção."""
        return self.DIAS_RETENCAO[self.tipo]

    def __repr__(self) -> str:
        """String representation."""
        return f"Plano(tipo={self.tipo}, dias={self.dias_retencao})"
