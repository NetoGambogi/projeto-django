from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import modelformset_factory
from gestao.fields import MultipleFileField, MultipleFileInput
from .models import CustomUser, Chamado, ChamadoAnexo, Tarefa

        
    # criar usuarios - admin 

class CreateCustomUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "role")
        labels = {
            "role": "Função do usuário",
        }

class UserForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ["username", "email", "role", "is_active"]

    # chamados = requerente

class ChamadoForm(forms.ModelForm):
    anexos = MultipleFileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False,
        max_upload_size=5 * 1024 * 1024,
        allowed_types=["pdf", "jpg", "png", "jpeg"],
        label="Arquivos"
    )
    
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
    anexos = MultipleFileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False,
        max_upload_size=5 * 1024 * 1024,
        allowed_types=["pdf", "jpg", "png", "jpeg"],
        label="Arquivos"
    )
    
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
        
    arquivo = forms.FileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False
    )
    
    
class KanbanCreateForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao"]

class KanbanUpdateForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ["titulo", "descricao", "responsavel"]