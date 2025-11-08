from django.db import models

COURT_TYPES = [
    ("futebol", "Futebol"),
    ("basquete", "Basquete"),
    ("tenis", "Tênis"),
    ("volei", "Vôlei"),
]

class Court(models.Model):
    name = models.CharField(max_length=100, unique=True)
    court_type = models.CharField(max_length=20, choices=COURT_TYPES)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class OpeningHour(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="opening_hours")
    weekday = models.IntegerField(help_text="0=Seg ... 6=Dom")
    start_time = models.TimeField()
    end_time = models.TimeField()
    class Meta:
        unique_together = ("court", "weekday", "start_time", "end_time")

class Block(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="blocks")
    start = models.DateTimeField()
    end = models.DateTimeField()
    reason = models.CharField(max_length=200, blank=True)
    class Meta:
        indexes = [models.Index(fields=["start","end"])]
