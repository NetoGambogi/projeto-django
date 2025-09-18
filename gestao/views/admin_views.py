from django.contrib import messages
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from gestao.mixins import AdminRequiredMixin
from ..models import CustomUser, Chamado
from ..forms import AdminChamadoForm, UserForm

class AdminDashboardView(AdminRequiredMixin, ListView):
    model = Chamado
    template_name = "admin/dashboard.html"
    context_object_name = "chamados"

class UserListView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = "admin/user_list.html"
    context_object_name = "usuarios"

    def get_queryset(self):
        qs = CustomUser.objects.all()
        role = self.request.GET.get("role")
        nome = self.request.GET.get("nome")
        if role:
            qs = qs.filter(role=role)
        if nome:
            qs = qs.filter(username_icontains=nome)
        return qs
    
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