from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from gestao.forms import KanbanCreateForm, KanbanUpdateForm
from ..models import Tarefa


class KanbanView(ListView):
    model = Tarefa
    template_name = "kanban/kanban.html"
    context_object_name = "tarefas"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo"] = Tarefa.objects.filter(status="todo")
        context["doing"] = Tarefa.objects.filter(status="doing")
        context["done"] = Tarefa.objects.filter(status="done")
        return context
    
class KanbanUpdateView(UpdateView):
    model = Tarefa
    form_class = KanbanUpdateForm
    template_name = "kanban/kanban_update.html"
    success_url = reverse_lazy("kanban")
    
class KanbanDetailView(DetailView):
    model = Tarefa
    template_name = "kanban/kanban_detail.html"

class KanbanTarefaCreate(CreateView):
    model = Tarefa
    form_class = KanbanCreateForm
    template_name = "kanban/kanban_create.html"
    success_url = reverse_lazy("kanban")

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

def AceitarTarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if tarefa.status == "todo":
        tarefa.status = "doing"
        tarefa.responsavel = request.user
        tarefa.save()
    return redirect("kanban")

def RetornarTarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if tarefa.status == "doing":
        tarefa.status = "todo"
        tarefa.responsavel = None
        tarefa.save()
    return redirect("kanban")

def ConcluirTarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    
    if tarefa.status == "doing":
        tarefa.status = "done"
        tarefa.responsavel = request.user
        tarefa.save()
    return redirect("kanban")