from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from base_conhecimento.forms import CreateConhecimentoForm, UpdateConhecimentoForm
from base_conhecimento.models import BaseConhecimento

class ConhecimentoView(ListView):
    model = BaseConhecimento
    template_name = "conhecimento/conhecimento_list.html"
    context_object_name = "conhecimentos"
    
    
class ConhecimentoDetailView(DetailView):
    model = BaseConhecimento
    template_name = "conhecimento/conhecimento_detail.html"
    context_object_name = "conhecimento"

class ConhecimentoCreateView(CreateView):
    model = BaseConhecimento
    form_class = CreateConhecimentoForm
    template_name = "conhecimento/conhecimento_form.html"
    success_url = reverse_lazy('conhecimentos')
    
    def form_valid(self, form):
        form.instance.responsavel = self.request.user
        return super().form_valid(form)
    
class ConhecimentoUpdateView(UpdateView):
    model = BaseConhecimento
    form_class = UpdateConhecimentoForm
    template_name = "conhecimento/conhecimento_update.html"
    success_url = reverse_lazy('conhecimentos')
    
def ConhecimentoDelete(request, pk):
    conhecimento = get_object_or_404(BaseConhecimento, pk=pk)
    conhecimento.delete()
    return redirect("conhecimentos")
    