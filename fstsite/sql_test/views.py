from django.http import HttpResponse, JsonResponse
from django.views import generic
from django.shortcuts import render

from .models import Article, Client, Command


# Macro and variable

prestationName = ""
prestationLoc = ""
debPrestation = ""
finPrestation = ""

# Create your views here.

class IndexView(generic.ListView):
    template_name = "sql/index.html"
    context_object_name = "latest_data"

    def get_queryset(self):
        return Article.objects.order_by("stock")[:5]

class DetailView(generic.DetailView):
    model = Article
    template_name = "sql/detail.html"

    def get_queryset(self):
        return Article.objects.filter(self.stock > 0)

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
    model = Command
    template_name = "sql/commande.html"

    def get_queryset(self):
        return Command.objects.order_by("article")

def devis(request):
    global prestationLoc, prestationName, debPrestation, finPrestation

    command = Command.objects.all()

    if request.method == 'POST':
        prestationName = request.POST.get('nomPrestation')
        prestationLoc = request.POST.get('lieuPrestation')
        debPrestation = request.POST.get('debPrestation')
        finPrestation = request.POST.get('finPrestation')

    elif request.method == 'GET':
        comm_id = request.GET.get('comm_id')
        if comm_id:
            comm = Command.objects.get(id=comm_id)
            commandes_data = [{'id': comm.id, 'article': comm.article}]
            return JsonResponse({'commandes': commandes_data})

    return render(request, 'devis/devis.html', {'ventes': ventes})
