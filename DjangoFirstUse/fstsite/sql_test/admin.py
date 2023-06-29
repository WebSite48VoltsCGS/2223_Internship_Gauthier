from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from .models import Article, Client, Commande, Vente, Pack

# Register your models here.


# Macro definition

fields = "fields"


# Extra functions


# Class definition


class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["product"]}),
        (None, {fields: ["model"]}),
        (None, {fields: ["buying_price"]}),
        (None, {fields: ["stock"]}),
        (None, {fields: ["location_price"]}),
        (None, {fields: ["weight"]}),
        (None, {fields: ["minimal_lot"]}),
    ]

    list_display = ["product", "model", "is_in_stock"]
    list_filter = ["product", "model"]
    search_fields = ["product"]


class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["asso"]}),
        (None, {fields: ["name"]}),
        (None, {fields: ["siret"]}),
        (None, {fields: ["user_name"]}),
        (None, {fields: ["user_lastname"]}),
        (None, {fields: ["adress"]}),
        (None, {fields: ["email"]}),
    ]

    list_display = ["name", "user_name", "user_lastname", "email"]
    list_filter = ["name", "user_lastname"]
    search_fields = ["name", "user_lastname"]


class VenteAdmin(admin.ModelAdmin):
    formfield_overrides = {models.ManyToManyField:
            {'widget': FilteredSelectMultiple(verbose_name='Commandes', is_stacked=False)}, }
    fieldsets = [
        (None, {fields: ["id_client"]}),
        (None, {fields: ["id_commande"]}),
        (None, {fields: ["billing"]}),
        (None, {fields: ["a_payer"]}),
        (None, {fields: ["cmd_payed"]}),
        (None, {fields: ["deb_loc"]}),
        (None, {fields: ["end_loc"]}),
        (None, {fields: ["bid_date"]}),
        (None, {fields: ["got_payed"]}),
    ]

    list_display = ["id_bid", "id_client", "cmd_passe", "billing", "a_payer", "cmd_payed", "deb_loc", "end_loc"]
    list_filter = ["id_bid"]


class CommandeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["article"]}),
        (None, {fields: ["number"]}),
    ]

    list_display = ["article", "number"]
    list_filter = ["article"]

class PackAdmin(admin.ModelAdmin):
    formfield_overrides = {models.ManyToManyField:
            {'widget': FilteredSelectMultiple(verbose_name='lot', is_stacked=False)}, }
    fieldsets = [
        (None, {fields: ["name"]}),
        (None, {fields: ["lot"]}),
        (None, {fields: ["price"]}),
        ]

    list_display = ["name"]
    list_filter = ["id", "name"]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Vente, VenteAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Pack, PackAdmin)
