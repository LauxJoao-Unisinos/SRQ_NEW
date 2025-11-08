from datetime import datetime, time, timedelta
from django.utils import timezone
from courts.models import OpeningHour, Block
from .models import Reservation

SLOT_MINUTES = 30

def get_available_slots(court, date, duration_minutes=60):
    tz = timezone.get_current_timezone()
    weekday = date.weekday()  # 0=Mon
    # Construir janelas válidas a partir do funcionamento
    windows = []
    for oh in OpeningHour.objects.filter(court=court, weekday=weekday):
        start_dt = tz.localize(datetime.combine(date, oh.start_time))
        end_dt = tz.localize(datetime.combine(date, oh.end_time))
        windows.append((start_dt, end_dt))
    # Remover bloqueios e reservas
    blocks = list(Block.objects.filter(court=court, start__date=date) |
                  Block.objects.filter(court=court, end__date=date))
    resvs = list(Reservation.objects.filter(court=court, start__date=date) |
                 Reservation.objects.filter(court=court, end__date=date))
    # Gerar slots discretizados
    slots = []
    step = timedelta(minutes=SLOT_MINUTES)
    dur = timedelta(minutes=duration_minutes)
    for wstart, wend in windows:
        start = wstart
        while start + dur <= wend:
            end = start + dur
            # checar conflitos
            conflict = any((b.start < end and b.end > start) for b in blocks) or                        any((r.start < end and r.end > start) for r in resvs)
            if not conflict:
                slots.append((start, end))
            start += step
    return slots
