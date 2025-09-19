from django.contrib import messages
from django.views.generic import ListView, UpdateView, DetailView
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django_filters.views import FilterView
from gestao.filters import ChamadoFilter, UserFilter
from gestao.mixins import AdminRequiredMixin
from ..models import CustomUser, Chamado
from ..forms import AdminChamadoForm, UserForm

User = get_user_model()

class AdminDashboardView(AdminRequiredMixin, ListView):
    model = Chamado
    template_name = "admin/dashboard.html"
    context_object_name = "chamados"
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ChamadoFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
    
        chamados = Chamado.objects.all()
        context["total"] = chamados.count()
        context["abertos"] = Chamado.objects.filter(status="aberto", responsavel__isnull=True).count() 
        context["em_andamento"] = chamados.filter(status="em_andamento").count()
        context["concluidos"] = chamados.filter(status="concluido").count()
        
        return context

class UserListView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "admin/user_list.html"
    context_object_name = "usuarios"
    paginate_by = 8
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = UserFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        
        usuarios = CustomUser.objects.all()
        context["total_users"] = usuarios.count()
        context["total_requerentes"] = usuarios.filter(role="requerente").count()
        context["total_responsaveis"] = usuarios.filter(role="responsavel").count()
        context["total_ativos"] = usuarios.filter(is_active=True).count()
        
        return context
    
class AdminChamadoUpdate(AdminRequiredMixin, UpdateView):
    model = Chamado
    form_class = AdminChamadoForm
    template_name = "admin/chamado_edit.html"
    success_url = reverse_lazy("admin_dashboard")
    
class AdminChamadoDetail(AdminRequiredMixin, DetailView):
    model = Chamado
    template_name = "admin/chamado_detail.html"
    
def AdminChamadoDelete(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    chamado.delete()
    return redirect("admin_dashboard")
    
class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    template_name = "admin/user_form.html"
    success_url = reverse_lazy("user_list")

def UserDesativarView(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user == request.user:
        messages.error(request, "Você não pode desativar sua própria conta.")
        return redirect("user_list")

    if not user.is_active:
        messages.warning(request, f"Usuário {user.username} já está desativado.")
    else:
        user.is_active = False
        user.save()
        messages.success(request, f"Usuário {user.username} desativado com sucesso!")

    return redirect("user_list")

def RetornarChamadoFila(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == "em_andamento":
        chamado.status = "aberto"
        chamado.responsavel = None
        chamado.save()
    return redirect("admin_dashboard")


## Filtros

    
    