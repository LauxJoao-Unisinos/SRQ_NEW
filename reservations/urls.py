from django.urls import path
from .views import my_reservations, availability, create

urlpatterns = [
    path("minhas/", my_reservations, name="my_reservations"),
    path("disponibilidade/", availability, name="availability"),
    path("nova/", create, name="reservation_create"),
]
