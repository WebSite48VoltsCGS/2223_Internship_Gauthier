from django.urls import path

from . import views

app_name = "devis"
urlpatterns = [
    path("", views.devis, name="devis/devis.html"),
]