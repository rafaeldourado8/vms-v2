"""Django models for Cidades context."""
import uuid

from django.db import models
from django.core.validators import URLValidator


class PlanoModel(models.Model):
    """Plano model."""

    TIPO_CHOICES = [
        ("BASICO", "Básico - 7 dias"),
        ("INTERMEDIARIO", "Intermediário - 15 dias"),
        ("AVANCADO", "Avançado - 30 dias"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cidades_planos"
        ordering = ["tipo"]

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class CidadeModel(models.Model):
    """Cidade model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255, unique=True)
    cnpj = models.CharField(max_length=14, unique=True)
    plano = models.ForeignKey(PlanoModel, on_delete=models.PROTECT, related_name="cidades")
    limite_cameras = models.IntegerField(default=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cidades_cidades"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class UsuarioCidadeModel(models.Model):
    """Usuario Cidade model."""

    TIPO_CHOICES = [
        ("GESTOR", "Gestor"),
        ("VISUALIZADOR", "Visualizador"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cidade = models.ForeignKey(CidadeModel, on_delete=models.CASCADE, related_name="usuarios")
    user_id = models.UUIDField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cidades_usuarios_cidade"
        unique_together = ["cidade", "user_id"]
        ordering = ["tipo", "created_at"]

    def __str__(self):
        return f"{self.cidade.nome} - {self.tipo}"


class CameraModel(models.Model):
    """Camera model."""

    STATUS_CHOICES = [
        ("ATIVA", "Ativa"),
        ("INATIVA", "Inativa"),
        ("ERRO", "Erro"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    localizacao = models.CharField(max_length=500)
    url = models.CharField(max_length=500, validators=[URLValidator(schemes=['rtsp', 'rtmp'])])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ATIVA")
    cidade = models.ForeignKey(CidadeModel, on_delete=models.CASCADE, related_name="cameras")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cidades_cameras"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["cidade", "status"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.nome} - {self.cidade.nome}"
