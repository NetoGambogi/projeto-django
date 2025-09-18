from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from gestao.mixins import RequerenteRequiredMixin
from ..models import Chamado, ChamadoAnexo
from ..forms import ChamadoForm, ChamadoAnexoForm

class ChamadoListView(RequerenteRequiredMixin, ListView):
    model = Chamado
    template_name = "chamados/chamado_list.html"

    def get_queryset(self):
        return Chamado.objects.filter(requerente=self.request.user)
    
class ChamadoCreateView(RequerenteRequiredMixin, CreateView):
    model = Chamado
    form_class = ChamadoForm
    template_name = "chamados/chamado_form.html"
    success_url = reverse_lazy("chamado_list")

    def form_valid(self, form):
        form.instance.requerente = self.request.user
        return super().form_valid(form)
    
def ChamadoDelete(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    chamado.delete()
    return redirect("chamado_list")
    
class ChamadoDetailView(RequerenteRequiredMixin, DetailView):
    model = Chamado
    template_name = "chamados/chamado_detail.html"

class ChamadoUpdateView(RequerenteRequiredMixin, UpdateView):
    model = Chamado
    form_class = ChamadoForm
    template_name = "chamados/chamado_form.html"
    success_url = reverse_lazy("chamado_list")
    
    def get_queryset(self):
        return Chamado.objects.filter(requerente=self.request.user, status="aberto")

    
class AnexoCreateView(RequerenteRequiredMixin, CreateView):
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
