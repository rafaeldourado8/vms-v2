"""Command to seed initial permissions."""
from django.core.management.base import BaseCommand

from src.admin.infrastructure.persistence.models import PermissionModel


class Command(BaseCommand):
    """Seed permissions command."""

    help = "Seed initial permissions"

    def handle(self, *args, **options):
        """Execute command."""
        permissions = [
            {"code": "users.create", "name": "Criar Usuários", "description": "Permite criar novos usuários"},
            {"code": "users.read", "name": "Visualizar Usuários", "description": "Permite visualizar usuários"},
            {"code": "users.update", "name": "Editar Usuários", "description": "Permite editar usuários"},
            {"code": "users.delete", "name": "Deletar Usuários", "description": "Permite deletar usuários"},
            {"code": "roles.create", "name": "Criar Roles", "description": "Permite criar roles"},
            {"code": "roles.read", "name": "Visualizar Roles", "description": "Permite visualizar roles"},
            {"code": "roles.update", "name": "Editar Roles", "description": "Permite editar roles"},
            {"code": "roles.delete", "name": "Deletar Roles", "description": "Permite deletar roles"},
            {"code": "cidades.create", "name": "Criar Cidades", "description": "Permite criar cidades"},
            {"code": "cidades.read", "name": "Visualizar Cidades", "description": "Permite visualizar cidades"},
            {"code": "cidades.update", "name": "Editar Cidades", "description": "Permite editar cidades"},
            {"code": "cidades.delete", "name": "Deletar Cidades", "description": "Permite deletar cidades"},
            {"code": "cameras.create", "name": "Criar Câmeras", "description": "Permite criar câmeras"},
            {"code": "cameras.read", "name": "Visualizar Câmeras", "description": "Permite visualizar câmeras"},
            {"code": "cameras.update", "name": "Editar Câmeras", "description": "Permite editar câmeras"},
            {"code": "cameras.delete", "name": "Deletar Câmeras", "description": "Permite deletar câmeras"},
            {"code": "streaming.view", "name": "Visualizar Streaming", "description": "Permite visualizar streaming"},
            {"code": "streaming.control", "name": "Controlar Streaming", "description": "Permite controlar streaming"},
        ]

        created = 0
        for perm_data in permissions:
            _, created_flag = PermissionModel.objects.get_or_create(
                code=perm_data["code"],
                defaults={"name": perm_data["name"], "description": perm_data["description"]},
            )
            if created_flag:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✓ {created} permissões criadas"))
        self.stdout.write(self.style.SUCCESS(f"✓ Total: {PermissionModel.objects.count()} permissões"))
