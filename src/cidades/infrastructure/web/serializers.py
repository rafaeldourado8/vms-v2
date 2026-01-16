"""API serializers for Cidades."""
from rest_framework import serializers


class CreateCidadeSerializer(serializers.Serializer):
    """Serializer for creating cidade."""

    nome = serializers.CharField(max_length=255)
    cnpj = serializers.CharField(max_length=18)
    tipo_plano = serializers.ChoiceField(choices=["BASICO", "INTERMEDIARIO", "AVANCADO"])


class CidadeResponseSerializer(serializers.Serializer):
    """Serializer for cidade response."""

    id = serializers.UUIDField()
    nome = serializers.CharField()
    cnpj = serializers.CharField()
    tipo_plano = serializers.CharField()
    dias_retencao = serializers.IntegerField()
    limite_cameras = serializers.IntegerField()
    usuarios = serializers.ListField()


class AddUsuarioCidadeSerializer(serializers.Serializer):
    """Serializer for adding usuario to cidade."""

    user_id = serializers.UUIDField()
    tipo = serializers.ChoiceField(choices=["GESTOR", "VISUALIZADOR"])


class CreateCameraSerializer(serializers.Serializer):
    """Serializer for creating camera."""

    nome = serializers.CharField(max_length=200)
    localizacao = serializers.CharField(max_length=500)
    url = serializers.CharField(max_length=500)


class CameraResponseSerializer(serializers.Serializer):
    """Serializer for camera response."""

    id = serializers.UUIDField()
    nome = serializers.CharField()
    localizacao = serializers.CharField()
    url = serializers.CharField()
    status = serializers.CharField()
    cidade_id = serializers.UUIDField()
