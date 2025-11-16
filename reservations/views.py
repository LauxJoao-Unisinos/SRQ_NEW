from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from courts.models import Court
from .models import Reservation
from .forms import AvailabilityForm, ReservationForm
from .utils import get_available_slots

@login_required
def my_reservations(request):
    qs = Reservation.objects.filter(user=request.user).order_by("-start")
    return render(request, "reservations/my_list.html", {"reservations": qs})

def availability(request):
    slots = []
    selected = {}
    form = AvailabilityForm(request.GET or None)
    if form.is_valid():
        date = form.cleaned_data["date"]
        court = form.cleaned_data["court"]
        duration = form.cleaned_data["duration_minutes"]
        selected = {"date": date, "court": court, "duration": duration}
        courts = [court] if court else list(Court.objects.filter(is_active=True))
        for c in courts:
            c_slots = get_available_slots(c, date, duration)
            slots.append((c, c_slots))
    return render(request, "reservations/availability.html", {"form": form, "slots": slots, "selected": selected})



@login_required
def create(request):
    """
    Fluxo em 2 passos:
    - GET (sem slot): usuário escolhe quadra + data + duração -> mostramos slots disponíveis
    - POST (com slot): usuário escolhe um slot -> criamos a reserva
    """
    slots = []
    selected = None  # data/court no template

    if request.method == "POST" and "slot" in request.POST:
        date_str = request.POST.get("date")
        court_id = request.POST.get("court")
        duration = int(request.POST.get("duration_minutes", "60"))
        slot_value = request.POST.get("slot") 

        court = Court.objects.get(id=court_id)
        date = datetime.fromisoformat(date_str).date()

        start_str, end_str = slot_value.split("|")
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)

        # Ajustar para timezone atual
        tz = timezone.get_current_timezone()
        if timezone.is_naive(start):
            start = timezone.make_aware(start, tz)
        if timezone.is_naive(end):
            end = timezone.make_aware(end, tz)

        form_data = {
            "court": court.id,
            "start": start,
            "end": end,
        }
        res_form = ReservationForm(form_data)
        if res_form.is_valid():
            res = res_form.save(commit=False)
            res.user = request.user
            res.save()
            return redirect("my_reservations")
        else:
            # Se der algum erro
            form = AvailabilityForm(initial={
                "date": date,
                "court": court,
                "duration_minutes": duration,
            })
            slots = get_available_slots(court, date, duration)
            # filtro adicional de regras de data
            now = timezone.now()
            valid_slots = []
            for s, e in slots:
                if (s - now).total_seconds() < 3600:
                    continue  # antecedência mínima de 1h
                if (s - now).days > 14:
                    continue  # antecedência máxima de 14 dias
                valid_slots.append((s, e))
            slots = valid_slots
            selected = {"court": court, "date": date, "duration_minutes": duration}
            return render(
                request,
                "reservations/form.html",
                {
                    "form": form,
                    "slots": slots,
                    "selected": selected,
                    "res_form_errors": res_form.errors,
                    "title": "Nova Reserva",
                },
            )

    else:
        # usuário chegou na página ou clicou em "Consultar"
        if request.method == "GET" and request.GET.get("date"):
            form = AvailabilityForm(request.GET)
            if form.is_valid():
                date = form.cleaned_data["date"]
                court = form.cleaned_data["court"]
                duration = form.cleaned_data["duration_minutes"]

                all_slots = get_available_slots(court, date, duration)

                now = timezone.now()
                slots = []
                for s, e in all_slots:
                    if (s - now).total_seconds() < 3600:
                        continue  # antecedência mínima 1h
                    if (s - now).days > 14:
                        continue  # antecedência máxima 14 dias
                    slots.append((s, e))

                selected = {"court": court, "date": date, "duration_minutes": duration}
            else:
                slots = []
        else:
            form = AvailabilityForm()

    return render(
        request,
        "reservations/form.html",
        {
            "form": form,
            "slots": slots,
            "selected": selected,
            "title": "Nova Reserva",
        },
    )

