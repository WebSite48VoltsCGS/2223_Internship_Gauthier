from django.http import HttpResponse, JsonResponse, FileResponse
from django.views import generic
from django.shortcuts import render

from .models import Article, Client, Command
from .script import writing
import os


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
    command = Command.objects.all()
    comm_id = None

    if request.GET.get("billing_id"):
        comm_id = request.GET.get("billing_id")

    if request.method == 'POST':

        directory = f"D:\\Git\Projet\\2223_Internship_Gauthier\\fstsite\\devis"
        for filename in os.listdir(directory):
            if filename.lower().endswith('.png'):
                continue
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        prestationName = request.POST.get('nomPrestation')
        prestationLoc = request.POST.get('lieuPrestation')
        debPrestation = request.POST.get('debPrestation')
        finPrestation = request.POST.get('finPrestation')
        bidId = request.POST.get('selected_value')
        coeff = request.POST.getlist('coeff_undefined')
        discount = request.POST.getlist('discount_undefined')
        deposit = request.POST.get('Deposit')

        writing(name=prestationName, loc=prestationLoc, deb=debPrestation, fin=finPrestation, deposit=deposit,
                discount=discount, coeff=coeff, bidId=bidId)

        file_path = f"D:\\Git\Projet\\2223_Internship_Gauthier\\fstsite\\devis\\devis_{bidId}.pdf"
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="devis_{bidId}.pdf"'

        return response

    elif request.method == 'GET':
        if comm_id:
            articles = Article.objects.filter(commandline__command__billing_id=comm_id)
            articles_data = [{'name': article.product, 'value': article.is_multiple} for article in articles]
            return JsonResponse({'articles': articles_data})

    return render(request, 'devis/devis.html', {'commande': command})

def new_bid(request):
    clients = Client.objects.all()

    client_id = None

    if request.GET.get("client"):
        client_id = request.GET.get("client")

    if request.method == 'GET':
        if client_id:
            client = Client.objects.get(id=client_id)
            client_data = {'asso': client.asso, 'name': client.name,
                           'surname': client.user_name, 'lastname': client.user_lastname}
            return JsonResponse({'clientSelected': client_data})

    return render(request, 'devis/new.html', {'clients': clients})