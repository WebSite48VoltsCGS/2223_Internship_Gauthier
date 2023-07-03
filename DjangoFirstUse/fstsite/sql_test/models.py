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
    marque = models.CharField(max_length=200, default="")
    model = models.CharField(max_length=200, default="")
    buying_price = models.FloatField(validators=[is_positive], default=0)
    stock = models.IntegerField(validators=[is_positive], default=0)
    location_price = models.FloatField(validators=[is_positive], default=0)
    weight = models.FloatField(validators=[is_positive], default=0)
    minimal_lot = models.IntegerField(validators=[is_positive], default=0)

    def __str__(self):
        return str(self.product) + " " + str(self.model)

    @admin.display(
        boolean=True,
        ordering="stock",
        description="Is in stock ?", )
    def is_in_stock(self):
        return self.stock > 0


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

        # check of repetition


class Commande(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)

    def clean(self):
        is_positive(self.number)
        article = self.article

        if article.stock == 0 or article.stock < article.minimal_lot:
            raise ValidationError("This product is currently unavailable")
        if article.stock - self.number < 0:
            raise ValidationError("Not enough product in stock. Their is " + str(article.stock) + " left")
        if article.minimal_lot - self.number > 0:
            raise ValidationError("Cannot buy less than " + str(article.minimal_lot))

    def __str__(self):
        return str(self.number) + " " + str(self.article)

class Pack(models.Model):
    name = models.CharField(max_length=200, default="")
    lot = models.ManyToManyField(Commande)
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.name)

class Vente(models.Model):
    id_bid = models.CharField(max_length=13, default="")
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    id_commande = models.ManyToManyField(Commande)
    billing = models.BooleanField(default=True)
    a_payer = models.BooleanField(default=False)
    cmd_passe = models.DateTimeField(default=timezone.now)
    cmd_payed = models.DateTimeField(null=True, blank=True)
    deb_loc = models.DateTimeField()
    end_loc = models.DateTimeField()
    bid_date = models.DateTimeField(null=True, blank=True)
    got_payed = models.DateTimeField(null=True, blank=True)


    def generate_id(self):
        formatted_date = timezone.now().strftime('%Y%m%d')
        formatted_numero = str(Vente.objects.filter(id_bid__startswith=formatted_date).count()+1).zfill(2)
        self.id_bid = f'{formatted_date}-{formatted_numero}'
        self.save()

    def __str__(self):
        if self.id_bid == "":
            self.generate_id()
        client = self.id_client
        return str(self.id_bid) + " to the name of " + str(client.user_name) + " " + str(client.user_lastname)


    def clean(self):

        # date correction
        if self.deb_loc > self.end_loc:
            raise ValidationError("Impossible to have a renting start date after the end of the renting")
        if self.deb_loc < self.cmd_passe:
            raise ValidationError("Impossible to have a renting before a command has been sent")
        if self.a_payer and (self.got_payed is None):
            raise ValidationError("Impossible to have a date of payment if no payment has been made")
        if self.got_payed is not None:
            if self.got_payed < self.cmd_passe:
                raise ValidationError("Impossible to have been payed before the command has been sent")
        # update of the stock

        if self.a_payer:
            if not Vente.objects.get(pk=self.pk).a_payer:
                for commande in self.id_commande.all():
                    article = commande.article
                    article.stock -= commande.number
                    article.save()


