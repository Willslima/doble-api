from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    SETOR_CHOICES = (
        ('NOC', 'NOC'),
        ('TECNICO', 'Técnico'),
    )
    
    setor = models.CharField(max_length=10, choices=SETOR_CHOICES, default='NOC')
    foto_perfil = models.ImageField(upload_to='perfil_fotos/', null=True, blank=True)