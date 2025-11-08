from django.urls import path
from .views import court_list, court_create, court_edit, openinghour_create, block_create

urlpatterns = [
    path("", court_list, name="court_list"),
    path("novo/", court_create, name="court_create"),
    path("<int:pk>/editar/", court_edit, name="court_edit"),
    path("funcionamento/novo/", openinghour_create, name="openinghour_create"),
    path("bloqueio/novo/", block_create, name="block_create"),
]
