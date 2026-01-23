"""Cidade aggregate root."""
from typing import List, Optional
from uuid import UUID

from src.modules.cidades.domain.entities.camera import Camera
from src.modules.cidades.domain.entities.plano import Plano
from src.modules.cidades.domain.entities.usuario_cidade import TipoUsuarioCidade, UsuarioCidade
from src.modules.cidades.domain.events.cidade_criada import CidadeCriada
from src.modules.cidades.domain.events.plano_atribuido import PlanoAtribuido
from src.modules.cidades.domain.value_objects.cnpj import CNPJ
from src.modules.cidades.domain.value_objects.limite_cameras import LimiteCameras
from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.domain_exception import (
    BusinessRuleViolationException,
    ValidationException,
)


class Cidade(AggregateRoot):
    """Cidade aggregate root."""

    MAX_VISUALIZADORES = 5

    def __init__(
        self,
        entity_id: UUID | None = None,
        nome: str = "",
        cnpj: CNPJ | None = None,
        plano: Plano | None = None,
        limite_cameras: LimiteCameras | None = None,
        usuarios: List[UsuarioCidade] | None = None,
        cameras: List[Camera] | None = None,
    ) -> None:
        """Initialize cidade."""
        super().__init__(entity_id)
        if not nome:
            raise ValidationException("Nome is required")
        if cnpj is None:
            raise ValidationException("CNPJ is required")

        self.nome = nome
        self.cnpj = cnpj
        self.plano = plano
        self.limite_cameras = limite_cameras or LimiteCameras(1000)
        self.usuarios = usuarios or []
        self.cameras = cameras or []

    @staticmethod
    def create(nome: str, cnpj: CNPJ, plano: Plano) -> "Cidade":
        """Factory method to create cidade."""
        cidade = Cidade(nome=nome, cnpj=cnpj, plano=plano)
        cidade.add_domain_event(CidadeCriada(cidade.id, nome, cnpj.value))
        return cidade

    def atribuir_plano(self, plano: Plano) -> None:
        """Atribuir plano à cidade."""
        self.plano = plano
        self._touch()
        self.add_domain_event(PlanoAtribuido(self.id, plano.tipo.value))

    def add_usuario(self, usuario: UsuarioCidade) -> None:
        """Add usuario to cidade."""
        if usuario.is_gestor():
            if self._has_gestor():
                raise BusinessRuleViolationException("Cidade já possui um gestor")
        else:
            if self._count_visualizadores() >= self.MAX_VISUALIZADORES:
                raise BusinessRuleViolationException(
                    f"Cidade já possui {self.MAX_VISUALIZADORES} visualizadores"
                )

        self.usuarios.append(usuario)
        self._touch()

    def remove_usuario(self, usuario: UsuarioCidade) -> None:
        """Remove usuario from cidade."""
        if usuario in self.usuarios:
            self.usuarios.remove(usuario)
            self._touch()

    def _has_gestor(self) -> bool:
        """Check if cidade has gestor."""
        return any(u.is_gestor() for u in self.usuarios)

    def _count_visualizadores(self) -> int:
        """Count visualizadores."""
        return sum(1 for u in self.usuarios if u.is_visualizador())

    def get_gestor(self) -> Optional[UsuarioCidade]:
        """Get gestor."""
        for usuario in self.usuarios:
            if usuario.is_gestor():
                return usuario
        return None

    def add_camera(self, camera: Camera) -> None:
        """Add camera to cidade."""
        if len(self.cameras) >= self.limite_cameras.value:
            raise BusinessRuleViolationException(
                f"Cidade já possui {self.limite_cameras.value} câmeras (limite máximo)"
            )
        self.cameras.append(camera)
        self._touch()

    def remove_camera(self, camera: Camera) -> None:
        """Remove camera from cidade."""
        if camera in self.cameras:
            self.cameras.remove(camera)
            self._touch()

    def count_cameras(self) -> int:
        """Count cameras."""
        return len(self.cameras)

    def __repr__(self) -> str:
        """String representation."""
        return f"Cidade(id={self.id}, nome={self.nome}, cnpj={self.cnpj})"
