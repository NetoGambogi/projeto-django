from django import forms
from django.forms import modelformset_factory
from .models import BaseConhecimento, Categoria

class CreateConhecimentoForm(forms.ModelForm):
    class Meta:
        model = BaseConhecimento
        fields = ["categoria", "titulo", "solucao", "anexo"]
        
class UpdateConhecimentoForm(forms.ModelForm):
    class Meta:
        model = BaseConhecimento
        fields = ["categoria", "titulo", "solucao", "anexo"]
        
class CreateCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]