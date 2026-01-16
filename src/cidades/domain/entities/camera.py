"""Camera entity."""
from uuid import UUID
from src.shared_kernel.domain.entity import Entity
from src.cidades.domain.value_objects.url_camera import URLCamera
from src.cidades.domain.value_objects.status_camera import StatusCamera


class Camera(Entity):
    """Camera entity."""

    def __init__(
        self,
        id: UUID,
        nome: str,
        localizacao: str,
        url: URLCamera,
        status: StatusCamera,
        cidade_id: UUID
    ):
        super().__init__(id)
        self.nome = nome
        self.localizacao = localizacao
        self.url = url
        self.status = status
        self.cidade_id = cidade_id

    def ativar(self):
        """Activate camera."""
        self.status = StatusCamera.ATIVA

    def desativar(self):
        """Deactivate camera."""
        self.status = StatusCamera.INATIVA

    def marcar_erro(self):
        """Mark camera as error."""
        self.status = StatusCamera.ERRO

    def __str__(self):
        return f"Camera({self.nome})"
