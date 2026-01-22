"""Django app configuration for Cidades persistence."""
from django.apps import AppConfig


class CidadesPersistenceConfig(AppConfig):
    """Cidades persistence app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.cidades.infrastructure.persistence"
    label = "cidades_persistence"
