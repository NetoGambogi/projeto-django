from django.urls import path

from base_conhecimento.views import categoria_views

from .views import conhecimento_views


urlpatterns = [  #  Base de conhecimento
    path("suporte/", conhecimento_views.ConhecimentoView.as_view(), name="conhecimentos"),
    path("suporte/<int:pk>/detail", conhecimento_views.ConhecimentoDetailView.as_view(), name="conhecimento_detail"),
    path("suporte/<int:pk>/update", conhecimento_views.ConhecimentoUpdateView.as_view(), name="conhecimento_update"),
    path("suporte/create", conhecimento_views.ConhecimentoCreateView.as_view(), name="conhecimento_create"),
    path("suporte/<int:pk>/delete/", conhecimento_views.ConhecimentoDelete, name="conhecimento_delete"),
    
    # Categoria
    
    path("categoria/", categoria_views.CategoriaListView.as_view(), name="categorias"),
    path("categoria/create", categoria_views.CategoriaCreate.as_view(), name="create_categoria")
]