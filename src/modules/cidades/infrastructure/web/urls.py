"""URLs for Cidades API."""
from django.urls import path

from src.modules.cidades.infrastructure.web.views import (
    add_usuario_cidade,
    create_cidade,
    list_cidades,
    create_camera,
    list_cameras,
    delete_camera,
)

urlpatterns = [
    path("", create_cidade, name="create_cidade"),
    path("list/", list_cidades, name="list_cidades"),
    path("<uuid:cidade_id>/usuarios/", add_usuario_cidade, name="add_usuario_cidade"),
    path("<uuid:cidade_id>/cameras/", create_camera, name="create_camera"),
    path("<uuid:cidade_id>/cameras/list/", list_cameras, name="list_cameras"),
    path("<uuid:cidade_id>/cameras/<uuid:camera_id>/", delete_camera, name="delete_camera"),
]
