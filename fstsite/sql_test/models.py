from django.db import models
from django.db.models import UniqueConstraint
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.


# Macro definition


# Extra functions


def is_positive(value):
    if value <= 0:
        raise ValidationError("Cannot be 0 or a negative value")


# Class definition


class Article(models.Model):
    product = models.CharField(max_length=200, default="")
    is_multiple = models.BooleanField(default=False)
    article = models.ManyToManyField('self', through='Component', blank=True, symmetrical=False,
                                     related_name='related_components')
    buying_price = models.FloatField(validators=[is_positive], default=0)
    stock = models.IntegerField(validators=[is_positive], default=0)
    location_price = models.FloatField(validators=[is_positive], default=0)
    weight = models.FloatField(validators=[is_positive], default=0)
    minimal_lot = models.IntegerField(validators=[is_positive], default=0)

    def __str__(self):
        return str(self.product)

    @admin.display(
        boolean=True,
        ordering="stock",
        description="Is in stock ?", )

    def is_in_stock(self):
        return self.stock > 0

    def update_weight(self):
        w = self.weight
        cnt = 0

        for article in self.article.all():
            cnt += 1
            w += article.update_weight()

        if cnt == 0:
            return self.weight

        return w

    def clean(self):
        self.save()
        if self.is_multiple:
            if len(self.article.all()) == 0:
                self.delete()
                raise ValidationError("Cannot have no item for a multiple selection !")
            self.weight = self.update_weight()
        else:
            self.save()
            if len(self.article.all()) != 0:
                self.delete()
                raise ValidationError("Cannot be a multiple article without components !")


class Component(models.Model):
    kit = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='parent_article', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='component_article', blank=True, null=True)
    number = models.PositiveIntegerField(default=1)


class Client(models.Model):
    asso = models.BooleanField(default=True)
    siret = models.IntegerField(null=True, blank=True, unique=True)
    adress = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    user_name = models.CharField(max_length=200, default="", blank=True)
    user_lastname = models.CharField(max_length=200, default="", blank=True)
    email = models.EmailField(default="", blank=True, unique=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['email'], name='email'),
            UniqueConstraint(fields=['siret'], name='siret'),
            UniqueConstraint(fields=['name'], name='name'),
        ]

    def __str__(self):
        if self.asso:
            return str(self.name) + " SIRET number " + str(self.siret)
        elif self.user_lastname is None:
            return str(self.user_name)
        else:
            return str(self.user_name) + " " + str(self.user_lastname)


    def clean(self):

        if self.asso and self.siret is None:
            raise ValidationError("Siret must be filled out for an association")
        if not self.asso and self.siret is not None:
            raise ValidationError("Cannot have a siret number for a person")
        if not self.asso and self.name is not None:
            raise ValidationError("Cannot have an association name for a person")

class Command(models.Model):
    billing_id = models.CharField(max_length=200, default="")
    articles = models.ManyToManyField(Article, through='CommandLine')
    is_payed = models.BooleanField(default=False)
    billing_date = models.DateTimeField(default=timezone.now)
    paiment_date = models.DateTimeField(default=timezone.now)
    start_loc = models.DateTimeField()
    end_loc = models.DateTimeField()

    def generate_id(self):
        formatted_date = timezone.now().strftime('%Y%m%d')
        formatted_numero = str(Command.objects.filter(billing_id__startswith=formatted_date).count() + 1).zfill(2)
        self.billing_id = f'{formatted_date}-{formatted_numero}'


class CommandLine(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)