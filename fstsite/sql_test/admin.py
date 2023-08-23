from django.contrib import admin
from .models import Article, Client, Command, Component, CommandLine
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
        (None, {fields: ["brand"]}),
        (None, {fields: ["category"]}),
        (None, {fields: ["sub_category"]}),
        (None, {fields: ["denomination"]}),
        (None, {fields: ["description"]}),
        (None, {fields: ["sell_or_loc"]}),
        (None, {fields: ["is_multiple"]}),
        (None, {fields: ["buying_price"]}),
        (None, {fields: ["stock"]}),
        (None, {fields: ["location_price"]}),
        (None, {fields: ["weight"]}),
        (None, {fields: ["minimal_lot"]}),
    ]
    inlines = [ComponentLine, ]

    list_display = ["product", "brand", "is_in_stock"]
    list_filter = ["product", "brand", "category", "sub_category"]
    search_fields = ["product", "internal_id", "brand", "category", "sub_category"]


class ClientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["asso"]}),
        (None, {fields: ["name"]}),
        (None, {fields: ["siret"]}),
        (None, {fields: ["user_name"]}),
        (None, {fields: ["user_lastname"]}),
        (None, {fields: ["adress"]}),
        (None, {fields: ["email"]}),
        (None, {fields: ["phone"]}),
    ]

    list_display = ["name", "user_name", "user_lastname", "email"]
    list_filter = ["name", "user_lastname"]
    search_fields = ["name", "user_lastname", "email", "phone"]

class CommandLineAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {fields: ["command"]}),
        (None, {fields: ["article"]}),
        (None, {fields: ["number"]}), ]

    list_display = ["command", "article"]
    list_filter = ["command"]

class CommandLineFun(admin.TabularInline):
    model = CommandLine
    fk_name = "command"
    extra = 0
    fields = ["command", "article", "number"]


class CommandAdmin(admin.ModelAdmin):
    inlines = [CommandLineFun, ]
    fieldsets = [
        (None, {fields: ["billing_date"]}),
        (None, {fields: ["client"]}),
        (None, {fields: ["is_payed"]}),
        (None, {fields: ["paiment_date"]}),
        (None, {fields: ["loc_place"]}),
        (None, {fields: ["start_loc"]}),
        (None, {fields: ["end_loc"]}), ]

    list_display = ["billing_id", "client"]
    list_filter = ["billing_id", "client"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(CommandLine, CommandLineAdmin)
