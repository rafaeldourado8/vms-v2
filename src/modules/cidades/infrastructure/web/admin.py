"""Django Admin for Cidades."""
from django.contrib import admin

from src.cidades.infrastructure.persistence.models import (
    CidadeModel,
    PlanoModel,
    UsuarioCidadeModel,
    CameraModel,
)


@admin.register(PlanoModel)
class PlanoAdmin(admin.ModelAdmin):
    """Plano admin."""

    list_display = ["tipo", "nome", "created_at"]
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

    fieldsets = (
        (None, {"fields": ("nome", "cnpj")}),
        ("Plano", {"fields": ("plano", "limite_cameras")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(UsuarioCidadeModel)
class UsuarioCidadeAdmin(admin.ModelAdmin):
    """Usuario Cidade admin."""

    list_display = ["cidade", "user_id", "tipo", "created_at"]
    list_filter = ["tipo", "created_at"]
    search_fields = ["cidade__nome"]
    readonly_fields = ["id", "created_at", "updated_at"]


@admin.register(CameraModel)
class CameraAdmin(admin.ModelAdmin):
    """Camera admin."""

    list_display = ["nome", "cidade", "status", "localizacao", "created_at"]
    list_filter = ["status", "cidade", "created_at"]
    search_fields = ["nome", "localizacao", "cidade__nome"]
    readonly_fields = ["id", "created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("nome", "localizacao", "cidade")}),
        ("Conexão", {"fields": ("url", "status")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
