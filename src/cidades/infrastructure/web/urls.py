"""URLs for Cidades API."""
from django.urls import path

from src.cidades.infrastructure.web.views import (
    add_usuario_cidade,
    create_cidade,
    list_cidades,
    create_camera,
    list_cameras,
    delete_camera,
    list_all_cameras,
    get_clips,
    get_mosaics,
)

urlpatterns = [
    path("cidades/", create_cidade, name="create_cidade"),
    path("cidades/list/", list_cidades, name="list_cidades"),
    path("cidades/<uuid:cidade_id>/usuarios/", add_usuario_cidade, name="add_usuario_cidade"),
    path("cidades/<uuid:cidade_id>/cameras/", create_camera, name="create_camera"),
    path("cidades/<uuid:cidade_id>/cameras/list/", list_cameras, name="list_cameras"),
    path("cidades/<uuid:cidade_id>/cameras/<uuid:camera_id>/", delete_camera, name="delete_camera"),
    path("cameras/", list_all_cameras, name="list_all_cameras"),
    path("clips", get_clips, name="get_clips"),
    path("mosaics", get_mosaics, name="get_mosaics"),
]
