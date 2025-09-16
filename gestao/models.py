from django.contrib.auth.models import AbstractUser
from django.db import models
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('requerente', 'Requerente'),
        ('responsavel', 'Responsável'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='requerente')
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em andamento'),
        ('concluido', 'Concluido'),
        ('cancelado', 'Cancelado'),
    ]
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    
    requerente = models.ForeignKey(
        'gestao.CustomUser',
        on_delete=models.CASCADE,
        related_name='chamados_requeridos',
        limit_choices_to={'role': 'requerente'}
        )
    
    responsavel = models.ForeignKey(
        'gestao.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='chamados_responsaveis',
        limit_choices_to={'role': 'responsavel'}
        )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )

    def __str__(self):
        return self.titulo