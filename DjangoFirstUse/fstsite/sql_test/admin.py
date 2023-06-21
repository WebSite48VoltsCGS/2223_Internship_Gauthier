from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from .models import Article,Client,Commande,Vente

# Register your models here.


# Macro definition

fields = "fields"



# Extra functions



# Class definition
    

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Product",{fields : ["product"]}),
                ("Model",{fields : ["model"]}),
                ("Purchase price",{fields:["buying_price"]}),
                ("Stock",{fields:["stock"]}),
                ("Location price",{fields:["location_price"]}),
                ("Weight",{fields:["weight"]}),
                ("Minimal bundle",{fields:["minimal_lot"]}),
                ]

    list_display = ["product","model","is_in_stock"]
    list_filter = ["product","model"]
    search_fields = ["product"]

class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Asso", {fields : ["asso"]}),
                ("Name",{fields:["name"]}),
                ("Siret", {fields : ["siret"]}),
                ("Firstname",{fields:["user_name"]}),
                ("Lastname",{fields:["user_lastname"]}),
                ("Adress",{fields:["adress"]}),
                ("Email",{fields:["email"]}),
                ]

    list_display = ["id","name","user_name","user_lastname","email"]
    list_filter = ["id"]
    search_fields = ["id"]


class VenteAdmin(admin.ModelAdmin):

    formfield_overrides = { models.ManyToManyField: {'widget': FilteredSelectMultiple(verbose_name='Commandes', is_stacked=False)},}


    fieldsets = [
                ("Client", {fields : ["id_client"]}),
                ("Commandes",{fields:["id_commande"]}),
                ("Paiement", {fields : ["paiement"]}),
                ("Est à payer", {fields : ["a_payer"]}),
                ("Commande payée" , {fields : ["cmd_paye"]}),
                ("Début de location" , {fields : ["deb_loc"]}),
                ("Fin de location" , {fields : ["end_loc"]}),
                ]

    
    list_display = ["id_client","cmd_passe","paiement","a_payer","cmd_paye","deb_loc","end_loc"]
    list_filter = ["id_client"]



class CommandeAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Article", {fields : ["article"]}),
                ("Nombre",{fields:["number"]}),
                ]

    list_display = ["article","number"]
    list_filtre = ["article"]


admin.site.register(Article,ArticleAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Vente,VenteAdmin)
admin.site.register(Commande,CommandeAdmin)
