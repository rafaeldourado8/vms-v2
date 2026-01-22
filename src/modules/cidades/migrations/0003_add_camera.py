"""Add Camera model."""
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cidades', '0002_add_usuario_cidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='CameraModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=200)),
                ('localizacao', models.CharField(max_length=500)),
                ('url', models.CharField(max_length=500, validators=[django.core.validators.URLValidator(schemes=['rtsp', 'rtmp'])])),
                ('status', models.CharField(choices=[('ATIVA', 'Ativa'), ('INATIVA', 'Inativa'), ('ERRO', 'Erro')], default='ATIVA', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cameras', to='cidades.cidademodel')),
            ],
            options={
                'db_table': 'cidades_cameras',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='cameramodel',
            index=models.Index(fields=['cidade', 'status'], name='cidades_cam_cidade_idx'),
        ),
        migrations.AddIndex(
            model_name='cameramodel',
            index=models.Index(fields=['status'], name='cidades_cam_status_idx'),
        ),
    ]
