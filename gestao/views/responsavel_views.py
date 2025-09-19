from multiprocessing import context
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from gestao.mixins import ResponsavelRequiredMixin
from ..models import Chamado, ChamadoAnexo
from ..forms import SolucaoForm, ChamadoAnexoForm

class ResponsavelDashboardView(ResponsavelRequiredMixin, ListView):
    model = Chamado
    template_name = "responsavel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        chamados = Chamado.objects.filter(responsavel=user)
        context["total"] = chamados.count()
        context["abertos"] = Chamado.objects.filter(status="aberto", responsavel__isnull=True).count() 
        context["em_andamento"] = chamados.filter(status="em_andamento").count()
        context["concluidos"] = chamados.filter(status="concluido").count()

        context["em_atendimento"] = (
            chamados.filter(status__in=["aberto", "em_andamento"])
            .order_by("-created_at")
        )

        context["historico"] = (
            chamados.filter(status__in=["concluido", "cancelado"])
            .order_by("-updated_at")[:5]
        )

        return context
    
def AceitarChamadoView(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == "aberto":
        chamado.status = "em_andamento"
        chamado.responsavel = request.user
        chamado.save()
    return redirect("chamado_fila")

class FilaEChamadosAceitosView(ResponsavelRequiredMixin, TemplateView):
    template_name = "responsavel/chamado_fila.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['chamados_abertos'] = Chamado.objects.filter(status='aberto')
        context ['chamados_aceitos'] = Chamado.objects.filter(
            status = 'em_andamento',
            responsavel=self.request.user
        )
        return context
    
class DetalheChamadoView(ResponsavelRequiredMixin, DetailView):
    model = Chamado
    template_name = "responsavel/chamado_detail.html"
    context_object_name = 'chamado'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.status != "concluido":
            context['form'] = SolucaoForm(instance=self.object)
        return context
    
def RetornarChamadoFila(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if chamado.status == "em_andamento":
        chamado.status = "aberto"
        chamado.responsavel = None
        chamado.save()
    return redirect("chamado_fila")
    
class ConcluirChamadoView(ResponsavelRequiredMixin, UpdateView):
    model = Chamado
    form_class = SolucaoForm
    template_name = "responsavel/chamado_detail.html"
    success_url = reverse_lazy("responsavel_dashboard")

    def form_valid(self, form):
        form.instance.status = "concluido"
        form.instance.responsavel = self.request.user
        response = super().form_valid(form)
    
        arquivos = form.cleaned_data.get("anexos") or []

        for arquivo in arquivos:

            ChamadoAnexo.objects.create(
                chamado=self.object,  
                arquivo=arquivo,
                enviado_por=self.request.user
            )

        return response
    
class ResponsavelAnexoCreateView(ResponsavelRequiredMixin, CreateView):
    model = ChamadoAnexo
    form_class = ChamadoAnexoForm
    template_name = "responsavel/anexo_form.html"

    def form_valid(self, form):
        chamado = Chamado.objects.get(pk=self.kwargs["pk"])
        form.instance.chamado = chamado
        form.instance.enviado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("responsavel_dashboard")