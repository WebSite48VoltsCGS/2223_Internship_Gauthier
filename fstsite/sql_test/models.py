from django.db import models
from django.db.models import UniqueConstraint
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


# Create your models here.


# Macro definition


# Extra functions


def is_positive(value):
    if value < 0:
        raise ValidationError("Cannot be 0 or a negative value")

def is_empty(tab):
    return not tab


# Class definition


class Article(models.Model):
    product = models.CharField(max_length=200, default="")
    brand = models.CharField(max_length=200, default="")
    category = models.CharField(max_length=200, default="")
    sub_category = models.CharField(max_length=200, default="")
    denomination = models.CharField(max_length=200, default="")
    description = models.TextField(max_length=200, default="", blank=True, null=True)
    sell_or_loc = models.BooleanField(default=False)
    is_multiple = models.BooleanField(default=False)
    article = models.ManyToManyField('self', through='Component', blank=True, symmetrical=False,
                                     related_name='related_components')
    buying_price = models.FloatField(validators=[is_positive], default=1)
    stock = models.IntegerField(validators=[is_positive], default=0)
    location_price = models.FloatField(validators=[is_positive], default=1)
    weight = models.FloatField(validators=[is_positive], default=1)
    minimal_lot = models.IntegerField(validators=[is_positive], default=1)

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
        weighted_sum = 0
        lst_component = Component.objects.filter(kit_id=self.id)
        for component in lst_component:
            weighted_sum += component.article.update_weight() * component.number

        if weighted_sum != 0:
            return weighted_sum
        return w


@receiver(post_save, sender=Article)
def post_save_article(sender, instance, **kwargs):
    if instance.weight != instance.update_weight():
        instance.weight = instance.update_weight()
        instance.save()
    if is_empty(instance.article.all()):
        if instance.is_multiple:
            instance.is_multiple = False
            instance.save()
    else:
        if not instance.is_multiple:
            instance.is_multiple = True
            instance.save()


class Component(models.Model):
    kit = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='parent_article', blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='component_article', blank=True,
                                null=True)
    number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Article {self.article} from {self.kit}'


class Client(models.Model):
    asso = models.BooleanField(default=True)
    siret = models.IntegerField(null=True, blank=True, unique=True)
    adress = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=200, null=True, blank=True, unique=True)
    user_name = models.CharField(max_length=200, default="", blank=True)
    user_lastname = models.CharField(max_length=200, default="", blank=True)
    email = models.EmailField(default="", blank=True, unique=True)
    phone = models.CharField(max_length=10, default="")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['email'], name='email'),
            UniqueConstraint(fields=['siret'], name='siret'),
            UniqueConstraint(fields=['name'], name='name'),
            UniqueConstraint(fields=['phone'], name='phone')
        ]

    def __str__(self):
        if self.asso:
            return f'{self.name} SIRET number {self.siret}'
        elif self.user_lastname is None:
            return f'{self.user_name}'
        else:
            return f'{self.user_name} {self.user_lastname}'


    def clean(self):

        if self.asso and self.siret is None:
            raise ValidationError("Siret must be filled out for an association")
        if not self.asso and self.siret is not None:
            raise ValidationError("Cannot have a siret number for a person")
        if not self.asso and self.name is not None:
            raise ValidationError("Cannot have an association name for a person")

class Command(models.Model):
    billing_id = models.CharField(max_length=200, default="")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    articles = models.ManyToManyField(Article, through='CommandLine')
    is_payed = models.BooleanField(default=False)
    billing_date = models.DateTimeField(default=timezone.now)
    paiment_date = models.DateTimeField(blank=True)
    loc_place = models.CharField(max_length=200, default="")
    start_loc = models.DateTimeField()
    end_loc = models.DateTimeField()

    @staticmethod
    def generate_id():
        formatted_date = timezone.now().strftime('%Y%m%d')
        formatted_numero = str(Command.objects.filter(billing_id__startswith=formatted_date).count()+1).zfill(2)
        return f'{formatted_date}-{formatted_numero}'

    def __str__(self):
        return f'Commande {self.billing_id} from {self.client}'

@receiver(pre_save, sender=Command)
def pre_save_command(sender, instance, **kwargs):
    if instance.billing_id == "":
        instance.billing_id = instance.generate_id()


class CommandLine(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'Article {self.article} from {self.command}'