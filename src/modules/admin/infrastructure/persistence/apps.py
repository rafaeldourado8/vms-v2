"""Django app configuration for Admin persistence."""
from django.apps import AppConfig


class AdminPersistenceConfig(AppConfig):
    """Admin persistence app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.admin.infrastructure.persistence"
    label = "admin_persistence"
