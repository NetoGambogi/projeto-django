from django.shortcuts import render, get_object_or_404, redirect
from .models import Chamado
from .forms import ChamadoForm


def chamado_list(request):
    chamados = Chamado.objects.all()
    return render (request, "chamados/list.html", {"chamados": chamados})

def chamado_create(request):
    if request.method == "POST":
        form = ChamadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chamado_list")
    else:
        form = ChamadoForm()  

    return render(request, "chamados/form.html", {"form": form})
    
def chamado_update(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if request.method == "POST":
        form = ChamadoForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
            return redirect("chamado_list")
    else:
        form = ChamadoForm(instance=chamado)
    return render(request, "chamados/form.html", {"form": form})
    
def chamado_delete(request, pk):
    chamado = get_object_or_404(Chamado, pk=pk)
    if request.method == "POST":
        chamado.delete()
        return redirect("chamado_list")
    return render(request, "chamados/confirm_delete.html", {"chamado": chamado})
