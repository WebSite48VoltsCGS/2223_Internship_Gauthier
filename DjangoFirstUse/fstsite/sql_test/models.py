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
        product = models.CharField(max_length=200,default="")
        marque = models.CharField(max_length=200,default="")
        model = models.CharField(max_length = 200,default="")
        buying_price = models.FloatField(validators = [is_positive],default = 0)
        stock = models.IntegerField(validators = [is_positive],default = 0)
        location_price = models.FloatField(validators = [is_positive],default = 0)
        weight = models.FloatField(validators = [is_positive],default = 0)
        minimal_lot = models.IntegerField(validators = [is_positive],default = 0)

    
        def __str__(self):
                return (self.product + " " + self.model)

        @admin.display(
                boolean=True,
                ordering="stock",
                description="Is in stock ?",)


        def is_in_stock(self):
                return self.stock >0


class Client(models.Model):
        asso = models.BooleanField(default = True)
        siret = models.IntegerField(default = 0)
        adress = models.CharField(max_length = 200,default="")
        name = models.CharField(max_length = 200,default="")
        user_name = models.CharField(max_length = 200,default="")
        user_lastname = models.CharField(max_length = 200,default="")
        email = models.EmailField(default="")


        def __str__(self):
                return str(self.id)


class Commande(models.Model):
        article = models.ForeignKey(Article, on_delete = models.CASCADE)
        number = models.IntegerField(validators = [is_positive],default = 0)

        def __str__(self):
                return str(self.article) + " : " + str(self.number)


class Vente(models.Model):
        id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
        id_commande = models.ManyToManyField(Commande)
        paiement = models.BooleanField(default = True)
        a_payer = models.BooleanField(default = False)
        cmd_passe = models.DateTimeField(auto_now_add=True)
        cmd_paye = models.DateTimeField()
        deb_loc = models.DateTimeField()
        end_loc = models.DateTimeField()

        def __str__(self):
                return str(self.id) + " " + str(self.id_client)



