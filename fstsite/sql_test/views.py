from django.http import HttpResponse, JsonResponse, FileResponse
from django.views import generic
from django.shortcuts import render
from django.core import serializers

from .models import Article, Client, Command, CommandLine
from .script import writing
import os
import json


# Macro, variable and function

def betterDate(date):
    if date != "":
        month = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre',
             'Novembre', 'Décembre']

        onlyDate = date[:10]
        onlyDate = onlyDate.split("-")
        print(onlyDate[1])
        return f'{onlyDate[2]} {month[int(onlyDate[1]-1)]} {onlyDate[0]}'
    return date

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
    test = True
    clients = [{'name': client, 'id': client.id} for client in Client.objects.all()]
    articles = [{'product': article.product, 'internalId': article.internal_id, 'price': article.buying_price}
                for article in Article.objects.all()]

    if request.method == 'POST':

        directory = f"D:\\Git\Projet\\2223_Internship_Gauthier\\fstsite\\devis"
        for filename in os.listdir(directory):
            if filename.lower().endswith('.png'):
                continue
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        client = request.POST.get('Client')
        dateStart = request.POST.get('datestart')
        dateEnd = request.POST.get('dateend')
        bidArticles = request.POST.getlist('Article')
        number = request.POST.getlist('nombre[]')
        coeff = request.POST.getlist('coeff[]')
        discount = request.POST.getlist('reduction[]')
        nomPrestation = request.POST.get('nomPrestation')
        nomPlace = request.POST.get('nomPlace')
        deposit = request.POST.get('Deposit')

        bidArticles.pop(0)

        idArticles = [Article.objects.get(internal_id=json.loads(bidArticles[i].replace("'", "\""))['internalId'])
                      for i in range(len(bidArticles))]

        if not deposit:
            deposit = 0
        if '' in coeff:
            coeff = [1 for _ in range(len(bidArticles))]
        if '' in discount:
            discount = [0 for _ in range(len(bidArticles))]
        if dateEnd is None:
            dateEnd = ""



        search_string = "'id': "
        id_value = ""

        start_index = client.find(search_string)
        if start_index != -1:
            start_index += len(search_string)
            end_index = client.find("}", start_index)
            if end_index == -1:
                end_index = len(input_string)
            id_value = client[start_index:end_index].strip()

        client = Client.objects.get(id=int(id_value))

        if dateEnd == "":
            command = Command(client=client, loc_place=nomPlace, start_loc=dateStart)
        else:
            command = Command(client=client, loc_place=nomPlace, start_loc=dateStart, end_loc=dateEnd,
                              description=nomPrestation, deposit=deposit)
        command.save()

        for i, article in enumerate(idArticles):
            line = CommandLine(command=command, article=article, number=int(number[i]), coeff=int(coeff[i]),
                               discount=int(discount[i]))
            line.save()

        writing(name=nomPrestation, loc=nomPlace, deb=betterDate(dateStart), fin=betterDate(dateEnd), deposit=deposit,
                discount=discount, coeff=coeff, bidId=command.billing_id)

        file_path = f"D:\\Git\Projet\\2223_Internship_Gauthier\\fstsite\\devis\\devis_{command.billing_id}.pdf"
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="devis_{command.billing_id}.pdf"'

        return response

    return render(request, 'devis/new.html', {'article_data': articles, 'clients': clients})


def old_bid(request):
    command = Command.objects.all()
    articles = [{'product': article.product, 'internalId': article.internal_id, 'price': article.buying_price}
                for article in Article.objects.all()]
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
            lines = CommandLine.objects.filter(command=Command.objects.get(billing_id=comm_id))
            return JsonResponse({'lines': lines})

    return render(request, 'devis/update.html', {'article_data': articles, 'commande': command})