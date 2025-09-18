from django import forms
from django.core.exceptions import ValidationError
import os

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size", 5 * 1024 * 1024)
        self.allowed_types = kwargs.pop("allowed_types", None)
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return []

        if not isinstance(data, (list, tuple)):
            data = [data]

        arquivos_validados = []

        for f in data:
            arquivo = super().clean(f, initial)

            if arquivo.size > self.max_upload_size:
                raise ValidationError(
                    f"O arquivo '{arquivo.name}' excede o limite de {self.max_upload_size/1024/1024:.1f} MB."
                )

            if self.allowed_types:
                ext = os.path.splitext(arquivo.name)[1].lower().lstrip(".")
                if ext not in self.allowed_types:
                    raise ValidationError(
                        f"Extensão inválida para '{arquivo.name}'. Permitidos: {', '.join(self.allowed_types)}"
                    )

            arquivos_validados.append(arquivo)

        return arquivos_validados
