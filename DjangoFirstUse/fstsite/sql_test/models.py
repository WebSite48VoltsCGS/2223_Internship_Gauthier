from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError


# Create your models here.


def is_positive(value):
        if value < 0:
            raise ValidationError("Cannot be a negative value")


class Article(models.Model):
    name = models.CharField(max_length=200)
    model = models.CharField(max_length = 200)
    price = models.FloatField(validators = [is_positive],default = 0)
    stock = models.IntegerField(validators = [is_positive],default = 0)

    
    def __str__(self):
        return (self.name + " " + self.model)

    @admin.display(
        boolean=True,
        ordering="stock",
        description="Is in stock ?",)


    def is_in_stock(self):
        return self.stock >0


class Client(models.Model):
    name = models.CharField(max_length = 200)   #both first and last, separated by a space
    email = models.CharField(max_length = 200)


    def __str__(self):
        return self.id


class Commande(models.Model):
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    id_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    number = models.IntegerField(validators = [is_positive],default = 0)

    def __str__(self):
        return self.id + " " + self.id_client
