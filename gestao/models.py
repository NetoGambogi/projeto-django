from django.conf import settings
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

    # Helpers
    def is_admin(self):
        return self.role == 'admin'

    def is_requerente(self):
        return self.role == 'requerente'

    def is_responsavel(self):
        return self.role == 'responsavel'


class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
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
        blank=True,
        related_name='chamados_responsaveis',
        limit_choices_to={'role': 'responsavel'}
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberto'
    )

    solucao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.get_status_display()}] {self.titulo}"

    @property
    def pode_editar_requerente(self):
        return self.status == 'aberto'

    @property
    def pode_excluir_requerente(self):
        return self.status == 'aberto'


def chamado_upload_path(instance, filename):
    return f"chamados/{instance.chamado.id}/{filename}"

class ChamadoAnexo(models.Model):
    chamado = models.ForeignKey(
        "gestao.Chamado",
        on_delete=models.CASCADE,
        related_name="anexos"
    )
    arquivo = models.FileField(upload_to=chamado_upload_path)
    enviado_por = models.ForeignKey(
        "gestao.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anexo {self.arquivo.name} (Chamado {self.chamado.id})"
    
class Tarefa(models.Model):
    STATUS_CHOICES = [
        ('todo', 'A fazer'),
        ('doing', 'Em progresso'),
        ('done', 'Concluído'),
    ]
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="Tarefas_criadas"
    )
    
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tarefas_assumidas"
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="todo")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.get_status_display()}"