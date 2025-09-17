from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import modelformset_factory
from .models import CustomUser, Chamado, ChamadoAnexo

    # usuarios

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "password1", "password2"]

class UserForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "is_active"]

    # chamados = requerente

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ["titulo", "descricao"]
        
    # chamados = admin
    
class AdminChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ["titulo", "descricao", "status", "requerente", "responsavel", "solucao"]    

    #conclusao = responsavel

class SolucaoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ["solucao"]
        widgets = {
            "solucao": forms.Textarea(attrs={"rows": 4})
        }

class ChamadoAnexoForm(forms.ModelForm):
    class Meta:
        model = ChamadoAnexo
        fields = ["arquivo"]
