"""API URLs."""
from django.urls import path

from src.admin.infrastructure.web.django_app.views import assign_role, create_user

urlpatterns = [
    path("", create_user, name="create_user"),
    path("<uuid:user_id>/roles/", assign_role, name="assign_role"),
]
