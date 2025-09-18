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
from gestao import views

urlpatterns = [

    path("", RedirectView.as_view(url="/login/", permanent=False)),

    # Autenticação
    path("login/", auth_views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.CustomLogoutView.as_view(), name="logout"),

    # Requerente
    path("chamados/", chamado_views.ChamadoListView.as_view(), name="chamado_list"), # exibe a lista de chamados do requerente
    path("chamados/novo/", chamado_views.ChamadoCreateView.as_view(), name="chamado_create"), # formulario de criacao de chamado
    path("chamados/<int:pk>/", chamado_views.ChamadoDetailView.as_view(), name="chamado_detail"), # detalhe dos chamados
    path("chamados/<int:pk>/editar/", chamado_views.ChamadoUpdateView.as_view(), name="chamado_edit"), # edicao dos chamados
    path("chamados/<int:pk>/excluir/", chamado_views.ChamadoDelete, name="chamado_delete"), # excluir um chamado caso aberto
    path("chamados/<int:pk>/anexo/", chamado_views.AnexoCreateView.as_view(), name="chamado_anexo"), # anexos do chamado

    # Admin
    path("admin/dashboard/", admin_views.AdminDashboardView.as_view(), name="admin_dashboard"), # admin dashboard - lista de chamados
    path("admin/chamados/<int:pk>/", admin_views.AdminChamadoDetail.as_view(), name="admin_chamados"),  # detalhe dos chamados
    path("admin/chamados/<int:pk>/editar/", admin_views.AdminChamadoUpdate.as_view(), name="admin_chamado_edit"), # editar os chamados
    path("admin/chamados/<int:pk>/excluir/", admin_views.AdminChamadoDelete, name="admin_chamado_delete"), # deletar um chamado
    path("admin/chamados/<int:pk>/retornar/", admin_views.RetornarChamadoFila, name="admin_chamado_retornar"),
    path("admin/usuarios/", admin_views.UserListView.as_view(), name="user_list"), # lista de usuários
    path("admin/usuarios/<int:pk>/editar/", admin_views.UserUpdateView.as_view(), name="user_edit"), # editar usuário
    path("admin/usuarios/<int:pk>/desativar/", admin_views.UserDesativarView, name="user_desativar"), # desativa um usuário

    # Responsável
    path("responsavel/dashboard/", responsavel_views.ResponsavelDashboardView.as_view(), name="responsavel_dashboard"), # dashboard responsavel
    path("responsavel/chamados/fila/", responsavel_views.FilaEChamadosAceitosView.as_view(), name="chamado_fila"), # fila de chamados abertos
    path("responsavel/chamados/<int:pk>/show/", responsavel_views.DetalheChamadoView.as_view(), name="responsavel_chamado_detail"), # detalhe dos chamados
    path("responsavel/chamados/<int:pk>/aceitar/", responsavel_views.AceitarChamadoView, name="chamado_aceitar"), # aceitar chamados
    path("responsavel/chamados/<int:pk>/retornar/", responsavel_views.RetornarChamadoFila, name="chamado_retornar"), # retornar chamado pra fila
    path("responsavel/chamados/<int:pk>/concluir/", responsavel_views.ConcluirChamadoView.as_view(), name="chamado_concluir"), # conclusão do chamado
    path("responsavel/chamados/<int:pk>/anexo/", responsavel_views.ResponsavelAnexoCreateView.as_view(), name="responsavel_anexo"), # anexos da conclusão do chamado

]