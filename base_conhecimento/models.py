from django.conf import settings
from django.db import models
from django.db.models.functions import Lower


# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("nome"),
                name="unique_categoria_nome_lower"
            )
        ]
    
    def save(self, *args, **kwargs):
        if self.nome:
            self.nome = self.nome.strip().lower().capitalize()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.nome
    
class BaseConhecimento(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    titulo = models.CharField(max_length=255)
    solucao = models.TextField()
    anexo = models.FileField(upload_to='base_conhecimento/', blank=True, null=True)
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo if self.titulo else f"Registro {self.id}"