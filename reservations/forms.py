from django import forms
from django.utils import timezone
from datetime import timedelta
from courts.models import Court
from .models import Reservation

class AvailabilityForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    court = forms.ModelChoiceField(
        queryset=Court.objects.filter(is_active=True),
        required=True,
        label="Quadra"
    )
    duration_minutes = forms.IntegerField(
        min_value=30,
        max_value=120,
        initial=60,
        label="Duração (minutos)"
    )


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["court", "start", "end"]
        widgets = {
            "start": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "end": forms.DateTimeInput(attrs={"type":"datetime-local"}),
        }
    def clean(self):
        cleaned = super().clean()
        court = cleaned.get("court")
        start = cleaned.get("start")
        end = cleaned.get("end")
        if not (court and start and end):
            return cleaned
        if end <= start:
            self.add_error("end","Fim deve ser após o início.")
        # Regras UC06
        now = timezone.now()
        if (start - now).total_seconds() < 3600:
            self.add_error("start","Antecedência mínima de 1 hora.")
        if (start - now).days > 14:
            self.add_error("start","Antecedência máxima de 14 dias.")
        if (end - start).total_seconds() > 2*3600:
            self.add_error("end","Duração máxima de 2 horas.")
        # Conflitos
        conflict = Reservation.objects.filter(court=court, start__lt=end, end__gt=start).exists()
        from courts.models import Block
        block_conflict = Block.objects.filter(court=court, start__lt=end, end__gt=start).exists()
        if conflict or block_conflict:
            self.add_error(None, "Horário indisponível.")
        return cleaned
