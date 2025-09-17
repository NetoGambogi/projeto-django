"""
URL configuration for gestao project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import RedirectView
from .views import auth_views, chamado_views, admin_views, responsavel_views
from .views.chamado_views import ChamadoListView, ChamadoCreateView

urlpatterns = [

    path("", RedirectView.as_view(url="/login/", permanent=False)),

    # Autenticação
    path("login/", auth_views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.CustomLogoutView.as_view(), name="logout"),

    # Requerente
    path("chamados/", chamado_views.ChamadoListView.as_view(), name="chamado_list"),
    path("chamados/novo/", chamado_views.ChamadoCreateView.as_view(), name="chamado_create"),
    path("chamados/<int:pk>/", chamado_views.ChamadoDetailView.as_view(), name="chamado_detail"),
    path("chamados/<int:pk>/editar/", chamado_views.ChamadoUpdateView.as_view(), name="chamado_edit"),
    path("chamados/<int:pk>/excluir/", chamado_views.ChamadoDeleteView.as_view(), name="chamado_delete"),
    path("chamados/<int:pk>/anexo/", chamado_views.AnexoCreateView.as_view(), name="chamado_anexo"),

    # Admin
    path("admin/dashboard/", admin_views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path("admin/usuarios/", admin_views.UserListView.as_view(), name="user_list"),
    path("admin/usuarios/<int:pk>/editar/", admin_views.UserUpdateView.as_view(), name="user_edit"),
    path("admin/usuarios/<int:pk>/desativar/", admin_views.UserDesativarView, name="user_desativar"),

    # Responsável
    path("responsavel/dashboard/", responsavel_views.ResponsavelDashboardView.as_view(), name="responsavel_dashboard"),
    path("responsavel/chamados/<int:pk>/aceitar/", responsavel_views.AceitarChamadoView, name="chamado_aceitar"),
    path("responsavel/chamados/<int:pk>/concluir/", responsavel_views.ConcluirChamadoView.as_view(), name="chamado_concluir"),
    path("responsavel/chamados/<int:pk>/anexo/", responsavel_views.ResponsavelAnexoCreateView.as_view(), name="responsavel_anexo"),

]