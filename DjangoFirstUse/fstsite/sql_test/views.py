from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Article,Client,Commande

# Create your views here.

class IndexView(generic.ListView):
    template_name = "sql/index.html"
    context_object_name = "latest_data"

    def get_queryset(self):
        """Return the five product the most in stock."""
        return Article.objects.order_by("stock")[:5]

class DetailView(generic.DetailView):
    model = Article
    template_name = "sql/detail.html"

    def get_queryset(self):
        return Article.objects.filter(stock >0)

def index(request):
    item_list = Article.objects.order_by("stock")
    output = ", ".join([q.stock for q in item_list])
    return HttpResponse(output)


class ClientView(generic.DetailView):
    model = Client
    template_name = "sql/clients.html"

    def get_queryset(self):
        return Client.objects.order_by("id")
    
class CommandeView(generic.DetailView):
    model = Commande
    template_name = "sql/commande.html"

    def get_queryset(self):
        return Commande.objects.order_by("id_client")

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            foreign_key_field =  'id_client'

            champ_cible = 'id_client__id'

            search_term_q = Q(**{f'{champ_cible}__icontains': search_term})

            try:
                search_term_int = int(search_term)
                search_term_q |= Q(**{f'{foreign_key_field}__id': search_term_int})
            except ValueError:
                pass

            queryset = queryset.filter(search_term_q)

        return queryset, use_distinct
