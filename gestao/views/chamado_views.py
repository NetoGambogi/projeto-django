from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Chamado, ChamadoAnexo
from ..forms import ChamadoForm, ChamadoAnexoForm

class ChamadoListView(LoginRequiredMixin, ListView):
    model = Chamado
    template_name = "chamados/chamado_list.html"

    def get_queryset(self):
        return Chamado.objects.filter(requerente=self.request.user)
    
class ChamadoCreateView(LoginRequiredMixin, CreateView):
    model = Chamado
    form_class = ChamadoForm
    template_name = "chamados/chamado_form.html"
    success_url = reverse_lazy("chamado_list")

    def form_valid(self, form):
        form.instance.requerente = self.request.user
        return super().form_valid(form)
    
class ChamadoDetailView(LoginRequiredMixin, DetailView):
    model = Chamado
    template_name = "chamados/chamado_detail.html"

class ChamadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Chamado
    form_class = ChamadoForm
    template_name = "chamados/chamado_form.html"
    success_url = reverse_lazy("chamado_list")
    
    def get_queryset(self):
        return Chamado.objects.filter(requerente=self.request.user, status="aberto")
    
class ChamadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Chamado
    template_name = "chamados/chamado_confirm_delete.html"
    success_url = reverse_lazy("chamado_list")

    def get_queryset(self):
        return Chamado.objects.filter(requerente=self.request.user, status="aberto")
    
class AnexoCreateView(LoginRequiredMixin, CreateView):
    model = ChamadoAnexo
    form_class = ChamadoAnexoForm
    template_name = "chamados/anexo_form.html"

    def form_valid(self, form):
        chamado = Chamado.objects.get(pk=self.kwargs["pk"])
        form.instance.chamado = chamado
        form.instance.enviado_por = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("chamado_detail", kwargs={"pk": self.kwargs["pk"]})
