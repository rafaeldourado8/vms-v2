"""Django Admin configuration for Cidades."""
from django.contrib import admin

from src.cidades.infrastructure.persistence.models import (
    CameraModel,
    CidadeModel,
    PlanoModel,
    UsuarioCidadeModel,
)


@admin.register(PlanoModel)
class PlanoAdmin(admin.ModelAdmin):
    """Plano admin."""

    list_display = ["nome", "tipo", "created_at"]
    list_filter = ["tipo"]
    search_fields = ["nome"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(CidadeModel)
class CidadeAdmin(admin.ModelAdmin):
    """Cidade admin."""

    list_display = ["nome", "cnpj", "plano", "limite_cameras", "created_at"]
    list_filter = ["plano", "created_at"]
    search_fields = ["nome", "cnpj"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(UsuarioCidadeModel)
class UsuarioCidadeAdmin(admin.ModelAdmin):
    """Usuario Cidade admin."""

    list_display = ["get_user_email", "cidade", "tipo", "created_at"]
    list_filter = ["tipo", "cidade"]
    search_fields = ["cidade__nome"]
    readonly_fields = ["id", "created_at", "updated_at", "get_user_info"]
    autocomplete_fields = ["cidade"]
    
    fieldsets = (
        (None, {"fields": ("cidade", "tipo")}),
        ("Usuário", {"fields": ("get_user_info", "user_id"), "description": "Cole o UUID do usuário (visível na lista de Users)"}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    
    def get_user_email(self, obj):
        """Get user email from user_id."""
        from src.admin.infrastructure.persistence.models import UserModel
        try:
            user = UserModel.objects.get(id=obj.user_id)
            return user.email
        except UserModel.DoesNotExist:
            return f"UUID: {obj.user_id}"
    get_user_email.short_description = "Usuário"
    
    def get_user_info(self, obj):
        """Get user info."""
        if not obj.user_id:
            return "-"
        from src.admin.infrastructure.persistence.models import UserModel
        try:
            user = UserModel.objects.get(id=obj.user_id)
            return f"{user.email} ({user.name})"
        except UserModel.DoesNotExist:
            return f"Usuário não encontrado: {obj.user_id}"
    get_user_info.short_description = "Informações do Usuário"


@admin.register(CameraModel)
class CameraAdmin(admin.ModelAdmin):
    """Camera admin."""

    list_display = ["nome", "cidade", "localizacao", "status", "created_at"]
    list_filter = ["status", "cidade", "created_at"]
    search_fields = ["nome", "localizacao", "cidade__nome"]
    readonly_fields = ["id", "created_at", "updated_at"]
