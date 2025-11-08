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
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.save()
            return redirect("my_reservations")
    else:
        form = ReservationForm()
    return render(request, "reservations/form.html", {"form": form, "title": "Nova Reserva"})
