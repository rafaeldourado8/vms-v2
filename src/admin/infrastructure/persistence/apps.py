"""Django app configuration for Admin persistence."""
from django.apps import AppConfig


class AdminPersistenceConfig(AppConfig):
    """Admin persistence app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.admin.infrastructure.persistence"
    label = "admin_persistence"

    def ready(self):
        """Import admin when app is ready."""
        import src.admin.infrastructure.web.django_app.admin  # noqa
