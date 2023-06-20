from django.contrib import admin
from .models import Article,Client,Commande

# Register your models here.
    

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Name",{"fields" : ["name"]}),
                ("Model",{"fields" : ["model"]}),
                ("Price",{"fields":["price"]}),
                ("Stock",{"fields":["stock"]}),
                ]

    list_display = ["name","model","is_in_stock"]
    list_filter = ["name","price","model"]
    search_fields = ["name"]

class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Name", {"fields" : ["name"]}),
                ("Email", {"fields" : ["email"]}),
                ]

    list_display = ["id","name","email"]
    list_filter = ["id"]
    search_fields = ["id"]


class CommandeAdmin(admin.ModelAdmin):
    fieldsets = [
                ("Client", {"fields" : ["id_client"]}),
                ("Article", {"fields" : ["id_article"]}),
                ("Nombre commandé", {"fields" : ["number"]}),
                ]

    list_display = ["id_client","id_article","number"]
    list_filter = ["id_client"]


admin.site.register(Article,ArticleAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Commande,CommandeAdmin)
