"""Create Camera Use Case."""
from src.modules.cidades.application.dtos.camera_response_dto import CameraResponseDTO
from src.modules.cidades.application.dtos.create_camera_dto import CreateCameraDTO
from src.modules.cidades.domain.entities.camera import Camera
from src.modules.cidades.domain.repositories.cidade_repository import ICidadeRepository
from src.modules.cidades.domain.value_objects.status_camera import StatusCamera
from src.modules.cidades.domain.value_objects.url_camera import URLCamera
from src.shared.application.use_case import UseCase
from src.shared.domain.domain_exception import EntityNotFoundException


class CreateCameraUseCase(UseCase[CreateCameraDTO, CameraResponseDTO]):
    """Use case for creating camera."""

    def __init__(self, cidade_repository: ICidadeRepository) -> None:
        """Initialize use case."""
        self.cidade_repository = cidade_repository

    async def execute(self, input_dto: CreateCameraDTO) -> CameraResponseDTO:
        """Execute use case."""
        cidade = await self.cidade_repository.find_by_id(input_dto.cidade_id)
        if cidade is None:
            raise EntityNotFoundException(f"Cidade not found: {input_dto.cidade_id}")

        url = URLCamera(input_dto.url)
        camera = Camera(
            nome=input_dto.nome,
            localizacao=input_dto.localizacao,
            url=url,
            status=StatusCamera.INATIVA,
            cidade_id=input_dto.cidade_id,
        )

        cidade.add_camera(camera)
        await self.cidade_repository.save(cidade)

        return CameraResponseDTO(
            id=camera.id,
            nome=camera.nome,
            localizacao=camera.localizacao,
            url=camera.url.value,
            status=camera.status.value,
            cidade_id=camera.cidade_id,
        )
