from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from courts.models import Court

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="reservations")
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["start","end","court"])]

    def __str__(self):
        return f"{self.court} - {self.start}"
