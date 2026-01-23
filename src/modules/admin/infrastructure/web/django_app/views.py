"""API views."""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from src.modules.admin.application.dtos.assign_role_dto import AssignRoleDTO
from src.modules.admin.application.dtos.create_user_dto import CreateUserDTO
from src.modules.admin.application.use_cases.assign_role import AssignRoleUseCase
from src.modules.admin.application.use_cases.create_user import CreateUserUseCase
from src.modules.admin.infrastructure.persistence.role_repository_impl import RoleRepository
from src.modules.admin.infrastructure.persistence.user_repository_impl import UserRepository
from src.modules.admin.infrastructure.web.django_app.serializers import (
    AssignRoleSerializer,
    CreateUserSerializer,
    UserResponseSerializer,
)
from src.shared.application.event_bus import EventBus


@api_view(["POST"])
@permission_classes([AllowAny])
async def create_user(request):
    """Create user endpoint."""
    serializer = CreateUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_repository = UserRepository()
        event_bus = EventBus()
        use_case = CreateUserUseCase(user_repository, event_bus)

        input_dto = CreateUserDTO(**serializer.validated_data)
        result = await use_case.execute(input_dto)

        response_serializer = UserResponseSerializer(result.model_dump())
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
async def assign_role(request, user_id):
    """Assign role to user endpoint."""
    serializer = AssignRoleSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_repository = UserRepository()
        role_repository = RoleRepository()
        use_case = AssignRoleUseCase(user_repository, role_repository)

        input_dto = AssignRoleDTO(
            user_id=user_id, role_code=serializer.validated_data["role_code"]
        )
        result = await use_case.execute(input_dto)

        response_serializer = UserResponseSerializer(result.model_dump())
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
