"""API views for Cidades."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.modules.cidades.application.dtos.add_usuario_cidade_dto import AddUsuarioCidadeDTO
from src.modules.cidades.application.dtos.create_cidade_dto import CreateCidadeDTO
from src.modules.cidades.application.dtos.create_camera_dto import CreateCameraDTO
from src.modules.cidades.application.use_cases.add_usuario_cidade import AddUsuarioCidadeUseCase
from src.modules.cidades.application.use_cases.create_cidade import CreateCidadeUseCase
from src.modules.cidades.application.use_cases.create_camera import CreateCameraUseCase
from src.modules.cidades.infrastructure.persistence.cidade_repository_impl import CidadeRepository
from src.modules.cidades.infrastructure.persistence.camera_repository_impl import CameraRepositoryImpl
from src.modules.cidades.infrastructure.web.serializers import (
    AddUsuarioCidadeSerializer,
    CidadeResponseSerializer,
    CreateCidadeSerializer,
    CreateCameraSerializer,
    CameraResponseSerializer,
)
from src.shared.application.event_bus import EventBus


@api_view(["POST"])
@permission_classes([IsAuthenticated])
async def create_cidade(request):
    """Create cidade endpoint."""
    serializer = CreateCidadeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        cidade_repository = CidadeRepository()
        event_bus = EventBus()
        use_case = CreateCidadeUseCase(cidade_repository, event_bus)

        input_dto = CreateCidadeDTO(**serializer.validated_data)
        result = await use_case.execute(input_dto)

        response_serializer = CidadeResponseSerializer(result.model_dump())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
async def list_cidades(request):
    """List cidades endpoint."""
    try:
        cidade_repository = CidadeRepository()
        cidades = await cidade_repository.find_all()

        results = []
        for cidade in cidades:
            results.append(
                {
                    "id": str(cidade.id),
                    "nome": cidade.nome,
                    "cnpj": cidade.cnpj.value,
                    "tipo_plano": cidade.plano.tipo.value if cidade.plano else "",
                    "dias_retencao": cidade.plano.dias_retencao if cidade.plano else 0,
                    "limite_cameras": cidade.limite_cameras.value,
                }
            )

        return Response(results, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
async def add_usuario_cidade(request, cidade_id):
    """Add usuario to cidade endpoint."""
    serializer = AddUsuarioCidadeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        cidade_repository = CidadeRepository()
        use_case = AddUsuarioCidadeUseCase(cidade_repository)

        input_dto = AddUsuarioCidadeDTO(
            cidade_id=cidade_id, **serializer.validated_data
        )
        result = await use_case.execute(input_dto)

        response_serializer = CidadeResponseSerializer(result.model_dump())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
async def create_camera(request, cidade_id):
    """Create camera endpoint."""
    serializer = CreateCameraSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        cidade_repository = CidadeRepository()
        camera_repository = CameraRepositoryImpl()
        use_case = CreateCameraUseCase(cidade_repository, camera_repository)

        input_dto = CreateCameraDTO(cidade_id=cidade_id, **serializer.validated_data)
        result = await use_case.execute(input_dto)

        response_serializer = CameraResponseSerializer(result.model_dump())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
async def list_cameras(request, cidade_id):
    """List cameras by cidade endpoint."""
    try:
        camera_repository = CameraRepositoryImpl()
        cameras = await camera_repository.find_by_cidade(cidade_id)

        results = [
            {
                "id": str(camera.id),
                "nome": camera.nome,
                "localizacao": camera.localizacao,
                "url": camera.url.value,
                "status": camera.status.value,
                "cidade_id": str(camera.cidade_id),
            }
            for camera in cameras
        ]

        return Response(results, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
async def delete_camera(request, cidade_id, camera_id):
    """Delete camera endpoint."""
    try:
        camera_repository = CameraRepositoryImpl()
        await camera_repository.delete(camera_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
