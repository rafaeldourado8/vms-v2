"""ASGI config for GT-Vision VMS."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "admin.infrastructure.web.django_app.settings"
)

application = get_asgi_application()
