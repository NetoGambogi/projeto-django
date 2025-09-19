from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from gestao.mixins import RequerenteRequiredMixin
from ..models import Chamado, ChamadoAnexo
from ..forms import ChamadoForm, ChamadoAnexoForm

class ChamadoListView(RequerenteRequiredMixin, ListView):
    model = Chamado
    template_name = "chamados/chamado_list.html"
    context_object_name = "chamados"
    paginate_by = 5 

    def get_queryset(self):
        return Chamado.objects.filter(requerente=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        chamados = Chamado.objects.filter(requerente=user)

        context["total_abertos"] = chamados.count()  
        context["nao_atendidos"] = chamados.filter(status="aberto", responsavel__isnull=True).count()
        context["em_atendimento"] = chamados.filter(status__in=["aberto", "em_andamento"], responsavel__isnull=False).count()
        context["concluidos"] = chamados.filter(status="concluido").count()

        return context
    
class ChamadoCreateView(RequerenteRequiredMixin, CreateView):
    model = Chamado
    form_class = ChamadoForm
    template_name = "chamados/chamado_form.html"
    success_url = reverse_lazy("chamado_list")

    def form_valid(self, form):
        form.instance.requerente = self.request.user

        response = super().form_valid(form)

        arquivos = form.cleaned_data.get("anexos") or []

        for arquivo in arquivos:
            ChamadoAnexo.objects.create(
                chamado=self.object,  
                arquivo=arquivo,
                enviado_por=self.request.user
            )

        return response
    
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
