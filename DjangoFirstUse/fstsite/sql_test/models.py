from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone


# Create your models here.


def is_positive(value):
        if value <= 0:
                raise ValidationError("Cannot be a negative value")


class Article(models.Model):
        product = models.CharField(max_length=200)
        marque = models.CharField(max_length=200)
        model = models.CharField(max_length = 200)
        buying_price = models.FloatField(validators = [is_positive],default = 0)
        stock = models.IntegerField(validators = [is_positive],default = 0)
        location_price = models.FloatField(validators = [is_positive],default = 0)
        weight = models.FloatField(validators = [is_positive],default = 0)
        minimal_lot = models.IntegerField(validators = [is_positive],default = 0)

    
        def __str__(self):
                return (self.name + " " + self.model)

        @admin.display(
                boolean=True,
                ordering="stock",
                description="Is in stock ?",)


        def is_in_stock(self):
                return self.stock >0


class Client(models.Model):
        asso = models.BooleanField()
        siret = models.IntegerField(default = 0)
        adress = models.CharField(max_length = 200)
        name = models.CharField(max_length = 200)
        user_name = models.CharField(max_length = 200)
        user_lastname = models.CharField(max_length = 200)


        def __str__(self):
                return str(self.id)


class Commande(models.Model):
        id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
        id_article = models.ForeignKey(Article, on_delete=models.CASCADE)       # devra être une liste
        number = models.IntegerField(validators = [is_positive],default = 0)    # devra être une liste
        paiement = models.BooleanField()
        a_payer = models.BooleanField()
        est_paye = models.BooleanField()
        cmd_passe = models.DateTimeField()
        cmd_paye = models.DateTimeField()
        deb_loc = models.DateTimeField()
        end_loc = models.DateTimeField()

        def __str__(self):
                return str(self.id) + " " + str(self.id_client)
