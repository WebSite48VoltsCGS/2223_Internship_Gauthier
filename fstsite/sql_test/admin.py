from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from .models import Article, Client, Command, Component
# Register your models here.


# Macro definition

fields = "fields"


# Extra functions


# Class definition

class ComponentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["kit"]}),
        (None, {fields: ["article"]}),
        (None, {fields: ["number"]}), ]


class ComponentLine(admin.TabularInline):
    model = Component
    fk_name = "kit"
    extra = 0
    fields = ["article", "number"]

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["product"]}),
        (None, {fields: ["buying_price"]}),
        (None, {fields: ["is_multiple"]}),
        (None, {fields: ["stock"]}),
        (None, {fields: ["location_price"]}),
        (None, {fields: ["weight"]}),
        (None, {fields: ["minimal_lot"]}),
    ]
    inlines = [ComponentLine, ]

    list_display = ["product", "is_in_stock"]
    list_filter = ["product"]
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

class CommandAdmin(admin.ModelAdmin):
    fieldsets = [
    ]

    list_display = []
    list_filter = []


admin.site.register(Article, ArticleAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Component, ComponentAdmin)