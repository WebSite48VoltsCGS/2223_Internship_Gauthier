from django.urls import path

from . import views

app_name = "devis"
urlpatterns = [
    path("", views.devis, name="devis/devis.html"),
    path("new/", views.new_bid, name="devis/new.html"),
    path("update/", views.old_bid, name="devis/update.html"),
]