"""Camera repository implementation."""
from typing import Optional, List
from uuid import UUID

from src.modules.cidades.domain.repositories.camera_repository import CameraRepository
from src.modules.cidades.domain.entities.camera import Camera
from src.modules.cidades.domain.value_objects.url_camera import URLCamera
from src.modules.cidades.domain.value_objects.status_camera import StatusCamera
from .models import CameraModel


class CameraRepositoryImpl(CameraRepository):
    """Camera repository implementation using Django ORM."""

    async def save(self, camera: Camera) -> None:
        """Save camera."""
        await CameraModel.objects.aupdate_or_create(
            id=camera.id,
            defaults={
                "nome": camera.nome,
                "localizacao": camera.localizacao,
                "url": camera.url.value,
                "status": camera.status.value,
                "cidade_id": camera.cidade_id,
            },
        )

    async def find_by_id(self, camera_id: UUID) -> Optional[Camera]:
        """Find camera by ID."""
        try:
            model = await CameraModel.objects.aget(id=camera_id)
            return self._to_entity(model)
        except CameraModel.DoesNotExist:
            return None

    async def find_by_cidade(self, cidade_id: UUID) -> List[Camera]:
        """Find all cameras by cidade."""
        models = [m async for m in CameraModel.objects.filter(cidade_id=cidade_id)]
        return [self._to_entity(m) for m in models]

    async def delete(self, camera_id: UUID) -> None:
        """Delete camera."""
        await CameraModel.objects.filter(id=camera_id).adelete()

    def _to_entity(self, model: CameraModel) -> Camera:
        """Convert model to entity."""
        return Camera(
            id=model.id,
            nome=model.nome,
            localizacao=model.localizacao,
            url=URLCamera(model.url),
            status=StatusCamera(model.status),
            cidade_id=model.cidade_id,
        )
