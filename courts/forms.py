from django import forms
from .models import Court, OpeningHour, Block
from django.utils import timezone
from reservations.models import Reservation

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ["name","court_type","price_per_hour","is_active"]

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["court","weekday","start_time","end_time"]

class BlockForm(forms.ModelForm):
    start = forms.DateTimeField(
        label="Início do bloqueio",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )
    end = forms.DateTimeField(
        label="Fim do bloqueio",
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
            }
        ),
    )

    class Meta:
        model = Block
        fields = ["court", "start", "end", "reason"]

    def clean(self):
        cleaned = super().clean()

        court = cleaned.get("court")
        start = cleaned.get("start")
        end = cleaned.get("end")

        if not court or not start or not end:
            return cleaned  

        # Garantir timezone 
        tz = timezone.get_current_timezone()
        if timezone.is_naive(start):
            start = timezone.make_aware(start, tz)
        if timezone.is_naive(end):
            end = timezone.make_aware(end, tz)

        cleaned["start"] = start
        cleaned["end"] = end

        # Início < fim
        if end <= start:
            self.add_error("end", "O fim do bloqueio deve ser depois do início.")
            return cleaned

        now = timezone.now()

        #  bloqueio no passado
        if end <= now:
            self.add_error("end", "Não é possível criar bloqueios totalmente no passado.")
            return cleaned

        # conflitos com reservas
        conflict_res = Reservation.objects.filter(
            court=court,
            start__lt=end,
            end__gt=start,
        ).exists()

        conflict_block = Block.objects.filter(
            court=court,
            start__lt=end,
            end__gt=start,
        ).exists()

        if conflict_res:
            self.add_error(
                None,
                "Já existe uma reserva nesse intervalo. Ajuste o horário do bloqueio.",
            )

        if conflict_block:
            self.add_error(
                None,
                "Já existe um bloqueio nesse intervalo. Ajuste o horário."
            )

        return cleaned