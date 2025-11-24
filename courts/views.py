from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Court, OpeningHour, Block
from .forms import CourtForm, OpeningHourForm, BlockForm

def staff_required(view):
    return user_passes_test(lambda u: u.is_staff)(view)

@login_required
def court_list(request):
    qs = Court.objects.all()
    return render(request, "courts/list.html", {"courts": qs})

@staff_required
def court_create(request):
    if request.method == "POST":
        form = CourtForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("court_list")
    else:
        form = CourtForm()
    return render(request, "courts/form.html", {"form": form, "title": "Nova Quadra"})

@staff_required
def court_edit(request, pk):
    court = get_object_or_404(Court, pk=pk)
    if request.method == "POST":
        form = CourtForm(request.POST, instance=court)
        if form.is_valid():
            form.save()
            return redirect("court_list")
    else:
        form = CourtForm(instance=court)
    return render(request, "courts/form.html", {"form": form, "title": "Editar Quadra"})

@staff_required
def openinghour_create(request):
    if request.method == "POST":
        form = OpeningHourForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("court_list")
    else:
        form = OpeningHourForm()
    return render(request, "courts/form.html", {"form": form, "title": "Faixa de Funcionamento"})

@staff_required
def block_create(request):
    if request.method == "POST":
        form = BlockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("court_list")
    else:
        form = BlockForm()

    return render(
        request,
        "courts/form.html",
        {
            "form": form,
            "title": "Bloqueio de horário",
        },
    )

