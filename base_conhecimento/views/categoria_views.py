from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from base_conhecimento.forms import CreateCategoriaForm
from base_conhecimento.models import Categoria

class CategoriaListView(ListView):
    model = Categoria
    template_name = "categoria/categoria_list.html"
    name = "categorias"
    

class CategoriaCreate(CreateView):
    model = Categoria
    form_class = CreateCategoriaForm
    template_name = "categoria/categoria_create.html"
    success_url = reverse_lazy("conhecimentos")
